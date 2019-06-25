import numpy as np
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute

q = QuantumRegister(4)
c = ClassicalRegister(4)
circuit = QuantumCircuit(q,c)

circuit.h(2)
circuit.h(3)
circuit.crz(pi/2,1,3)
circuit.crz(pi,1,2)
circuit.crz(pi,0,3)
circuit.rzz(pi/2,2,3)
circuit.crz(-pi/2,1,3)
circuit.crz(pi,1,2)
circuit.crz(pi,0,3)

simulator = Aer.get_backend('unitary_simulator')


result = execute(circuit, simulator).result()
unitary = result.get_unitary(circuit)
print("Circuit unitary:\n", unitary)
print(circuit)