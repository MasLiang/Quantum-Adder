from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
import sys
sys.path.append("..")
from Basic_Gates.init_state import bit2state
from BQFA.BQFA_in_Mazumder import *

def CRA_in_Mazumder(circ, q, c, n):
    '''
    This circuit is quantum carry-ripple adder using the binary quantum full adder proposed 
        in (Mazumder, et al. 2008). If user wants to add it in their circuits, they need 
        to pass their circuit, qubits, classical registers and length of input data 
        that will be used in this circuit. 

    input:
        circ        :       circuit
        q           :       input qubit 
        c           :       classical register
        n           :       length of input data
    output:
        circ        :       circuit
    
    **Example:**

    circ = CRA_in_Mazumder(circ, q, c, n)

    '''
    circ = BQFA_in_Mazumder(circ, q[0],q[1],q[2],q[3],q[4],q[5],q[6])
    circ.measure(q[1],c[0])
    for i in range(1,n):
        circ = BQFA_in_Mazumder(circ, q[6*i+1],q[6*i+2],q[6*i+3],q[6*i-2],q[6*i+4],q[6*i+5],q[6*i+6]) 
        circ.measure(q[6*i+2],c[i])
    circ.measure(q[6*n-2],c[n])
    return circ

if __name__ == "__main__":
    data_A = "11"
    data_B = "01"
    data_A = data_A[::-1]
    data_B = data_B[::-1]      
    Carry_in = '1'
    n = len(data_A)
    # initiate 3 qubits
    q = QuantumRegister(6*n+1,'q')
    # initiate 2 traditional bits
    c = ClassicalRegister(n+1,'c')
    #initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # transform custom bit to quantum state vector
    data_string = ''
    data_string += data_A[0]
    data_string += '1'
    data_string += data_B[0]
    data_string += Carry_in
    data_string += '001'
    for i in range(1,n):
        data_string += data_A[i]
        data_string += '1'
        data_string += data_B[i]
        data_string += '001'
    # data_string = data_string[::-1]
    initial_state = bit2state(data_string)
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = CRA_in_Mazumder(circ, q, c, n)
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