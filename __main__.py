from qiskit import QuantumCircuit
from matplotlib import pyplot as plt
from qiskit_aer import AerSimulator

import matplotlib

#matplotlib.use("TkAgg")  # or 'Agg', 'Qt5Agg', etc.


def encode_message(msg, circuit, index=0):
    if msg == "00":
        pass  # To send 00 we do nothing
    elif msg == "10":
        circuit.x(index)  # To send 10 we apply an X-gate
    elif msg == "01":
        circuit.z(index)  # To send 01 we apply a Z-gate
    elif msg == "11":
        circuit.z(index)  # To send 11, we apply a Z-gate
        circuit.x(index)  # followed by an X-gate
    else:
        raise ValueError("Invalid message: can either be 00, 01, 10 or 11")


def main():

    send_image()
    return

    # Create a quantum circuit with two qubits
    qc = QuantumCircuit(2, 2)

    # Create the bell pair
    qc.h(0)  # Apply a h-gate to the first qubit
    qc.cx(0, 1)  # Apply a CNOT, using the first qubit as the control
    qc.barrier()  # Makes diagram neater by seperating gates

    # Alice chooses her message onto qubit 0.
    # I choose 11, but you can choose any of the 4 options and test it out
    msg = "11"
    encode_message(msg, qc)

    qc.barrier()  # Makes diagram neater by seperating gates

    # Alice sends her qubit to Bob

    # After recieving Alice's qubit, Bob applies the decoding protocol
    qc.cx(0, 1)
    qc.h(1)

    # Bob measures his qubits to read Alice's message
    qc.measure_all()

    # Draw output
    qc.draw(output="mpl")
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
