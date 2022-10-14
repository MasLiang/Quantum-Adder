from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
import sys
sys.path.append("..")
from Basic_Gates.init_state import bit2state
from Basic_Gates.NG_gate import *

def BQFA_in_Mazumder(circ, q_A, q_1_1, q_B, q_C, q_0_1, q_0_2, q_1_2):
    '''
    This circuit is binary quantum full adder proposed in (Mazumder. 2008). 
        If user wants to add it in their circuits, they need to pass their 
        circuit and the qubits that will be used in this circuit. 

    input:
        circ        :       circuit
        q_A         :       input data A 
        q_B         :       input data B
        q_C         :       input carry 
        q_0_1       :       auxiliary qubit whose initial state is |0>
        q_0_2       :       auxiliary qubit whose initial state is |0>
        q_1_1       :       auxiliary qubit whose initial state is |1>
        q_1_2       :       auxiliary qubit whose initial state is |1>
    output:
        circ        :       circuit
    
    **Example:**

    circ = BQFA_in_Mazumder(circ, q[0], q[1], q[2], q[3], q[4], q[5], q[6])
    
    A BQFA_in_Mazumder is added to the circuit. q[0]-q[2] correspond to input 
        data A,B and input carry. q[3]-q[6] are initiated as |0> or |1>.

    **Circuit symbol:**

    .. parsed-literal::      
                                
                                         ┌───┐         ┌───┐   
          q_A    ────────────■───────────┤ X ├────■────┤ X ├─────────────────────────────────────────────────────────────────────────────────  garbage
                    ┌───┐    │           └───┘    │    └───┘         ┌───┐                                                                    
          q_1_1  ───┤ X ├────│────────────────────■─────────────■────┤ X ├────x──────────────────────────────────────────────────────────────  |Sum>
                    └─┬─┘    │    ┌───┐           │             │    └───┘    │                         ┌───┐                ┌───┐
          q_B    ─────┤──────■────┤ X ├────x──────│─────────────│─────────────│────────────────────■────┤ X ├───────────x────┤ X ├───────────  garbage
                      │      │    └───┘    │      │           ┌─┴─┐           │    ┌───┐           │    └─┬─┘           │    └─┬─┘
          q_C    ─────│──────│─────────────│──────│──────■────┤ X ├───────────x────┤ X ├───────────│──────│─────────────│──────│─────────────  garbage
                      │    ┌─┴─┐           │    ┌─┴─┐    │    └─┬─┘         ┌───┐  └─┬─┘  ┌───┐    │      │    ┌───┐    │      │
          q_0_1  ─────■────┤ X ├───────────x────┤ X ├────│──────■───────────┤ X ├────■────┤ X ├────│──────■────┤ X ├────x──────│─────────────  |Carry>
                           └───┘                └───┘  ┌─┴─┐                └───┘    │    └───┘    │      │    └───┘  ┌───┐    │     ┌───┐
          q_0_2  ──────────────────────────────────────┤ X ├─────────────────────────■─────────────│──────■───────────┤ X ├────■─────┤ X ├───  garbage
                                                       └───┘                                     ┌─┴─┐                └───┘    │     └───┘
          q_1_2  ────────────────────────────────────────────────────────────────────────────────┤ X ├─────────────────────────■─────────────  garbage
                                                                                                 └───┘ 


    '''
    circ = NG_gate(circ,q_A,q_1_1,q_B,q_0_1)
    circ = NG_gate(circ,q_0_1,q_0_2,q_1_1,q_C)
    circ = NG_gate(circ,q_0_2,q_1_2,q_0_1,q_B)
    return circ

if __name__ == "__main__":
    # initiate 7 qubits
    q = QuantumRegister(7,'q')
    # initiate 2 traditional bits
    c = ClassicalRegister(2,'c')
    # initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # input
    data_A = 1
    data_B = 0
    Carry = 1
    # transform custom bit to quantum state vector
    initial_state = bit2state(str(data_A)+'1'+str(data_B)+str(Carry)+'001')
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = BQFA_in_Mazumder(circ, q[0], q[1], q[2], q[3], q[4], q[5], q[6])
    circ.measure(q[1],c[0])
    circ.measure(q[4],c[1])
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
