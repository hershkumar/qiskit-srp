SRP QISkit programs, written in python, using the qiskit library.
# Programs

## unitary
This is a useful tool for obtaining the unitary matrix of a circuit or set of gates. This can be used to double check the equivalence of two circuits, or to check a circuit design against a matrix.
## timeEvolutionBasic
This time evolves a basic Hamiltonian, which only takes into account the spin in the z direction of two particles (H = sigma_z^1 * sigma_z^2).
## fullHamiltonian
This time evolves the full Heisenberg model Hamiltonian, using Trotterization in order to approximate the correct time evolution on a quantum computer. This does not take into account an external magnetic field when describing/evolving the Hamiltonian.
## Z4GaugeTheory
This is an implementation of a Z4 (integers mod 4 under addition) gauge theory, using one plaquette with 2 sites, for a total of 2 links.
