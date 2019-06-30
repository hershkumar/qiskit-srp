
import numpy as np
import pickle
import os
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.providers.aer import StatevectorSimulator



def initialization(num_links, num_ancilla, t_final, dt):
    # figure out the number of qubits necessary for the registers
    num_qubits = 2 * num_links + num_ancilla

    #initialize qubit registers
    q = QuantumRegister(num_qubits)
    c = ClassicalRegister(num_qubits)
    # initialize the list qubits with only the useful qubits (no ancilla)
    i = 0
    qubits = []
    while (i < (num_qubits - num_ancilla)):
        qubits.append(q[i])
        i += 1

    # initialize links with all the paired links
    links = []
    for i,k in zip(qubits[0::2], qubits[1::2]):
        links.append((i, k))

    # q, c, qubits, links
    return (q, c, qubits, links)


# GATE DEFINITIONS -----------------------------------
# element 1 (q1,q2) + element 2 (q3,q4)
def multiplication(circuit, q0, q1, q2, q3):
    circuit.cx(q2, q0)
    circuit.ccx(q3, q1, q0)
    circuit.cx(q3, q1)

# defines the trace circuit
def trace(circuit, dt, q0, q1):
    circuit.x(q0)
    circuit.crz(dt, q0, q1)
    circuit.x(q0)

#defines the kinetic term of the hamiltonian as a circuit
# q0 and q1 are the 2 qubits that hold the group element
# q2 and q3 are the 2 ancillary qubits
def kinetic(circuit, dt, q0, q1, q2, q3):
    circuit.h(q2)
    circuit.h(q3)
    circuit.crz(pi/2, q1, q3)
    circuit.crz(pi, q1, q2)
    circuit.crz(pi, q0, q3)

    circuit.rzz(dt, q2, q3)

    circuit.crz(pi, q0, q3)
    circuit.crz(pi, q1, q2)
    circuit.crz(-pi/2, q1, q3)

# finds the inverse of a group element (the number is stored in q0, q1)
def inverse(circuit, q0, q1):
    circuit.cx(q1, q0)

# sv sim
def sv_sim(num_links, num_ancilla, t_final, dt, output_file, initial_state):
    (q, c, qubits, links) = initialization(num_links, num_ancilla, t_final, dt)
    # the maximum number of times that we append the circuit
    n_max = t_final / dt
    out_list = []
    n = 0
    print(n_max)
    while (n <= n_max):
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
                kinetic(circuit, dt, pair[0], pair[1], q[4], q[5])

            # potential portion of the circuit
            multiplication(circuit, q[0], q[1], q[2], q[3])
            trace(circuit, dt, q[0], q[1])
            inverse(circuit, q[2], q[3])
            multiplication(circuit, q[0], q[1], q[2], q[3])
            inverse(circuit, q[2], q[3])

            count += 1
        # use either the statevector simulator or the qasm simulator based on the backend variable
        os.system( 'cls' )
        percent = int((n+1) / n_max * 100)
        print(f"Executing run {repr(n+1)} of {repr(int(n_max))}: ({repr(percent)}%) done.")
        simulator = Aer.get_backend('statevector_simulator')
        result = execute(circuit,simulator).result()
        statevector = result.get_statevector(circuit)
        out_list.append(np.insert(statevector, 0, n * dt))
        n += 1
    # write out_list to output_file here
    print(f"Writing state vector to {output_file} ...")
    with open(output_file, "wb") as out:
        pickle.dump(out_list, out)
        #out.write(str(out_list))
    print("Done!")

# qasm sim TODO
#def qasm_sim():

# run either a qasm or sv simulation
def run_sim(backend, num_links, num_ancilla, t_final, dt, output_file='', initial_state='000000'):
    if output_file == '':
        output_file = 'z4' + backend + 'data.dat'
    # TODO: only sv for now
    sv_sim(num_links, num_ancilla, t_final, dt, output_file, initial_state)
