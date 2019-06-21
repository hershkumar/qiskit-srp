import numpy as np
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.providers.aer import StatevectorSimulator
num_qubits = 4
q = QuantumRegister(num_qubits)
c = ClassicalRegister(num_qubits)


circuit = QuantumCircuit(q,c)
simulator = Aer.get_backend('statevector_simulator')
result = execute(circuit,simulator).result()
statevector = result.get_statevector(circuit)