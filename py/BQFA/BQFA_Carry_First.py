from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit import transpile
import sys
sys.path.append("..")
from Basic_Gates.init_state import bit2state

def Carry_First_BQFA(circ, q_A, q_B, q_C, q_D, c_Carry=None, c_Sum=None):
    '''
    This circuit is Carry-first binary quantum full adder. If user wants to 
        add it in their circuits, they need to pass their circuit and the 
        qubits & classical regisger that will be used in this circuit. It 
        should be noticed that the Peres gate is replaced by Toffoli gate 
        and CNOT gate.

    input:
        circ        :       circuit
        q_A         :       input data A 
        q_B         :       input data B
        q_C         :       input carry 
        c_Sum       :       classical register. If the "Sum" is measured, the 
                                state will be stored in this register.
        q_D         :       duplicate the "Carry" to this qubit
        c_Carry     :       classical register. If the "Carry" is measured, 
                                the state will be stored in this register
    output:
        circ        :       circuit
    
    **Example:**
    
    circ = Carry_First_BQFA(circ, q[0], q[1], q[2], q_D=q[3])

    A Carry_First_BQFA is added to the circuit. q[0]-q[2] correspond to input 
        data A,B and input carry. The "Sum" and "Carry" are going to be uesd 
        in other circuit. Thus, they are not measured. As a result, there is 
        no need to used classical registers.

    **Circuit symbol:**
                                
                        ┌───┐  ┌───────┐         ┌───────┐           ┌───┐ 
          q_A  ─────────┤ X ├──┤       ├─────────┤       ├───────────┤ X ├──  |Sum>
                 ┌───┐  └─┬─┘  │       │         │       │    ┌───┐  └─┬─┘
          q_B  ──┤ X ├────│────┤ Peres ├─────────┤ Peres ├────┤ X ├────│────
                 └─┬─┘    │    │ Gate  │ |Carry> │ Gate  │    └─┬─┘    │   
          q_C  ────■──────■────┤       ├────■────┤       ├──────■──────■────
                               └───────┘  ┌─┴─┐  └───────┘    
          q_D  ───────────────────────────┤ X ├─────────────────────────────
                                          └───┘

    ''' 
    circ.cx(q_C,q_B)
    circ.cx(q_C,q_A)
    circ.ccx(q_A,q_B,q_C)
    circ.cx(q_A,q_B)
    circ.cx(q_C,q_D)
    circ.cx(q_A,q_B)
    circ.ccx(q_A,q_B,q_C)
    circ.cx(q_C,q_B)
    circ.cx(q_B,q_A)
    if c_Sum!=None:
        circ.measure(q_A,c_Sum)
    return circ

if __name__ == "__main__":
    # initiate 4 qubits
    q = QuantumRegister(4,'q')
    # initiate 2 traditional bits
    c = ClassicalRegister(2,'c')
    # initiate quantum circuit
    circ = QuantumCircuit(q,c)
    # input
    data_A = 1
    data_B = 1
    Carry = 1
    # transform custom bit to quantum state vector
    initial_state = bit2state(str(data_A)+str(data_B)+str(Carry)+'0')
    # initial input qubit state
    circ.set_statevector(initial_state)
    # build the quantum circuit
    circ = Carry_First_BQFA(circ, q[0], q[1], q[2], q[3])
    circ.measure(q[0],c[0])
    circ.measure(q[3],c[1])
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
