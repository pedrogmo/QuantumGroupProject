from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

import circuit

from matplotlib import pyplot as plt
from qiskit_aer import AerSimulator

import matplotlib

#matplotlib.use("TkAgg")  # or 'Agg', 'Qt5Agg', etc.


def main():

    send_image()
    return

    # Create a quantum circuit with two qubits
    qc = QuantumCircuit(2, 2)
    simulator = AerSimulator()
    circ = transpile(circuit.build_circuit("00"), simulator)

    result = simulator.run(circ, shots=100).result()
    counts = result.get_counts(circ)

    plot_histogram(counts, title="Superdense coding")
    plt.show()

def send_image():#img: Image):
    #bitstr = img.to_bistring()
    bitstr = "001100110110"

    # We transmit two bits at a time   
    # For now, assume that bitstr is even, for simplicity
    n = int(len(bitstr) / 2)

    circuits = [QuantumCircuit(2, 2) for i in range(n)]

    # First, entangle `n` qubits
    for circ in circuits:
        circ.h(0)
        circ.cx(0, 1)
        circ.barrier()

    # Here we can wait for an indeterminate amount of time

    # Alice applies operations to each of her qubit depending on the bit pair
    for i in range(n):
        circ = circuits[i]

        msg = bitstr[2*i:2*(i+1)]
        encode_message(msg, circ)
        
        # Now, Alice sends her component of the entangled pair
        # And Bob receives and decodes it

        circ.cx(0, 1)
        circ.h(1)
        circ.measure_all()
    
        # Simulate circuit
        result = AerSimulator().run(circ).result()

        # Then do something with the result (https://docs.quantum.ibm.com/api/qiskit/qiskit.result.Result)
        print (result.get_counts().most_frequent())


if __name__ == "__main__":
    main()
