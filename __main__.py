from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeQuebec
from qiskit.visualization import plot_histogram

import matplotlib
from matplotlib import pyplot as plt

import circuit
import simulation
from image import Image

matplotlib.use("TkAgg")  # or 'Agg', 'Qt5Agg', etc.


def superdense_draw(bitstring: str):
    circ = circuit.build_circuit(bitstring)
    circ.draw("mpl")
    plt.show()


def main():
    simulator = FakeQuebec()
    message = "0000000000"
    print(f"The message {message} will be sent using superdense coding.")
    message_result = simulation.simulate_normal(simulator, message, 2, 10)
    print(f"The message {message_result} has been received.")


def transmit_msg():
    simulator = AerSimulator()

    image = Image("./images/mario.png")
    message = image.to_bitstr()

    print("Transmitting message of length ", len(message))

    message_result = simulation.simulate_normal(simulator, message, 28, 1)[0]
    image_result = Image.from_bitstr(message_result, image.width, image.height)

    print("Finished transmitting image!")

    image_result.display()

def transmit_img_decoherence():
    device_backend = FakeQuebec()
    simulator = AerSimulator.from_backend(device_backend)

    image = Image("./images/mario.png")
    message = image.to_bitstr(compress_flag = False)

    print("Transmitting message of length ", len(message))

    message_result = simulation.simulate_normal(simulator, message, 28, 1, delay_us=100)[0]
    image_result = Image.from_bitstr(message_result, image.width, image.height, compress_flag = False)

    print("Finished transmitting image!")

    image_result.display()

def graph_decoherence():
    message = "111111111111"

    delays = [0, 100, 200, 300, 400]
    fidelity = []

    for delay in delays:
        device_backend = FakeQuebec()
        simulator = AerSimulator.from_backend(device_backend)

        message_results = simulation.simulate_normal(simulator, message, 2, 1000, delay_us=delay)
        total_matches = 0

        for res in message_results:
            total_matches += sum([c1 == c2 for c1, c2 in zip(message, res)])

        avg_matches = total_matches / len(message_results)
        acc = 100 * avg_matches / len(message)
        fidelity.append(acc)

        print(f"{acc}%")

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(delays, fidelity, marker='o', linestyle='-', color='b', label='Fidelity')

    # Customize the plot
    plt.title('Fidelity vs. Delay Time', fontsize=16)
    plt.xlabel('Delay Time (μs)', fontsize=14)
    plt.ylabel('Fidelity (%)', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(alpha=0.5)
    plt.legend(fontsize=12)

    # Show the plot
    plt.tight_layout()
    plt.show()

    # plt.bar([str(d) for d in delays], accuracies)
    # plt.title('Fidelity per Delay time')
    # plt.xlabel('Delay (microseconds)')
    # plt.ylabel('Fidelity (%)')
    # plt.show()


if __name__ == "__main__":
    # main()
    # transmit_msg()
    # transmit_img_decoherence()
    graph_decoherence()