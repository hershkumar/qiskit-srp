# implements a 2 Z4 gauge theory
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.providers.aer import StatevectorSimulator
# sets the state of the qubits to the specified string
def set_state(state):
	state = list(state)
	i = 0
	while (i < num_qubits):
		if (state[i] == '1'):
			circuit.x(q[i])
		i+=1

# number 1 (q1,q2) + number 2 (q3,q4)
def addition_gate(q0,q1,q2,q3):
	circuit.cx(q2,q0)
	circuit.ccx(q3,q1,q0)
	circuit.cx(q3,q1)

# finds the inverse of a group element (the number is stored in q0,q1)
def inverse(q0,q1):
	circuit.cx(q[1],q[0])

# defines the trace circuit
#def trace(q0,q1):


#defines the kinetic term of the hamiltonian as a circuit 
#def kinetic():


# number of sites on the lattice
num_sites = 2
num_qubits = 2 * num_sites
# the initial state the system should be set to 
initial_state = '0000'

q = QuantumRegister(num_qubits)
c = ClassicalRegister(num_qubits)

circuit = QuantumCircuit(q,c)
set_state(initial_state)

circuit.measure(q,c)
simulator = Aer.get_backend('statevector_simulator')
result = execute(circuit,simulator).result()
statevector = result.get_statevector(circuit)
print(statevector)
print(circuit)
