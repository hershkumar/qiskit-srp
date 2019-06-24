import numpy as np
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute

q = QuantumRegister(2)
c = ClassicalRegister(2)
circ = QuantumCircuit(q,c)
circ.crz(pi,0,1)

simulator = Aer.get_backend('unitary_simulator')


result = execute(circ, simulator).result()
unitary = result.get_unitary(circ)
print("Circuit unitary:\n", unitary)
