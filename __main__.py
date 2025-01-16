from qiskit import transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

import circuit

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg")  # or 'Agg', 'Qt5Agg', etc.


def superdense_simulate(simulator, message):
    circ = transpile(circuit.build_circuit(message), simulator)
    result = simulator.run(circ, shots=1, memory=True).result()
    return result.get_memory(circ)[-1]


def superdense_simulate2(simulator, message):
    circs = circuit.build_circuits(message, 8)
    results = list(simulator.run(circ, shots=1, memory=True).result().get_memory(circ)[-1] for circ in circs)
    return "".join(results)


def main():
    simulator = AerSimulator()
    message = "11001011101111010111010111010101101011111100101110111101011101011101010110101111"
    print(f"The message {message} will be sent using superdense coding.")
    message_result = superdense_simulate2(simulator, message)
    print(f"The message {message_result} has been received.")

    assert message == message_result


if __name__ == "__main__":
    main()
