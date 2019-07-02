import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pickle

# TODO the lattice geometry is hardcoded -- this should be changed, but probably won't be

def initialize(backend, filename):
    if backend == 'sv':
        x = []
        ys = []
        with open(filename, "rb") as infile:
            raw_data = pickle.load(infile)
        # read the time and the full 64-component state vector
        for arr in raw_data:
            x.append(arr[0])
            ys.append(arr[1:])
        return (x, ys)
    if backend == 'qasm':
        x = []
        ys = []
        with open(filename, "rb") as infile:
            raw_data = pickle.load(infile)
        for dic in raw_data:
            x.append(dic['time'])
            del dic['time']
            ys.append(dic)
        return (x,ys)
def plot(backend, filename, desired_state = '0000'):
    # populate simulation data from a file
    (x, ys) = initialize(backend, filename)
    if backend == 'sv':
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

        # plot all the probabilities that we want
        for i in range(4):
            plt.plot(x, probs[i], colors[i], label = prefixes[i])
        # labels and legend for the plot
        plt.ylabel('Probability of ' + desired_state)
        plt.xlabel('Time')
        plt.legend(loc='upper left')
        plt.title('Time vs. Probability of ' + desired_state)
        # shows the plot
        plt.show()
    if backend == 'qasm':
        y_plot = []
        # TODO add qasm plotting capabilities
        for dic in ys:
            num_shots = sum(dic.values())
            prob = 0
            if desired_state in dic:
                prob = dic[desired_state]/num_shots
            y_plot.append(prob)
        plt.plot(x, y_plot)
        # labels and legend for the plot
        plt.ylabel('Probability of ' + desired_state)
        plt.xlabel('Time')
        plt.legend(loc='upper left')
        plt.title('Time vs. Probability of ' + desired_state)
        # shows the plot
        plt.show()
# TODO: this is broken

def plotAll(filename):
    for i in range(16):
        state_curr = format(i,'b')
        plot(filename,state_curr)