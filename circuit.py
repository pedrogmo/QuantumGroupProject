from qiskit import QuantumCircuit


def assert_bitstring(bitstring: str):
    if len(bitstring) % 2 == 1:
        # Because superdense coding sends pairs of bits, the string should be an even numbered length
        raise ValueError("Invalid length: bitstring should be an even number of bits long")
    for bit in bitstring:
        if bit != "0" and bit != "1":
            raise ValueError("Invalid content: bitstring can only contain 0 and 1 values")


def assert_package_length(package_length: int):
    if package_length > 28:
        # Because the qiskit simulation only supports up to 28 qubits, the package length cannot exceed 28 bits
        raise ValueError("Invalid package length: packages should not exceed 28 bits")
    if package_length % 2 == 1:
        # Because superdense coding sends pairs of bits, the package length should be an even number
        raise ValueError("Invalid package length: packages should be an even number of bits long")


def bell_state(circuit: QuantumCircuit, index_0: int, index_1: int):
    circuit.h(index_0)
    circuit.cx(index_0, index_1)


def bell_state_inv(circuit: QuantumCircuit, index_0: int, index_1: int):
    circuit.cx(index_0, index_1)
    circuit.h(index_0)


def encode_bit_pair(circuit: QuantumCircuit, bit_pair: str, index: int):
    if bit_pair[0] == "1":
        circuit.z(index)
    if bit_pair[1] == "1":
        circuit.x(index)


def build_circuit(bits: str) -> QuantumCircuit:
    # Reverse bitstring and check validity
    bits = bits[::-1]
    assert_bitstring(bits)

    # Initialize quantum circuit
    n = len(bits)
    circuit = QuantumCircuit(n)

    # Build the circuit
    # Create all the Bell-pairs
    for i in range(0, n, 2):
        bell_state(circuit, i, i+1)
    circuit.barrier()

    # Encode the bit pairs into the first qubit of every Bell-pair
    for i in range(0, n, 2):
        encode_bit_pair(circuit, bits[i:i + 2], i)
    circuit.barrier()

    # Decode all the Bell-pairs and measure their states
    for i in range(0, n, 2):
        bell_state_inv(circuit, i, i + 1)
    circuit.measure_all()

    return circuit


def build_circuits(bits: str, package_length: int) -> list:
    # Check validity of package length
    assert_package_length(package_length)

    # Divide bits into equally sized packages (with the last bits as the remainder package)
    packages = list(bits[i:i+package_length] for i in range(0, len(bits), package_length))

    # Build the circuits
    return list(build_circuit(package) for package in packages)
