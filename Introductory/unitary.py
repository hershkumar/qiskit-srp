import numpy as np
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute

q = QuantumRegister(3)
c = ClassicalRegister(3)
circuit = QuantumCircuit(q,c)

# xnor gate 
#circuit.x(0)
#circuit.cx(0,1)
#circuit.cx(1,2)

simulator = Aer.get_backend('unitary_simulator')


result = execute(circuit, simulator).result()
unitary = result.get_unitary(circuit)
print("Circuit unitary:\n", unitary)
circuit.draw(output="latex", filename="unitary.pdf")