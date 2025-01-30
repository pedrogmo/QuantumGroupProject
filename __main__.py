from pyexpat.errors import messages
# from pywin import default_scintilla_encoding

from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import fake_provider as q_fp

import matplotlib
from matplotlib import pyplot as plt
from sympy.crypto import encode_morse

import circuit
import quantum_hardware
from quantum_hardware import ExperimentResult
import simulation
import tester
from image import Image

matplotlib.use("TkAgg")  # or 'Agg', 'Qt5Agg', etc.


def circuit_draw(bitstring: str):
    circuit = simulation.build_circuit(bitstring)
    circuit.draw("mpl")
    plt.show()


def main():
    # tester.bit_flip_example()
    tester.provider_example()


def transmit_msg_sim():
    simulator = AerSimulator()

    image = Image("./images/mario.png")
    message = image.to_bitstr()

    print("Transmitting message of length ", len(message))

    message_result = simulation.simulate(simulator, message, 28, 1)[0]
    image_result = Image.from_bitstr(message_result, image.width, image.height)

    print("Finished transmitting image!")

    image_result.display()


def fetch_job():
    image = Image("./images/mario.png")
    job_id = "cy98eja7v8tg008frzc0"
    exp_result: ExperimentResult = quantum_hardware.fetch_previous_job(job_id, 28)

    message_result = exp_result.bitstring
    image_result = Image.from_bitstr(message_result, image.width, image.height)

    print(f"Finished transmitting image with a fidelity of {exp_result.fidelity}!")

    image_result.display()


def transmit_msg_hardware():
    image = Image("./images/mario.png")
    message = image.to_bitstr(compress_flag=False)

    print("Transmitting message of length ", len(message))

    exp_result: ExperimentResult = quantum_hardware.run(message, 126)

    message_result = exp_result.bitstring
    image_result = Image.from_bitstr(
        message_result, image.width, image.height, compress_flag=False
    )

    print(f"Finished transmitting image with a fidelity of {exp_result.fidelity}!")

    image_result.display()


def measure_fidelity_hardware():
    image = Image("./images/mario.png")
    message = image.to_bitstr(compress_flag=False)

    # qubit_counts = [4, 8, 16, 32, 64, 96, 126]
    qubit_counts = [80, 100, 112]
    qubit_counts.reverse()

    print("Transmitting message of length ", len(message))

    for q in qubit_counts:
        # color print the qubit count
        print(f"[\033[1;32;40m{q} qubits\033[0m]")
        exp_result: ExperimentResult = quantum_hardware.run(message, q)

        message_result: str = exp_result.bitstring
        image_result: Image = Image.from_bitstr(
            message_result, image.width, image.height, compress_flag=False
        )

        print(f"Finished transmitting image with a fidelity of {exp_result.fidelity}!")

        # write to a file for later analysis with qubit count and fidelity
        with open("fidelity_results.txt", "a") as f:
            f.write(f"{q} qubits | {exp_result.fidelity}\n")

        # save the image in images/hardware/sherbrooke with the qubit count as title
        image_result.buffer.save(f"images/hardware/sherbrooke/{q}_qubits.png")


def transmit_img_decoherence():
    device_backend = q_fp.FakeAlgiers()
    simulator = AerSimulator.from_backend(device_backend)

    image = Image("./images/mario.png")
    message = image.to_bitstr(compress_flag=False)

    print("Transmitting message of length ", len(message))

    message_result = simulation.simulate_normal(simulator, message, 28, 1, delay_us=0)[
        0
    ]
    image_result = Image.from_bitstr(
        message_result, image.width, image.height, compress_flag=False
    )

    print("Finished transmitting image!")

    image_result.display()


def graph_decoherence():
    message = "111111111111"

    delays = [0, 100, 200, 300, 400]
    fidelity = []

    for delay in delays:
        device_backend = q_fp.FakeAlgiers()
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
    # graph_decoherence()
    # transmit_msg_hardware()
    # measure_fidelity_hardware()
    transmit_msg_sim()
    # graph_decoherence()
    # fetch_job()