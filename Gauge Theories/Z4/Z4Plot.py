import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pickle

def initialize(backend, filename):
    x = []
    ys = []
    with open(filename, "rb") as infile:
        raw_data = pickle.load(infile)
    if backend == 'sv':
        for vector in raw_data:
            x.append(vector[0])
            ys.append(vector[1:])
        return (x, ys)
    if backend == 'qasm':
        for dic in raw_data:
            x.append(dic['time'])
        return (x, raw_data)

# plot a single state of the system
def plot(backend, filename, desired_state='0000'):
    (x, ys) = initialize(backend, filename)
    y = []
    # statevector simulator
    if backend == 'sv':
        index = int(desired_state, 2)
        for vector in ys:
            element = vector[index]
            prob = (element * element.conjugate()).real
            y.append(prob)
    # qasm simulator
    if backend == 'qasm':
        for dic in ys:
            num_shots = sum(dic.values())
            prob = 0
            if desired_state in dic:
                prob = dic[desired_state]/num_shots
            y.append(prob)
    plt.plot(x, y)
    # labels and legend for the plot
    plt.ylabel('Probability of ' + desired_state)
    plt.xlabel('Time')
    plt.title('Time vs. Probability of ' + desired_state)
    # shows the plot
    plt.show()