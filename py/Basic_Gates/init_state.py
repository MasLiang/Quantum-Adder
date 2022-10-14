import qiskit.quantum_info as qi

def bit2state(input_bit):
    '''
    This is used to transfore classical bit to quantum state of qubit.
    '''
    input_bit = input_bit[::-1]
    # transform custom bit to quantum state vector
    if input_bit[0]=='1':
        state_vector_temp = [0,1]
    else:
        state_vector_temp = [1,0]
    for i in input_bit[1:]:
        state_vector = []
        for j in state_vector_temp:
            if j==0:
                state_vector.append(0)
                state_vector.append(0)
            else:
                if i=='0':
                    state_vector.append(1)
                    state_vector.append(0)
                else:
                    state_vector.append(0)
                    state_vector.append(1)
        state_vector_temp = state_vector
    # transform numpy list to state_vector
    psi = qi.Statevector(state_vector)
    return psi