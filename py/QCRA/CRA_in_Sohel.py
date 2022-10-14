from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
import sys
sys.path.append("..")
from Basic_Gates.init_state import bit2state
from BQFA.BQFA_in_Sohel import *

def CRA_in_Sohel(circ, q, c, n):
    '''
    This circuit is quantum carry-ripple adder using the binary quantum full adder proposed 
        in (Sohel, et al. 2008). If user wants to add it in their circuits, they need 
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

    circ = CRA_in_Sohel(circ, q, c, n)

    '''
    for i in range(n):
        circ = BQFA_in_Sohel(circ, q[4*i+2],q[4*i+1],q[4*i],q[4*i+3],q[4*i+4]) 
        circ.measure(q[4*i+3],c[i])
    circ.measure(q[4*n],c[n])
    return circ

if __name__ == "__main__":
    data_A = "10"
    data_B = "10"    
    Carry_in = '1'
    data_A = data_A[::-1]
    data_B = data_B[::-1]   
    n = len(data_A)
    # initiate 3 qubits
    q = QuantumRegister(4*n+1,'q')
    # initiate 2 traditional bits
    c = ClassicalRegister(n+1,'c')
    #initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # transform custom bit to quantum state vector
    data_string = ''
    data_string += Carry_in
    for i in range(n):
        data_string += data_A[i]
        data_string += data_B[i]
        data_string += '00'
    # data_string = data_string[::-1]
    initial_state = bit2state(data_string)
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = CRA_in_Sohel(circ, q, c, n)
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