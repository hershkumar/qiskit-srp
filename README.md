# Hersh Kumar's SRP code

SRP QISkit programs, written in python, using the qiskit library.

## Programs

### unitary

This is a useful tool for obtaining the unitary matrix of a circuit or set of gates. This can be used to double check the equivalence of two circuits, or to check a circuit design against a matrix.

### timeEvolutionBasic

This time evolves a basic Hamiltonian, which only takes into account the spin in the z direction of two particles (H = sigma_z^1 * sigma_z^2).

### fullHamiltonian

This time evolves the full Heisenberg model Hamiltonian, using Trotterization in order to approximate the correct time evolution on a quantum computer. This does not take into account an external magnetic field when describing/evolving the Hamiltonian.

### Z4GaugeTheory (OUTDATED)

This is an implementation of a Z4 (integers mod 4 under addition) gauge theory, using one plaquette with 2 sites, for a total of 2 links.

### Z4Plot and Z4Sim

These split the Z4 gauge theory into 2 separate files, one that runs the simulation and stores the data into a specified file, and one that plots a desired state via reading a data file. These files should be used instead of Z4GaugeTheory.

#### qasm-10-.05.dat and sv-10-.05.dat

These are 2 premade simulation files, starting from the state 0000 and evolving until time 10, with a time step of .05.
