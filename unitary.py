import numpy as np
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute

q = QuantumRegister(1)
c = ClassicalRegister(1)
circ = QuantumCircuit(q,c)
circ.h(0)
circ.rz(pi,0)
circ.h(0)

simulator = Aer.get_backend('unitary_simulator')


result = execute(circ, simulator).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)
