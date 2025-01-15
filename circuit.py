from qiskit import QuantumCircuit


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
