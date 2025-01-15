from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

import circuit

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg")  # or 'Agg', 'Qt5Agg', etc.


def main():
    simulator = AerSimulator()
    circ = transpile(circuit.build_circuit("11"), simulator)

    result = simulator.run(circ, shots=100).result()
    counts = result.get_counts(circ)

    plot_histogram(counts, title="Superdense coding")
    plt.show()


if __name__ == "__main__":
    main()
