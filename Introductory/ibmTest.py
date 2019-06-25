
from qiskit.providers.ibmq import least_busy
from qiskit import IBMQ
from qiskit.compiler import transpile, assemble
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.quantum_info import Pauli, state_fidelity, basis_state, process_fidelity 
IBMQ.load_accounts()

small_devices = IBMQ.backends(filters=lambda x: x.configuration().n_qubits == 5 and not x.configuration().simulator)
backend = least_busy(small_devices)

q = QuantumRegister(1)
c = ClassicalRegister(1)

circuit = QuantumCircuit(q,c)
circuit.h(q)
circuit.measure(q,c)
qobj = assemble(transpile(circuit, backend=backend), shots=1024)
job = backend.run(qobj)

result = job.result()
print(result.get_counts())