from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
from init_state import bit2state

def BQFA_Sum_first_left(circ, q_A, q_B, q_C):
    '''
    This circuit is left part of QBFA_Sum_first_4q.
    '''
    circ.cx(q_C,q_A)
    circ.cx(q_B,q_A)
    return circ

def BQFA_Sum_first_right(circ, q_A, q_B, q_C):
    '''
    This circuit is right part of QBFA_Sum_first_4q.
    '''
    circ.cx(q_B,q_A)
    circ.cx(q_C,q_B)
    circ.ccx(q_A,q_B,q_C)
    return circ
    
def BQFA_Sum_first_4q(circ, q_A, q_B, q_C, q_0):
    '''
    This circuit is binary quantum full adder called Sum-first Binary Quantum Full Adder. 
    Besides, it uses four qubits. 

    input:
        circ        :       circuit
        q_A         :       input data A 
        q_B         :       input data B
        q_C         :       input carry 
        q_0         :       auxiliary qubit whose initial state is |0>
    output:
        circ        :       circuit
    
    **Example:**

    circ = BQFA_Sum_first_4q(circ, q[0], q[1], q[2], q[3])
    
    A BQFA_Sum_first_4q is added to the circuit. q[0]-q[2] correspond to input data A,B and input carry. 
        q[3] is initiated as |0>.

    **Circuit symbol:**

    .. parsed-literal::      
                                
                  ┌───┐ ┌───┐      ┌───┐
          q_0: ───┤ X ├─┤ X ├──■───┤ X ├─────────■─────
                  └─┬─┘ └─┬─┘  │   └─┬─┘ ┌───┐   │
          q_1: ─────┼─────■────┼─────■───┤ X ├───■─────
                    │          │         └─┬─┘ ┌─┴─┐
          q_2: ─────■──────────┼───────────■───┤ X ├─── |Carry>
                             ┌─┴─┐             └───┘
          q_3: ──────────────┤ X ├───────────────────── |Sum>
                             └───┘             
                  
    '''
    circ = BQFA_Sum_first_left(circ, q_A, q_B, q_C)
    circ.cx(q_A,q_0)
    circ = BQFA_Sum_first_right(circ, q_A, q_B, q_C)
    return circ

if __name__ == "__main__":
    # initiate 3 qubits
    q = QuantumRegister(4,'q')
    # initiate 2 traditional bits
    c = ClassicalRegister(2,'c')
    # initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # input
    data_A = 0
    data_B = 1
    Carry = 0
    # transform custom bit to quantum state vector
    initial_state = bit2state(str(data_A)+str(data_B)+str(Carry)+'0')
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = BQFA_Sum_first_4q(circ, q[0], q[1], q[2], q[3])
    circ.measure(q[3],c[0])
    circ.measure(q[2],c[1])
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