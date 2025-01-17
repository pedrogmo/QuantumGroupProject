from qiskit import transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

import circuit

from matplotlib import pyplot as plt
import matplotlib

from image import Image
matplotlib.use("TkAgg")  # or 'Agg', 'Qt5Agg', etc.


def superdense_simulate(simulator, message):
    circ = circuit.build_circuit(message)
    circ_transpiled = transpile(circ, simulator)
    result = simulator.run(circ_transpiled, shots=1, memory=True).result()
    return result.get_memory(circ_transpiled)[-1]


def superdense_simulate2(simulator, message, package_size):
    circs = circuit.build_circuits(message, package_size)
    circs_transpiled = list(transpile(circ, simulator) for circ in circs)
    results = list(simulator.run(circ, shots=1, memory=True).result().get_memory(circ)[-1]
                   for circ in circs_transpiled)
    return "".join(results)


def main():
    simulator = AerSimulator()
    message = "1111111111111111111111111111"
    print(f"The message {message} will be sent using superdense coding.")
    message_result = superdense_simulate2(simulator, message, 8)
    print(f"The message {message_result} has been received.")

    assert message == message_result

def transmit_msg():
    simulator = AerSimulator()
    image = Image("./images/mario.png")
    message = image.to_bitstr()
    
    print("Transmitting message of length ", len(message))

    message_result = superdense_simulate2(simulator, message, 8)
    image_result = Image.from_bitstr(message_result, image.width, image.height)
    
    print("Finished transmitting image!")
    
    image_result.display()


if __name__ == "__main__":
    # main()
    transmit_msg()
