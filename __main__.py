import qiskit_ibm_runtime.fake_provider
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime.fake_provider import FakeQuebec

import matplotlib
from matplotlib import pyplot as plt

import circuit
from image import Image

matplotlib.use("TkAgg")  # or 'Agg', 'Qt5Agg', etc.


def superdense_simulate(simulator, bitstring: str, package_size: int, error_correction=False) -> str:
    """
    This simulation method assumes a perfect noiseless simulator. This is why the simulation is only run once (shots=1)
    and using memory=True the resulting measurement is recorded into a list and retrieved using [-1]. This yields a list
    of bitstrings, which are then joined together to recreate the original bitstring
    """
    n = 3
    if error_correction:
        bitstring *= n

    # Build all the circuits (amount of circuits depends on amount of packages)
    circs = circuit.build_circuits(bitstring, package_size)

    # Transpile circuits such that it can run on the simulation
    circs_transpiled = list(transpile(circ, simulator) for circ in circs)

    # Simulate circuits and collect their results in a list.
    results = list(
        simulator.run(circ, shots=1, memory=True).result().get_memory(circ)[-1]
        for circ in circs_transpiled
    )
    results = "".join(results)

    if error_correction:
        threshold = int((n - 1) / 2)
        results = list(results[i:i + n] for i in range(0, len(results), n))
        results = "".join(list("1" if bit.count("1") > threshold else "0" for bit in results))
    return results


def superdense_draw(bitstring: str):
    circ = circuit.build_circuit(bitstring)
    circ.draw(output="mpl")
    plt.show()


def main():
    simulator = FakeQuebec()
    message = "1111111111"
    print(f"The message {message} will be sent using superdense coding.")
    message_result = superdense_simulate(simulator, message, 8, error_correction=False)
    print(f"The message {message_result} has been received.")
    # assert message == message_result


def transmit_msg():
    simulator = AerSimulator()
    image = Image("./images/mario.png")
    message = image.to_bitstr()

    print("Transmitting message of length ", len(message))

    message_result = superdense_simulate(simulator, message, 28)
    image_result = Image.from_bitstr(message_result, image.width, image.height)

    print("Finished transmitting image!")

    image_result.display()


if __name__ == "__main__":
    main()
    # transmit_msg()
