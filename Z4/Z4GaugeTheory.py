# implements a 2 Z4 gauge theory
# uses 1 plaquette, with n sites
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.providers.aer import StatevectorSimulator
links = []
data = []
#*----------------------------------*#
#* MODIFIABLE VARIABLES

# number of sites on the plaquette
#* currently this variable is not used by anything because the number of sites doesn't really matter 
#* until you enact a gauge transformation
num_sites = 2
# the number of total links between sites
num_links = 2
# the number of ancilary qubits that we are using
num_ancillary = 2
# chooses whether or not to use the qasm_simulator or the statevector simulator
# either "qasm" or "sv"
backend = "qasm"
# the initial state the system should be set to 
#! this does not do anything because the set_state function is broken
initial_state = '000000'

#*----------------------------------*#

# checks to make sure that you picked one of the right two variables
if (backend != "qasm" and backend != "sv"):
    print("Please choose either \"qasm\" or \"sv\" for the backend variable. ")
# sets the state of the qubits to the specified string
# TODO: figure out why this function is broken
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
    circuit.crz(-pi/2,q1,q3)
    circuit.crz(pi,q1,q2)
    circuit.crz(pi,q0,q3)
# finds the inverse of a group element (the number is stored in q0,q1)
def inverse(q0,q1):
    circuit.cx(q[1],q[0])


# figure out the number of qubits necessary for the registers
num_qubits = 2 * num_links + num_ancillary

#initialize qubit registers
q = QuantumRegister(num_qubits)
c = ClassicalRegister(num_qubits)

circuit = QuantumCircuit(q,c)

"""
TODO: The actual code that should go here:
 1. start from gauge invariant state
 2. time evolve
 3. make sure that the ending state is also gauge invariant
"""

circuit.measure(q,c)
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

# reverse the ordering of the qubits for readability
for i in data:
    for key in i:
        key = key[::-1]
        print(data)