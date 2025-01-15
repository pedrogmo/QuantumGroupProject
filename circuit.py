from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def assert_message(message):
    if len(message) % 2 == 1:
        raise ValueError("Invalid length: message should be an even number of bits long")
    for bit in message:
        if bit != "0" and bit != "1":
            raise ValueError("Invalid message: message can only contain 0 and 1 values")


def build_circuit(message):
    message = message[::-1]
    assert_message(message)
    n = len(message)

    # Initialize quantum circuit
    circuit = QuantumCircuit(n)

    # Prepare and share the Bell state
    circuit.h(0)
    for i in range(1, n):
        circuit.cx(0, i)
    circuit.barrier()

    # Sender encodes the bits
    if message[n-1] == "1":
        circuit.z(n-1)
    for i in range(0, n-2):
        if message[i] == "1":
            circuit.x(i)
    circuit.barrier()

    # Receiver decodes the bits
    for i in range(0, n-1):
        circuit.cx(n-1, i)
    circuit.h(n-1)
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