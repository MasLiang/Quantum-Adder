from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
import sys
sys.path.append("..")
from Basic_Gates.init_state import bit2state
from BQFA.BQFA_Sum_First import *
from BQFA.BQFA_in_Cuccaro import *
from BQFA.BQFA_in_Google import *

def QMDA_mixed(circ, q, c, n):
    '''
    This circuit is QMDA with qubit-efficient and low T-count optimisations by using 
        temporary logical-AND [13], carry- and sum-first QFAs. If user wants to add 
        it in their circuits, they need to pass their circuit, qubits, classical 
        registers and length of input data that will be used in this circuit.

    input:
        circ        :       circuit
        q           :       input qubit 
        c           :       classical register
        n           :       length of input data
    output:
        circ        :       circuit
    
    **Example:**

    circ = OA_Sum_google_mixed(circ, q, c, n)

    '''
    circ.x(q[1])
    circ = MAG(circ,q[0], q[1], q[2])
    for i in range(1,n):
        circ.x(q[5*i+1])
        circ = BQFA_Sum_first_left(circ, q[5*i+0], q[5*i+1], q[5*i+2])
    circ.x(q[3])
    circ = BQFA_in_Google(circ, q[2], q[3], q[5], q[4])
    circ.x(q[3])
    circ = UMA_1(circ, q[0], q[1], q[2])
    circ.measure(q[1], c[0])
    for i in range(1,n):
        circ = BQFA_Sum_first_right(circ, q[5*i+0], q[5*i+1], q[5*i+2])
        circ.x(q[5*i+3])
        circ = BQFA_in_Google(circ, q[5*i+2], q[5*i+3], q[5*i+5], q[5*i+4])
        circ.x(q[5*i+3])
    for i in range(n):
        circ.measure(q[5*i+3],c[2*i+1])
        circ.measure(q[5*i+4],c[2*i+2])
    circ.measure(q[5*n+1],c[2*n+1])

    return circ

if __name__ == "__main__":
    data_A = "1111"
    data_B = "1111"
    Carry = "11"        
    n = len(data_A)//2
    # initiate 3 qubits
    q = QuantumRegister(5*n+2,'q')
    # initiate 2 traditional bits
    c = ClassicalRegister(2*n+2,'c')
    #initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # transform custom bit to quantum state vector
    data_string = ''
    for i in range(n):
        data_string += data_A[2*i:2*i+2]
        data_string += data_B[2*i:2*i+2]
        data_string += '0'
    data_string += Carry
    initial_state = bit2state(data_string)
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = QMDA_mixed(circ, q, c, n)
    print(circ.draw())

    # Build a simulator to exert the quantum circuit
    backend = QasmSimulator()

    # First we have to transpile the quantum circuit
    # to the low-level QASM instructions used by the
    # backend
    circ_compiled = transpile(circ, backend)

    # Execute the circuit on the qasm simulator.
    # We've set the number of repeats of the circuit
    # to be 1, because each state of each qubit is |0> or |1> 
    # rather than superposition state.
    job_sim = backend.run(circ_compiled, shots=1)

    # Grab the results from the job.
    result_sim = job_sim.result()
    counts = result_sim.get_counts(circ_compiled)
    print(counts)