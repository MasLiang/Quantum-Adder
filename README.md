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
  	- sum-first BQFA
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
  	- QMDA_Carry_First:		Qubit-efficient QMDA with carry-first QFAs
  	- MSDF_mixed:			QMDA with qubit-efficient and low T-count optimisations by using temporary logical-AND, carry- and sum-first QFAs
  	- MSDF_Sum_google_mixed:	QMDA with qubit-efficient and low T-count optimisations. 
  	- MSDF_in_Biswas: 		QMDA based on the BQFA proposed in Biswas
  	- MSDF_in_Cuccaro:		QMDA based on the BQFA proposed in Cuccaro
  	- MSDF_in_Google:		QMDA with low-depth and low T-count optimisations by using temporary logical-AND based QFAs
  	- MSDF_in_Islam:		QMDA based on the BQFA proposed in Islam
  	- MSDF_in_Mazumder:		QMDA based on the BQFA proposed in Mazumder
  	- MSDF_in_Sohel:		QMDA based on the BQFA proposed in Sohel 
