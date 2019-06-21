from qiskit import IBMQ
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.quantum_info import Pauli, state_fidelity, basis_state, process_fidelity 
#IBMQ.load_accounts()

#define registers (the quantum and classical systems)
q = QuantumRegister(1)
c = ClassicalRegister(1)
# initialize the circuit
circuit = QuantumCircuit(q,c)

# add gates
circuit.h(q)

# finish the circuit
circuit.measure(q,c)
num_shots = 1024
job = execute(circuit,backend = Aer.get_backend('qasm_simulator'),shots = num_shots)
result = job.result()
# output the results
print(result.get_counts(circuit))
#parsing percentages
output = result.get_counts(circuit)
num_zeros = output['0']
percentage = 100 * (num_zeros/num_shots)
#round and print percent
print(str(round(percentage , 2)) + "% are 0's.")
print(str(round(100 - percentage,2)) + "% are 1's.")