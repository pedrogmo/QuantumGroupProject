from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def assert_message(message):
    if len(message) % 2 == 1:
        raise ValueError("Invalid length: message should be an even number of bits long")
    for bit in message:
        if bit != "0" and bit != "1":
            raise ValueError("Invalid message: message can only contain 0 and 1 values")


def bell_state(circuit, index_0, index_1):
    circuit.h(index_0)
    circuit.cx(index_0, index_1)


def bell_state_inv(circuit, index_0, index_1):
    circuit.cx(index_0, index_1)
    circuit.h(index_0)


def encode_bit_pair(circuit, bit_pair, index):
    if bit_pair[0] == "1":
        circuit.z(index)
    if bit_pair[1] == "1":
        circuit.x(index)


def build_circuit(bits):
    # Reverse message and check validity
    bits = bits[::-1]
    assert_message(bits)

    # Initialize quantum circuit
    n = len(bits)
    circuit = QuantumCircuit(n)

    # Prepare and share the Bell state
    for i in range(0, n, 2):
        bell_state(circuit, i, i+1)
        encode_bit_pair(circuit, bits[i:i + 2], i)
        bell_state_inv(circuit, i, i + 1)
    circuit.measure_all()

    return circuit


def build_circuits(bits, package_size):
    if package_size % 2 == 1:
        raise ValueError("Invalid package length: packages should be an even number of bits long")
    if package_size > 28:
        print("Warning: qiskit does not support simulating >28 qubits. Package size has been set to 28.")
        package_size = 28

    packages = list(bits[i:i+package_size] for i in range(0, len(bits), package_size))
    return list(build_circuit(package) for package in packages)



# def transmit_image():
#     bitstr = "001101101010010010"
#
#     print(f"Alice transmits bit string\t{bitstr}")
#
#     # We transmit two bits at a time
#     # For now, assume that bitstr is even, for simplicity
#     n = int(len(bitstr) / 2)
#
#     circuits = [QuantumCircuit(2) for i in range(n)]
#
#     # First, entangle `n` qubits
#     for circ in circuits:
#         circ.h(0)
#         circ.cx(0, 1)
#         circ.barrier()
#
#     # Here we can wait for an arbitrary amount of time
#
#     # Bistring measured by Bob
#     bob_bitstr = ""
#
#     for i in range(n):
#         circ = circuits[i]
#
#         # Get the next two bits from the bit string
#         msg = bitstr[2*i:2*(i+1)]
#
#         # Alice applies operations to each of her qubit depending on the bit pair
#         encode_message(circ, msg)
#
#         # Now, Alice sends her component of the entangled pair
#         # And Bob receives and decodes it
#
#         circ.cx(0, 1)
#         circ.h(0)
#         circ.measure_all()
#
#         # Simulate circuit
#         result = AerSimulator().run(circ).result()
#
#         # Then append the measurement result to the string
#         bob_bitstr += result.get_counts().most_frequent()
#
#     print(f"Bob reads bit string\t\t{bob_bitstr}")
