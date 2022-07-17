from sqrt_root_CNOT_Hermitian_gate import *
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
from init_state import bit2state

def Peres_gate(circ, q_c, q_t1, q_t2):
    '''
    This circuit is Peres gate. If user wants to add a Peres_gate in 
        their circuits, they need to pass their circuit and the qubits 
        that will be used in this gate.
    input:
        circ        :       circuit
        q_c         :       contral qubit 
        q_t1        :       target qubit 1
        q_t2        :       target qubit 2
    output:
        circ        :       circuit
    
    **Example:**

    circ = Peres_gate(circ, q[0], q[1], q[2])
    
    A Peres gate is added to the circuit and q[0]-q[1] are used in 
        this gate.
    
    **Circuit symbol:**

    .. parsed-literal::       
             
          q_c  ───────────■───────■───────────────  P
                          │     ┌─┴─┐                  
          q_t1 ───■───────■─────┤ X ├──────■──────  Q
                ┌─┴──┐  ┌─┴──┐  └───┘  ┌───┴────┐
          q_t2 ─┤ √X ├──┤ √X ├─────────┤ (√X)^T ├─  R
                └────┘  └────┘         └────────┘
        
        i.e.,

          q_c  ───────────■───────■──────────────────────  P
                          │     ┌─┴─┐                  
          q_t1 ───■───────■─────┤ X ├──────────■─────────  Q
                ┌─┴──┐  ┌─┴──┐  └───┘  ┌────┐  │  ┌────┐
          q_t2 ─┤ √X ├──┤ √X ├─────────┤  H ├──■──┤ H  ├─  R
                └────┘  └────┘         └────┘     └────┘

    **Math:**

    .. math::

        P = A
        Q = A\oplus B
        R = AB\oplus C

    '''
    circ.csx(q_t1, q_t2)
    circ.csx(q_c, q_t2)
    circ.cx(q_c,q_t1)
    circ = sqrt_root_CNOT_Hermitian(circ, q_t1, q_t2)
    return circ

if __name__ == "__main__":
    # initiate 3 qubits
    q = QuantumRegister(3,'q')
    # initiate 3 traditional bits
    c = ClassicalRegister(3,'c')
    # initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # input
    A = 1
    B = 1
    C = 1
    # transform custom bit to quantum state vector
    initial_state = bit2state(str(A)+str(B)+str(C))
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = Peres_gate(circ, q[0], q[1], q[2])
    circ.measure(q[0],c[0])
    circ.measure(q[1],c[1])
    circ.measure(q[2],c[2])
    print(circ.draw())

    # Build a simulator to exert the quantum circuit
    backend = QasmSimulator()

    # First we have to transpile the quantum circuit
    # to the low-level QASM instructions used by the
    # backend
    circ_compiled = transpile(circ, backend)

    # Execute the circuit on the qasm simulator.
    # We've set the number of repeats of the circuit
    # to be 1024
    job_sim = backend.run(circ_compiled, shots=1024)

    # Grab the results from the job.
    result_sim = job_sim.result()
    counts = result_sim.get_counts(circ_compiled)
    print(counts)