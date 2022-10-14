# Quantum-Adder
This is a library of quantum adder based on Qiskit platform provided by IBM, including basic quantum gates implementation, binary quantum full adders, quantum carry ripple adder, and quantum most-significant digit-first adders.

# Prerequisites

 - Python 3.7 +
 - pip install -U pip && pip install qiskit

# Content
- basic gates
	- MAG_gate
	- NG_gate
	- Peres_gate
	- Temperary_logical_AND
	- Toffoli gate with T-depth being 4
	- Toffoli_gate
	- Sqrt_root_CNOT_Hermitian_gate
- binary quantum full adder
  	- carry-first BQFA
		There are two structures in this file: using 4 qbits or 3 qubits.
  	- sum-first BQFA
		There are two structures in this file: using 4 qbits or 3 qubits.
  	- BQFA proposed in Biswas
  	- BQFA proposed in Cuccaro
  	- BQFA proposed in Google
  	- BQFA proposed in Islam
  	- BQFA proposed in Mazumder
  	- BQFA proposed in Sohel
- quantum carry ripple adder
	- CAR_in_Islam:			CRA based on BQFA in Islam
	- CRA_in_Biswas:		CRA based on BQFA in Biswas
	- CRA_in_Cuccaro_2cnotversion:	CRA based on BQFA in Cuccaro
	- CRA_in_Google:		CRA based on BQFA in Google
	- CRA_in_Mazumder:		CRA based on BQFA in Mazumder
	- CRA_in_Sohel:			CRA based on NQFA in Sohel
- quantum most-significant digit-first adder
  	- MSDF_Carry_First_4q_deep:	the QMDA based on carry-first BQFA with 4 qubits
  	- MSDF_Carry_first:		the QMDA based on carry-first BQFA with 3 qubits
  	- MSDF_Sum_Carry_google_mixed:	the QMDA with sum- and carry-first BQFA as well as the BQFA proposed in Google
  	- MSDF_Sum_Carry_mixed_4q:	the QMDA with sum- and carry-first BQFA
  	- MSDF_Sum_First_4q:		the QMDA with sum-first BQFA with 4 qubits
  	- MSDF_Sum_first:		the QMDA with sum-first BQFA with 3 qubits
  	- MSDF_Sum_google_mixed:	the QMDA with sum-first BQFA and the BQFA proposed in Google
  	- MSDF_in_Biswas: 		the QMDA based on the BQFA proposed in Biswas
  	- MSDF_in_Cuccaro:		the QMDA based on the BQFA proposed in Cuccaro
  	- MSDF_in_Google:		the QMDA based on the BQFA proposed in Google
  	- MSDF_in_Islam:		the QMDA based on the BQFA proposed in Islam
  	- MSDF_in_Mazumder:		the QMDA based on the BQFA proposed in Mazumder
  	- MSDF_in_Sohel:		the QMDA based on the BQFA proposed in Sohel 
