from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
from init_state import bit2state

def NG_gate(circ, A, B, C, D):
    '''
    This circuit is NG gate. If user wants to add a NG_gate in their circuits,
        they need to pass their circuit and the qubits that will be used in this gate.
    input:
        circ        :       circuit
        A, B, C, D  :       qubit 
    output:
        circ        :       circuit
    **Example:**

    circ = NG_gate(circ, q[0], q[1], q[2], q[3])
    
    A NG gate is added to the circuit and q[0]-q[3] are used in this gate.
    
    **Circuit symbol:**

    .. parsed-literal::
                                          ┌───┐         ┌───┐
          A  ──────────■──────────────────┤ X ├────■────┤ X ├─  P
              ┌───┐    │                  └───┘    │    └───┘
          D  ─┤ X ├────│───────────────────────────■──────────  G
              └─┬─┘    │    ┌───┐                  │
          B  ───│──────■────┤ X ├────x─────────────│──────────  Q
                │    ┌─┴─┐  └───┘    │           ┌─┴─┐
          C  ───■────┤ X ├───────────x───────────┤ X ├────────  R
                     └───┘                       └───┘

    **Math:**

    .. math::

        P = A
        G = C\oplus D
        Q = AB\oplus C
        R = A'(C\oplus D)\oplus B'

    '''
    circ.cx(D,B)
    circ.ccx(A,C,D)
    circ.x(C)
    circ.swap(C,D)
    circ.x(A)
    circ.ccx(A,B,D)
    circ.x(A)
    return circ

if __name__ == "__main__":
    # initiate 4 qubits
    q = QuantumRegister(4,'q')
    # initiate 4 traditional bits
    c = ClassicalRegister(4,'c')
    # initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # input
    A = 0
    B = 1
    C = 1
    D = 0
    # transform custom bit to quantum state vector
    initial_state = bit2state(str(A)+str(B)+str(C)+str(D))
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = NG_gate(circ, q[0], q[1], q[2], q[3])
    circ.measure(q[0],c[0])
    circ.measure(q[1],c[1])
    circ.measure(q[2],c[2])
    circ.measure(q[3],c[3])
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