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
    message = image.to_bitstr()

    print("Transmitting message of length ", len(message))

    message_result = simulation.simulate_normal(simulator, message, 28, 1)[0]
    image_result = Image.from_bitstr(message_result, image.width, image.height)

    print("Finished transmitting image!")

    image_result.display()



if __name__ == "__main__":
    # main()
    # transmit_msg()
    transmit_img_decoherence()
