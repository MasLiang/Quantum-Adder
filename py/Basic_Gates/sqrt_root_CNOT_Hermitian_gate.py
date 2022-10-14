from math import pi
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
from Basic_Gates.init_state import bit2state

def sqrt_root_CNOT_Hermitian(circ, q_c, q_t):
    '''
    This circuit is hermitian of sqrt root CNOT gate. If user wants 
        to add it in their circuits, they need to pass their circuit 
        and the qubits that will be used in this gate.
    input:
        circ:   circuit
        q_c :   contral qubit
        q_t :   target qubit
    output:
        circ:   circuit
    
    **Example:**

    circ = sqrt_root_CNOT_Hermitian(circ, q[0], q[1])
    
    A hermitian of sqrt root CNOT gate is added to the circuit and 
        q[0], q[1] are used in this gate.

    **Circuit symbol:**

    .. parsed-literal::

        q_0: ──────────■──────────
              ┌────┐   │   ┌────┐
        q_1: ─┤  H ├───■───┤ H  ├─
              └────┘       └────┘

    **Matrix representation:**

    .. math::

        C\sqrt{X} \ q_c, q_t =
        I \otimes |0 \rangle\langle 0| + {\sqrt{X}}^{\dagger} \otimes |1 \rangle\langle 1|  =
            \begin{pmatrix}
                1   &       0           & 0 &       0       \\
                0   &   (1 - i) / 2     & 0 &   (1 + i) / 2 \\
                0   &       0           & 1 &       0       \\
                0   &   (1 + i) / 2     & 0 &   (1 - i) / 2
            \end{pmatrix}

    '''
    circ.h(q_t)
    circ.cp(-pi/2, q_c,q_t)
    circ.h(q_t)
    return circ

if __name__ == "__main__":
    # initiate 2 qubits
    q = QuantumRegister(2,'q')
    # initiate 2 traditional bits
    c = ClassicalRegister(2,'c')
    # initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # input
    A = 0
    B = 1
    # transform custom bit to quantum state vector
    initial_state = bit2state(str(A)+str(B))
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = sqrt_root_CNOT_Hermitian(circ, q[0], q[1])
    circ.measure(q[0],c[0])
    circ.measure(q[1],c[1])
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

