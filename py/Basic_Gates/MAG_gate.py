from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
from init_state import bit2state

def MAG (circ, A, B, C):
    
    '''
    This circuit is MAG gate. If user wants to add a MAG_gate in their circuits,
        they need to pass their circuit and the qubits that will be used in this gate.
    input:
        circ        :       circuit
        A, B, C     :       qubit 
    output:
        circ        :       circuit
    **Example:**

    circ = MAG_gate(circ, A, B, C)
    
    A NG gate is added to the circuit and q[0]-q[3] are used in this gate.
    
    **Circuit symbol:**

    .. parsed-literal::
                     ┌───┐  
          A  ────────┤ X ├────■──── P
              ┌───┐  └─┬─┘    │    
          B  ─┤ X ├────│──────■──── G
              └─┬─┘    │    ┌─┴─┐  
          C  ───■──────■────┤ X ├── Q
                            └───┘  

    **Math:**

    .. math::

        P = C\oplus A
        G = C\oplus B
        Q = ((C\oplus A)(C\oplus B))\oplus C

    '''
    
    circ.cx(C,B)
    circ.cx(C,A)
    circ.ccx(A,B,C)
    return circ

if __name__ == "__main__":
    # initiate 4 qubits
    q = QuantumRegister(3,'q')
    # initiate 2 traditional bits
    c = ClassicalRegister(3,'c')
    # initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # input
    data_A = 1
    data_B = 1
    # transform custom bit to quantum state vector
    initial_state = bit2state(str(data_A)+str(data_B)+'0')
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = MAG(circ, q[0], q[1], q[2])
    circ.measure(q[0], c[0])
    circ.measure(q[1], c[1])
    circ.measure(q[2], c[2])
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
    job_sim = backend.run(circ_compiled, shots=1024)

    # Grab the results from the job.
    result_sim = job_sim.result()
    counts = result_sim.get_counts(circ_compiled)
    print(counts)
