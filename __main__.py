from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeQuebec
from qiskit.visualization import plot_histogram

import matplotlib
import numpy as np
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


def transmit_msg(mapping: str = "00", compress_flag: bool = True, image="./images/mario.png"):
    """
    Transmits an image using dense coding.

    :param mapping: bit-mapping to go over image (2 bit string)
    :param compress_flag: whether to compress the image or not
    :param image: the image path to transmit
    """
    simulator = AerSimulator()
    image = Image(image)
    message = image.to_bitstr(compress_flag=compress_flag)

    print("Transmitting message of length ", len(message))

    message_result = simulation.simulate_normal(simulator, message, 28, 1, mapping=mapping)[0]
    image_result = Image.from_bitstr(message_result, image.width, image.height, compress_flag=compress_flag)

    print("Finished transmitting image!")

    image_result.display()
    plt.show()


def transmit_msg_with_cypher(cypher_before: bool, compress_flag: bool = True, image="./images/mario.png"):
    """
    Transmits an image using dense coding, adding key cyphering/de-cyphering to the quantum circuit.

    :param cypher_before: if TRUE then cyphers the message before transmission and then decodes it using superdense
    circuit, otherwise cyphers it using quantum the circuit
    :param compress_flag: whether to compress the image or not
    :param image: the image path to transmit
    """
    encoding="RGB"
    simulator = AerSimulator()
    image = Image(image)
    message = image.to_bitstr(compress_flag=compress_flag, encoding=encoding)

    key = np.random.choice([0, 1], size=len(message))
    message_result = None

    if cypher_before:
        print("Cyphering Image.")
        temp = np.array(list(message))
        temp = temp.astype(int)
        temp = np.bitwise_xor(temp, key)
        temp = temp.astype(str)
        message = "".join(temp)

    post_cypher_image = Image.from_bitstr(message, image.width, image.height, compress_flag=compress_flag, encoding=encoding)
    post_cypher_image.display(subplot=(1, 2, 1))



    print("Transmitting message of length ", len(message))

    message_result = simulation.simulate_normal(simulator, message, 28, 1, mapping="".join(key.astype(str)))[0]
    image_result = Image.from_bitstr(message_result, image.width, image.height, compress_flag=compress_flag, encoding=encoding)

    print("Finished transmitting image!")

    image_result.display(subplot=(1,2,2))
    plt.show()


def mapped_image():
    print("Enter 2 bit mapping:")
    mapping = input()
    if mapping == "":
        print("Cypher before? (y/n):")
        mapping = input()
        if mapping == "y":
            transmit_msg_with_cypher(True, compress_flag=False)
        else:
            transmit_msg_with_cypher(False, compress_flag=False)
    else:
        transmit_msg(mapping, compress_flag=False)


def mapped_image_all(compress_flag: bool = False, image="./images/mario.png"):
    """
    Transmits an image using dense coding.

    :param mapping: bit-mapping to go over image (2 bit string)
    :param compress_flag: whether to compress the image or not
    :param image: the image path to transmit
    """
    simulator = AerSimulator()
    image = Image(image)
    message = image.to_bitstr(compress_flag=compress_flag, encoding="RGB")

    mappings = ["00", "01", "10", "11"]
    for i in range(len(mappings)):
        print("Transmitting message", i, "of length ", len(message))
        message_result = simulation.simulate_normal(simulator, message, 28, 1, mapping=mappings[i])[0]
        image_result = Image.from_bitstr(message_result, image.width, image.height, compress_flag=compress_flag, encoding="RGB")
        image_result.display(subplot=(2, 2, i+1))
        print("Finished transmitting image!")

    plt.show()



if __name__ == "__main__":
    # main()
    # transmit_msg()
    # mapped_image()
    mapped_image_all()
