from qiskit import QuantumCircuit


def encode_message(circuit, msg, index=0):
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
