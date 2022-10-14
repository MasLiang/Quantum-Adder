from sqrt_root_CNOT_Hermitian_gate import *

def Toffoli_gate(circ, q_c1, q_c2, q_t):
    '''
    This circuit is Toffoli gate. If user wants to add a Toffoli_gate in their circuits,
        they need to pass their circuit and the qubits that will be used in this gate.

    input:
        circ        :       circuit
        q_c1        :       contral qubit 1 
        q_c2        :       contral qubit 2
        q_t         :       target qubit
    output:
        circ        :       circuit
    
    **Example:**

    circ = Toffoli_gate(circ, q[0], q[1], q[2])
    
    A Toffoli gate is added to the circuit and q[0]-q[1] are used in this gate.

    **Circuit symbol:**

    .. parsed-literal::       
             
          q_c1 ───────────■───────■─────────────────■───  P
                          │     ┌─┴─┐             ┌─┴─┐     
          q_c2 ───■───────■─────┤ X ├──────■──────┤ X ├─  Q
                ┌─┴──┐  ┌─┴──┐  └───┘  ┌───┴────┐ └───┘
          q_t  ─┤ √X ├──┤ √X ├─────────┤ (√X)^T ├───────  R
                └────┘  └────┘         └────────┘
        
        i.e.,

          q_c1 ───────────■───────■────────────────────────■───  P
                          │     ┌─┴─┐                    ┌─┴─┐
          q_c2 ───■───────■─────┤ X ├──────────■─────────┤ X ├─  Q
                ┌─┴──┐  ┌─┴──┐  └───┘  ┌────┐  │  ┌────┐ └───┘
          q_t  ─┤ √X ├──┤ √X ├─────────┤  H ├──■──┤ H  ├───────  R
                └────┘  └────┘         └────┘     └────┘

    **Math:**

    .. math::

        P = A
        Q = B
        R = AB\oplus C

    '''
    circ.csx(q_c2, q_t)
    circ.csx(q_c1, q_t)
    circ.cx(q_c1,q_c2)
    circ = sqrt_root_CNOT_Hermitian(circ, q_c2, q_t)
    circ.cx(q_c1,q_c2)
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
    C = 0
    # transform custom bit to quantum state vector
    initial_state = bit2state(str(A)+str(B)+str(C))
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = Toffoli_gate(circ, q[0], q[1], q[2])
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
