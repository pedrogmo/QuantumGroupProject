from pyexpat.errors import messages

from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import fake_provider as q_fp
from qiskit.visualization import plot_histogram

import matplotlib
from matplotlib import pyplot as plt

import simulation
from image import Image

matplotlib.use("TkAgg")  # or 'Agg', 'Qt5Agg', etc.


def superdense_draw(bitstring: str):
    circuit = simulation.build_circuit(bitstring)
    circuit.draw("mpl")
    plt.show()


def main():
    simulator = q_fp.FakeAlgiers()
    message = "00000000"
    print(f"The message {message} will be sent using superdense coding.")
    circuits = simulation.build_circuits_transpiled(message, 8, simulator)
    results = simulation.simulate(simulator, circuits, 100)
    results = {value: results.count(value) for value in set(results)}
    print(f"The message {results} has been received.")
    plot_histogram(results)
    plt.show()


def transmit_msg():
    simulator = AerSimulator()

    image = Image("./images/mario.png")
    message = image.to_bitstr()

    print("Transmitting message of length ", len(message))

    message_result = simulation.simulate(simulator, message, 28, 1)[0]
    image_result = Image.from_bitstr(message_result, image.width, image.height)

    print("Finished transmitting image!")

    image_result.display()


def transmit_img_decoherence():
    device_backend = q_fp.FakeAlgiers()
    simulator = AerSimulator.from_backend(device_backend)

    image = Image("./images/mario.png")
    message = image.to_bitstr(compress_flag = False)

    print("Transmitting message of length ", len(message))

    message_result = simulation.simulate(simulator, message, 28, 1, delay_us=0)[0]
    image_result = Image.from_bitstr(message_result, image.width, image.height, compress_flag = False)

    print("Finished transmitting image!")

    image_result.display()

def graph_decoherence():
    message = "111111111111"

    delays = [0, 100, 200, 300, 400]
    accuracies = []

    for delay in delays:
        device_backend = q_fp.FakeAlgiers()
        simulator = AerSimulator.from_backend(device_backend)

        message_results = simulation.simulate(simulator, message, 2, 20, delay_us=delay)
        total_matches = 0

        for res in message_results:
            total_matches += sum([c1 == c2 for c1, c2 in zip(message, res)])

        avg_matches = total_matches / len(message_results)
        acc = 100 * avg_matches / len(message)
        accuracies.append(acc)

        print(f"{acc}%")

    plt.bar([str(d) for d in delays], accuracies)
    plt.title('Accuracy per Delay time')
    plt.xlabel('Delay (microseconds)')
    plt.ylabel('Accuracy (%)')
    plt.show()


if __name__ == "__main__":
    main()
    # superdense_draw("0000")
    # transmit_msg()
    # transmit_img_decoherence()
    # graph_decoherence()
