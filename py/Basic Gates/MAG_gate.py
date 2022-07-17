def MAG(circ,q[0],q[1],q[2]):
    circ.cx(q[2],q[1])
    circ.cx(q[2],q[0])
    circ.ccx(q[0],q[1],q[2])
    return circ