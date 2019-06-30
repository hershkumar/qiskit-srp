import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pickle

# TODO the lattice geometry is hardcoded -- this should be changed

def initialize(filename):
    x = []
    ys = []
    with open(filename, "rb") as infile:
        raw_data = pickle.load(infile)
    # read the time and the full 64-component state vector
    for arr in raw_data:
        x.append(arr[0])
        ys.append(arr[1:])
    return (x, ys)


def plot(filename, desired_state = '0000'):
    # populate simulation data from a file
    (x, ys) = initialize(filename)
    # get the base colors supported by matplotlib
    colors = [c for c in mcolors.BASE_COLORS]
    # all possible values for the ancillary qubits
    prefixes = ['00', '01', '10', '11']
    desired_ys = [(prefix + desired_state) for prefix in prefixes]
    probs = [[], [], [], []]
    for statevector in ys:
        for state in range(len(desired_ys)):
            element = statevector[int(desired_ys[state], 2)]
            prob = (element * element.conjugate()).real
            probs[state].append(prob)


    for i in range(4):
        plt.plot(x, probs[i], colors[i], label = prefixes[i])
    # labels and legend for the plot
    plt.ylabel('Probability of ' + desired_state)
    plt.xlabel('Time')
    plt.legend(loc='upper left')
    plt.title('Time vs. Probability of ' + desired_state)
    # shows the plot
    plt.show()

def plotAll(filename):
    for i in range(16):
        state_curr = format(i,'b')
        plot(filename,state_curr)