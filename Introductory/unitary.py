import numpy as np
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute

q = QuantumRegister(2)
c = ClassicalRegister(2)
circuit = QuantumCircuit(q,c)

# xnor gate 
#circuit.x(0)
#circuit.cx(0,1)
#circuit.cx(1,2)

# double feynman gate
#circuit.cx(0,1)
#circuit.cx(0,2)

# square root of not gate
#circuit.cx(0,1)
#circuit.h(1)
#circuit.rz(pi,1)
#circuit.h(1)
#circuit.cx(0,1)

#csqx
#circuit.h(1)
#circuit.crz(pi,0,1)
#circuit.h(1)


simulator = Aer.get_backend('unitary_simulator')


result = execute(circuit, simulator).result()
unitary = result.get_unitary(circuit)
print("Circuit unitary:\n", unitary)
circuit.draw(output="latex", filename="unitary.pdf")