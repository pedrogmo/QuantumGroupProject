from qiskit import transpile
import circuit


def simulate_normal(simulator, bitstring: str, package_size: int, shots=1) -> list:
    """
    This simulation method assumes a perfect noiseless simulator. This is why the simulation is only run once (shots=1)
    and using memory=True the resulting measurement is recorded into a list and retrieved using [-1]. This yields a list
    of bitstrings, which are then joined together to recreate the original bitstring
    """

    # Build all the circuits (amount of circuits depends on amount of packages)
    circs = circuit.build_circuits(bitstring, package_size)

    # Transpile circuits such that it can run on the simulation
    circs_transpiled = list(transpile(circ, simulator) for circ in circs)

    # Simulate circuits and collect their results in a list.
    results = list(
        simulator.run(circ, shots=shots, memory=True).result().get_memory(circ)
        for circ in circs_transpiled
    )

    # Reorder results into correct list of bitstrings
    results = list(
        "".join(result[i] for result in results)
        for i in range(shots)
    )
    return results


def error_correction_encode(bitstring: str, n: int=3) -> str:
    if n % 2 == 0:
        raise ValueError("Invalid multiplier: n should be an uneven number")
    return bitstring * n


def error_correction_decode(bitstring: str, n: int=3) -> str:
    if n % 2 == 0:
        raise ValueError("Invalid multiplier: n should be an uneven number")
    threshold = int((n - 1) / 2)

    results = list(bitstring[i:i + n] for i in range(0, len(bitstring), n))
    return "".join(list("1" if bit.count("1") > threshold else "0" for bit in results))


def bitstring_flip(bitstring: str) -> str:
    new_bitstring = ""
    for bit in bitstring:
        if bit == "0":
            new_bitstring += "1"
        else:
            new_bitstring += "0"
    return new_bitstring


def bit_flip_encode(bitstring: str) -> str:
    if bitstring.count("0") > bitstring.count("1"):
        return "00" + bitstring
    return "11" + bitstring_flip(bitstring)


def bit_flip_decode(bitstring: str) -> str:
    if bitstring[0:2] == "00":
        return bitstring[2:]
    elif bitstring[0:2] == "11":
        return bitstring_flip(bitstring[2:])
    raise ValueError("Invalid starter bit pair: should either be 00 (not flipped) or 11 (flipped)")


def simulate_error_correction(simulator, bitstring: str, package_size: int, n: int=3) -> list:
    bitstring = error_correction_encode(bitstring, n)
    results = simulate_normal(simulator, bitstring, package_size)
    return list(error_correction_decode(result, n) for result in results)


def simulate_bit_flip(simulator, bitstring: str, package_size: int) -> list:
    bitstring = bit_flip_encode(bitstring)
    results = simulate_normal(simulator, bitstring, package_size)
    return list(bit_flip_decode(result) for result in results)
