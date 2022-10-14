from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
import sys
sys.path.append("..")
from Basic_Gates.init_state import bit2state
from BQFA.BQFA_in_Mazumder import *

def QMDA_in_Mazumder(circ, q, c, n):
    '''
    This circuit is quantum online adder using the binary quantum full adder proposed 
        in (Mazumder. 2008). If user wants to add it in their circuits, they need to 
        pass their circuit, qubits, classical registers and length of input data that 
        will be used in this circuit. 

    input:
        circ        :       circuit
        q           :       input qubit 
        c           :       classical register
        n           :       length of input data
    output:
        circ        :       circuit
    
    **Example:**

    circ = QMDA_in_Mazumder(circ, q, c, n)

    '''
    for i in range(n):
        circ.x(q[12*i+2])
        circ = BQFA_in_Mazumder(circ, q[12*i],q[12*i+1],q[12*i+2],q[12*i+3],q[12*i+4],q[12*i+5],q[12*i+6])
    circ.measure(q[1],c[0])
    for i in range(n-1):
        circ.x(q[12*i+8])
        circ = BQFA_in_Mazumder(circ, q[12*i+4],q[12*i+7],q[12*i+8],q[12*i+13],q[12*i+9],q[12*i+10],q[12*i+11])
        circ.x(q[12*i+8])
        circ.measure(q[12*i+8],c[2*i+1])
        circ.measure(q[12*i+9],c[2*i+2])
    circ.x(q[12*n-4])
    circ = BQFA_in_Mazumder(circ, q[12*n-8],q[12*n-5],q[12*n-4],q[12*n],q[12*n-3],q[12*n-2],q[12*n-1])
    circ.x(q[12*n-5])
    circ.measure(q[12*n-5],c[2*n-1])
    circ.measure(q[12*n-3],c[2*n])
    circ.measure(q[12*n+1],c[2*n+1])
    return circ

if __name__ == "__main__":
    data_A = "1111"
    data_B = "0010"
    Carry = "10"     
    n = len(data_A)//2
    # initiate 3 qubits
    q = QuantumRegister(12*n+2,'q')
    # initiate 2 traditional bits
    c = ClassicalRegister(2*n+2,'c')
    #initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # transform custom bit to quantum state vector
    data_string = ''
    for i in range(n):
        data_string += data_A[2*i]
        data_string += '1'
        data_string += data_A[2*i+1]
        data_string += data_B[2*i]
        data_string += '0011'
        data_string += data_B[2*i+1]
        data_string += '001'
    data_string += Carry
    initial_state = bit2state(data_string)
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = QMDA_in_Mazumder(circ, q, c, n)
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