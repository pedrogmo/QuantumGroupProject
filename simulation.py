from qiskit import QuantumCircuit
from qiskit import transpile


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


def build_circuit(bitstring: str, delay_us: float = 0.0) -> QuantumCircuit:
    # Reverse bitstring and check validity
    bitstring = bitstring[::-1]
    assert_bitstring(bitstring)

    # Initialize quantum circuit
    n = len(bitstring)
    circuit = QuantumCircuit(n)

    # Build the circuit
    # Create all the Bell-pairs
    for i in range(0, n, 2):
        bell_state(circuit, i, i+1)
    circuit.barrier()

    # Here, we can wait an arbitrary amount of time
    if delay_us != 0.0:
        circuit.delay(delay_us, unit="us")

    # Encode the bit pairs into the first qubit of every Bell-pair
    for i in range(0, n, 2):
        encode_bit_pair(circuit, bitstring[i:i + 2], i)
    circuit.barrier()

    # Decode all the Bell-pairs and measure their states
    for i in range(0, n, 2):
        bell_state_inv(circuit, i, i + 1)
    circuit.measure_all()

    return circuit


def build_circuits(bitstring: str, package_length: int, delay_us: float = 0.0) -> list:
    # Check validity of package length
    assert_package_length(package_length)

    # Divide bits into equally sized packages (with the last bits as the remainder package)
    packages = list(bitstring[i:i + package_length] for i in range(0, len(bitstring), package_length))

    # Build the circuits
    return list(build_circuit(package, delay_us=delay_us) for package in packages)


def build_circuit_transpiled(bits: str, simulator, delay_us: float = 0.0) -> QuantumCircuit:
    circuit = build_circuit(bits, delay_us)
    return transpile(circuit, simulator)


def build_circuits_transpiled(bits: str, package_length: int, simulator, delay_us: float = 0.0) -> list:
    circuits = build_circuits(bits, package_length, delay_us)
    return list(transpile(circuit, simulator) for circuit in circuits)


def simulate(simulator, circuits: list, shots: int=1) -> list:
    # Simulate circuits and collect their results in a list.
    results = list(
        simulator.run(circuit, shots=shots, memory=True).result().get_memory(circuit)
        for circuit in circuits
    )

    # Reorder results into correct list of bitstrings
    results = list(
        "".join(result[i] for result in results)
        for i in range(shots)
    )

    return results


def simulate_full(simulator, bitstring: str, package_length: int, shots: int, correction_methods: list) -> list:
    if len(correction_methods) == 0:
        encode_methods, decode_methods, args = [], [], []
    else:
        encode_methods, decode_methods, args = zip(*correction_methods)

    for method, arg in zip(encode_methods, args):
        bitstring = method(bitstring, *arg)

    circuits = build_circuits_transpiled(bitstring, package_length, simulator)
    results = simulate(simulator, circuits, shots)

    for method, arg in zip(decode_methods, args):
        results = list(method(result, *arg) for result in results)

    return results
