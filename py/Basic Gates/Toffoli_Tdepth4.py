from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
from init_state import bit2state

def doubly_controlled_NOT_gate(circ, q, c):
    circ.h(q[6])
    circ.cx(q[1],q[5])
    circ.cx(q[0],q[3])
    circ.cx(q[1],q[4])
    circ.cx(q[2],q[5])
    circ.cx(q[3],q[6])
    circ.cx(q[0],q[4])
    circ.cx(q[2],q[6])
    circ.cx(q[5],q[3])
    circ.t(q[0])
    circ.t(q[1])
    circ.t(q[2])
    circ.t(q[3])
    circ.tdg(q[4])
    circ.tdg(q[5])
    circ.tdg(q[6])
    circ.cx(q[0],q[1])
    circ.cx(q[1],q[2])
    circ.cx(q[2],q[3])
    circ.cx(q[3],q[4])
    circ.cx(q[4],q[5])
    circ.cx(q[5],q[6])
    circ.h(q[6])

    circ.measure(q[0],c[0])
    circ.measure(q[1],c[1])
    circ.measure(q[2],c[2])
    circ.measure(q[3],c[3])
    circ.measure(q[4],c[4])
    circ.measure(q[5],c[5])
    circ.measure(q[6],c[6])
    return circ


def Toffoli(circ, q_A, q_B, q_C, c_A, c_B, c_C):
    '''

    ''' 
    circ.h(q_C)
    circ.cx(q_B,q_C)
    circ.tdg(q_C)
    circ.cx(q_A,q_C)
    circ.t(q_C)
    circ.cx(q_B,q_C)
    circ.tdg(q_B)
    circ.tdg(q_C)
    circ.cx(q_A,q_B)
    circ.cx(q_A,q_C)
    circ.tdg(q_A)
    circ.tdg(q_B)
    circ.t(q_C)
    circ.cx(q_A,q_B)
    circ.s(q_B)
    circ.h(q_C)
    circ.measure(q_A, c_A)
    circ.measure(q_B, c_B)
    circ.measure(q_C, c_C)
    return circ

if __name__ == "__main__":
    # initiate 4 qubits
    q = QuantumRegister(7,'q')
    # initiate 2 traditional bits
    c = ClassicalRegister(7,'c')
    # initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # input
    data_A = 1
    data_B = 1
    data_C = 0
    # transform custom bit to quantum state vector
    initial_state = bit2state(str(data_A)+str(data_B)+str(data_C)+'000'+str(data_C))
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    # circ = Toffoli(circ, q[0], q[1], q[2], c[0], c[1], c[2])
    circ = doubly_controlled_NOT_gate(circ, q, c)
    
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
