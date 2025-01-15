from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def encode_message(circuit, msg, index=0):
    if msg not in ["00", "01", "10", "11"]:
        raise ValueError("Invalid message: can either be 00, 01, 10 or 11")

    if msg[0] == "1":
        circuit.x(index)
    if msg[1] == "1":
        circuit.z(index)


def bell_pair(circuit, index_0, index_1):
    circuit.h(index_0) # Hadamard gate
    circuit.cx(index_0, index_1) # CNOT gate


def bell_pair_inv(circuit, index_0, index_1):
    circuit.cx(index_0, index_1)
    circuit.h(index_0)


def build_circuit(message):
    circuit = QuantumCircuit(2)

    bell_pair(circuit, 0, 1)
    circuit.barrier()

    encode_message(circuit, message)
    circuit.barrier()

    bell_pair_inv(circuit, 0, 1)

    circuit.measure_all()

    return circuit

def transmit_image():
    bitstr = "001101101010010010"

    print(f"Alice transmits bit string\t{bitstr}")

    # We transmit two bits at a time   
    # For now, assume that bitstr is even, for simplicity
    n = int(len(bitstr) / 2)

    circuits = [QuantumCircuit(2) for i in range(n)]

    # First, entangle `n` qubits
    for circ in circuits:
        circ.h(0)
        circ.cx(0, 1)
        circ.barrier()

    # Here we can wait for an arbitrary amount of time

    # Bistring measured by Bob
    bob_bitstr = ""

    for i in range(n):
        circ = circuits[i]

        # Get the next two bits from the bit string
        msg = bitstr[2*i:2*(i+1)]

        # Alice applies operations to each of her qubit depending on the bit pair
        encode_message(circ, msg)
        
        # Now, Alice sends her component of the entangled pair
        # And Bob receives and decodes it

        circ.cx(0, 1)
        circ.h(0)
        circ.measure_all()
    
        # Simulate circuit
        result = AerSimulator().run(circ).result()

        # Then append the measurement result to the string
        bob_bitstr += result.get_counts().most_frequent()
    
    print(f"Bob reads bit string\t\t{bob_bitstr}")