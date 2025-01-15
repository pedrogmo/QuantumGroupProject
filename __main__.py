from qiskit import transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

import circuit

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg")  # or 'Agg', 'Qt5Agg', etc.


def main():
    message = "100011"
    print(f"The message {message} will be sent using superdense coding.")

    # Define and draw the circuit
    circ = circuit.build_circuit(message)
    circ.draw(output="mpl")
    plt.show()

    # Define the simulator and simulate the circuit
    simulator = AerSimulator()
    circ = transpile(circ, simulator)
    result = simulator.run(circ, shots=1, memory=True).result()

    # Print the last result of the simulation
    memory = result.get_memory(circ)
    message_result = memory[-1]
    print(f"The message {message_result} has been received.")

    # Plot the results of the simulation
    # counts = result.get_counts(circ)
    # plot_histogram(counts, title="Superdense coding")
    # plt.show()


if __name__ == "__main__":
    main()
