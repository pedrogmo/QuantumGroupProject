from qiskit import QuantumCircuit


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
