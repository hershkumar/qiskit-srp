# This code time evolves the full Heisenberg spin chain model on n qubits, and plots the probability 
# of obtaining a certain state for varying lengths of time evolution
from math import pi
import matplotlib.pyplot as plt
import numpy as np
from qiskit import (Aer, ClassicalRegister, QuantumCircuit, QuantumRegister,
                    execute)
# number of qubits that we are running the time evolution on
num_qubits = 4
q = QuantumRegister(num_qubits)
c = ClassicalRegister(num_qubits)
x = []
y = []
default = '0' * num_qubits
# How long should each trotterized gate set be run for?
dt = .05
# which state do we want to graph the probability of
# use default to get the '000...' case
desired_state = '0000'

# gets the pairs of qubits that we need 
qubit_list = list(range(0,num_qubits))
zipped = list(zip(qubit_list, qubit_list[1:] + qubit_list[:1]))

max_time = 10


n = 0
# the maximum
n_limit = 10

while (n <= n_limit):
	circuit = QuantumCircuit(q,c)
	
	x.append(n*dt)
	count = 0
	while (count < n):
		# gates for the Rxx portion of the hamiltonian
		for i in qubit_list:
			circuit.h(i)

		for i in zipped:
			q1 = i[0]
			q2 = i[1]
			circuit.rzz(dt,q1,q2)

		for i in qubit_list:
			circuit.h(i)

		# gates for the Ryy portion of the hamiltonian
		for i in qubit_list:
			circuit.rx(pi/2,i)
		
		for i in zipped:
			q1 = i[0]
			q2 = i[1]
			circuit.rzz(dt,q1,q2)

		for i in qubit_list:
			circuit.rx(-pi/2,i)

		# gates for the Rzz portion of the Hamiltonian
		
		for i in zipped:
			q1 = i[0]
			q2 = i[1]
			circuit.rzz(dt,q1,q2)

		count += 1


	circuit.measure(q,c)
	num_shots = 100
	job = execute(circuit,backend = Aer.get_backend('qasm_simulator'),shots = num_shots)
	result = job.result()
	results = result.get_counts(circuit)
	print(results)
	if (desired_state in results):
		num = results[desired_state]
		prob = num / num_shots
	else:
		prob = 0
	y.append(prob)
	n += 1
#plot the probability of the desired gate
plt.plot(x,y)
plt.ylabel('Probability of ' + desired_state)
plt.xlabel('Time')
plt.title('Time vs. Probability of ' + desired_state)
plt.ylim([-.2,1.2])
plt.show()
