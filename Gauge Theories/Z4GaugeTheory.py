# implements a 2 Z4 gauge theory
# uses 1 plaquette, with n sites
import numpy as np
import os
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.providers.aer import StatevectorSimulator
links = []
qubits = []
desired_states = []
data = []
x = []
ys = [[], [], [], []]
y_sum = []
#*----------------------------------*#
# the number of links
num_links = 2
# the number of ancillary qubits that we are using
num_ancilla = 2
# chooses whether or not to use the qasm_simulator or the statevector simulator
# either "qasm" or "sv"
backend = "sv"
# the initial state the system should be set to
initial_state = '000000'
# chooses whether or not to measure all qubits, rather than just non-ancillary qubits
measure_ancilla = False
# the final time that we want to evolve for
t_final = 10
# the timestep
dt = .1
# which state do you want to plot?
desired_state = '111111'
desired_state_no_ancilla = '1111'
#*----------------------------------*#
if (backend=="sv"):
    desired_states.append('00' + desired_state_no_ancilla)
    desired_states.append('01' + desired_state_no_ancilla)
    desired_states.append('10' + desired_state_no_ancilla)
    desired_states.append('11' + desired_state_no_ancilla)
    # which element of the statevector do you want?
    counter = 0
    while (counter < len(desired_states)):
        desired_states[counter] = int(desired_states[counter],2)
        counter += 1
# the maximum number of times that we append the circuit
n_max = t_final / dt
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
    circuit.crz(dt,q0,q1)
    circuit.x(q0)

#defines the kinetic term of the hamiltonian as a circuit
# q0 and q1 are the 2 qubits that hold the group element
# q2 and q3 are the 2 ancillary qubits
def kinetic(q0,q1,q2,q3):
    circuit.h(q2)
    circuit.h(q3)
    circuit.crz(pi/2,q1,q3)
    circuit.crz(pi,q1,q2)
    circuit.crz(pi,q0,q3)

    circuit.rzz(dt,q2,q3)

    circuit.crz(pi,q0,q3)
    circuit.crz(pi,q1,q2)
    circuit.crz(-pi/2,q1,q3)
# finds the inverse of a group element (the number is stored in q0,q1)
def inverse(q0, q1):
    circuit.cx(q1, q0)


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

#* actual time evolution starts here
print("Beginning time evolution")
n = 0
while (n < n_max):
    x.append(n*dt)
    count = 0
    # initializes the quantum circuit
    circuit = QuantumCircuit(q,c)
    # places the 4 qubits into a gauge invariant state using Hadamards
    for i in qubits:
        circuit.h(i)
    # starts appending the gates
    while (count < n):

        # kinetic portion of the circuit
        for pair in links:
            kinetic(pair[0],pair[1],q[4],q[5])

        # potential portion of the circuit
        multiplication(q[0],q[1],q[2],q[3])
        trace(q[0],q[1])
        inverse(q[2],q[3])
        multiplication(q[0],q[1],q[2],q[3])
        inverse(q[2],q[3])

        count += 1
    if (backend == "qasm" and measure_ancilla == True):
        circuit.measure(q,c)
    if (backend == "qasm" and measure_ancilla == False):
        circuit.measure(qubits,c[:4])
    # use either the statevector simulator or the qasm simulator based on the backend variable
    if (backend == "sv"):
        os.system( 'cls' )
        percent = int((n+1)/(t_final/dt)*100)
        print("executing run " + str(n+1) +" of "+ str(int(t_final/dt)) + " ("+ str(percent) +"%)")
        simulator = Aer.get_backend('statevector_simulator')
        result = execute(circuit,simulator).result()
        statevector = result.get_statevector(circuit)

        # get all 4 states with last four qubits in state 1111
        # there are 4 due to the 2 ancillary qubits (00,01...)
        elements = [statevector[desired_states[i]] for i in [0, 1, 2, 3]]
        # get the probabilities of these states
        probs = [(element * element.conjugate()).real for element in elements]
        # append the right probability to the correct plotted list
        i = 0
        while (i < len(ys)):
            ys[i].append(probs[i])
            i += 1
        # append all the probabilities to the sum list y_sum
        y_sum.append(sum(probs))
    elif (backend == "qasm"):
        os.system( 'cls' )
        # calculate the percent of runs completed
        percent = int((n+1)/(t_final/dt)*100)
        print("executing run " + str(n+1) +" of "+ str(int(t_final/dt)) + " ("+ str(percent) +"%)")
        num_shots = 100
        job = execute(circuit,backend = Aer.get_backend('qasm_simulator'),shots = num_shots)
        result = job.result()
        results = result.get_counts(circuit)
        #! fix this
        if (desired_state in results):
            num = results[desired_state]
            prob = num / num_shots
        else:
            prob = 0
        y.append(prob)

    n += 1
#plot the probability of the desired gate
for i in range(len(ys)):
    plt.plot(x, ys[i], ['r','g','b','c'][i], label = format(i, 'b'))
#plots the sum of all 4 probabilities
plt.plot(x,y_sum,'m',label='total')
# labels and legend for the plot
plt.ylabel('Probability of ' + desired_state)
plt.xlabel('Time')
plt.legend(loc='upper left')
plt.title('Time vs. Probability of ' + desired_state)
plt.ylim([-.2,1.2])
# shows the plot
plt.show()
print("plot drawn")

# draw the circuit in a pdf file
#! this is broken because the circuit is too long
#! I dont think that there is any way around this issue, without drawing an intermediate circuit diagram
#circuit.draw(output="latex", filename="Z4Circuit.pdf")
