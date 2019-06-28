# implements a 2 Z4 gauge theory
# uses 1 plaquette, with n sites
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.providers.aer import StatevectorSimulator
links = []
qubits = []
data = []
#*----------------------------------*#
# number of sites on the plaquette
#! currently this variable is not used by anything
num_sites = 2
# the number of links
num_links = 2
# the number of ancillary qubits that we are using
num_ancilla = 2
# chooses whether or not to use the qasm_simulator or the statevector simulator
# either "qasm" or "sv"
backend = "qasm"
# the initial state the system should be set to
initial_state = '000000'
# chooses whether or not to measure all qubits, rather than just non-ancillary qubits
measure_ancilla = False
#*----------------------------------*#

# checks to make sure that you picked one of the right two variables
if (backend != "qasm" and backend != "sv"):
    print("Please choose either \"qasm\" or \"sv\" for the backend variable. ")
# sets the state of the qubits to the specified string
def set_state(state):
    state = list(state)
    i = 0
    while (i < num_qubits):
        if (state[i] == '1'):
            circuit.x(q[i])
        i+=1

# element 1 (q1,q2) + element 2 (q3,q4)
def multiplication(q0,q1,q2,q3):
    circuit.cx(q2,q0)
    circuit.ccx(q3,q1,q0)
    circuit.cx(q3,q1)

# defines the trace circuit
def trace(q0,q1):
    circuit.x(q0)
    circuit.crz(pi/2,q0,q1)
    circuit.x(q0)

#defines the kinetic term of the hamiltonian as a circuit 
#inputs:
# q0 and q1 are the 2 qubits that hold the group element
# q2 and q3 are the 2 ancillary qubits
def kinetic(q0,q1,q2,q3):
    circuit.h(q2)
    circuit.h(q3)
    circuit.crz(pi/2,q1,q3)
    circuit.crz(pi,q1,q2)
    circuit.crz(pi,q0,q3)
    circuit.rzz(pi/2,q2,q3)
    circuit.crz(pi,q0,q3)
    circuit.crz(pi,q1,q2)
    circuit.crz(-pi/2,q1,q3)
# finds the inverse of a group element (the number is stored in q0,q1)
def inverse(q0,q1):
    circuit.cx(q[1],q[0])


# figure out the number of qubits necessary for the registers
num_qubits = 2 * num_links + num_ancilla

#initialize qubit registers
q = QuantumRegister(num_qubits)
c = ClassicalRegister(num_qubits)
# initialize the list qubits with only the useful qubits (no ancilla)
i = 0 
while (i < (num_qubits - num_ancilla)):
    qubits.append(q[i])
    i += 1

# initialize links with all the paired links
for i,k in zip(qubits[0::2], qubits[1::2]):
    links.append((i,k))
    
#* actual circuit starts here
# initializes the quantum circuit
circuit = QuantumCircuit(q,c)
# places the 4 qubits into a gauge invariant state using Hadamards
for i in qubits:
    circuit.h(i)

# kinetic portion of the circuit
for pair in links:
    kinetic(pair[0],pair[1],q[4],q[5])

# potential portion of the circuit
multiplication(q[0],q[1],q[2],q[3])
trace(q[0],q[1])
inverse(q[2],q[3])
multiplication(q[0],q[1],q[2],q[3])
inverse(q[2],q[3])



if (measure_ancilla == True):
    # measures all qubits (including ancilla)
    circuit.measure(q,c)
else:
    # measures all the actual qubits, but not the ancilla
    circuit.measure(qubits,c[:4])

# draw the circuit in a pdf file
circuit.draw(output="latex", filename="Z4Circuit.pdf")
# use either the statevector simulator or the qasm simulator based on 
# the backend variable
if (backend == "sv"):
    print("Using backend: \'statevector_simulator\'")
    simulator = Aer.get_backend('statevector_simulator')
    result = execute(circuit,simulator).result()
    statevector = result.get_statevector(circuit)
    print(statevector)
elif (backend == "qasm"):
    print("Using backend: \'qasm_simulator\'")
    num_shots = 100
    job = execute(circuit,backend = Aer.get_backend('qasm_simulator'),shots = num_shots)
    result = job.result()
    results = result.get_counts(circuit)
    # place the resulting dictionary in the data list
    data.append(results)

print(data)