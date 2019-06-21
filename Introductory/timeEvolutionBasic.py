import numpy as np
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute

# this is for the hamiltonian H = sigma_x^1 sigma_x^2
q = QuantumRegister(2)
c = ClassicalRegister(2)
i = 0
timestep = pi/16
x = []
y = []
while (i < 100):
	circuit = QuantumCircuit(q,c)
	# add gates that get you the x
	x.append(i*timestep)
	circuit.h(0)
	circuit.h(1)
	circuit.rzz(i*timestep,0,1)
	circuit.h(0)
	circuit.h(1)

	

	circuit.measure(q,c)

	num_shots = 2048
	job = execute(circuit,backend = Aer.get_backend('qasm_simulator'),shots = num_shots)
	result = job.result()
	# output the results 

	results = result.get_counts(circuit)
	print(results)
	if (("00" in results) and ("11" in results)):
		prob = results['11']/num_shots
	elif ("11" in results):
		prob = 1
	else:
		prob = 0
	y.append(prob)
	i+= 1
#print(circuit)
plt.plot(x,y)
plt.ylabel('Probability of 11')
plt.xlabel('Time')
plt.title('Time vs. Probability of 11')
plt.show()