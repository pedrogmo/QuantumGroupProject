from qiskit import transpile
import circuit


bit_flip_threshold = 0.7
bit_flip_addon = 2
bit_flip_no = "0" * bit_flip_addon
bit_flip_yes = "1" * bit_flip_addon



def simulate_normal(simulator, bitstring: str, package_size: int, shots: int=1) -> list:
    """
    This simulation method assumes a perfect noiseless simulator. This is why the simulation is only run once (shots=1)
    and using memory=True the resulting measurement is recorded into a list and retrieved using [-1]. This yields a list
    of bitstrings, which are then joined together to recreate the original bitstring
    """

    # Build all the circuits (amount of circuits depends on amount of packages)
    circs = circuit.build_circuits(bitstring, package_size, delay_us=delay_us)

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
    return "".join(bit * n for bit in bitstring)


def error_correction_decode(bitstring: str, n: int=3) -> str:
    if n % 2 == 0:
        raise ValueError("Invalid multiplier: n should be an uneven number")
    threshold = int((n - 1) / 2)

    results = list(bitstring[i:i + n] for i in range(0, len(bitstring), n))
    return "".join(list("1" if bit.count("1") > threshold else "0" for bit in results))


def bitstring_flip(bitstring: str) -> str:
    return "".join("1" if bit == "0" else "0" for bit in bitstring)


def bit_flip_encode(bitstring: str) -> str:
    count_1 = bitstring.count("1") / len(bitstring)
    if count_1 > 0.7:
        return bit_flip_yes + bitstring_flip(bitstring)
    return bit_flip_no + bitstring


def bit_flip_decode(bitstring: str) -> str:
    if bitstring[0:bit_flip_addon] == bit_flip_no:
        return bitstring[bit_flip_addon:]
    return  bitstring_flip(bitstring[bit_flip_addon:])


def simulate_error_correction(simulator, bitstring: str, package_size: int, shots: int=1, n: int=3) -> list:
    bitstring = error_correction_encode(bitstring, n)
    results = simulate_normal(simulator, bitstring, package_size, shots)
    return list(error_correction_decode(result, n) for result in results)


def simulate_bit_flip(simulator, bitstring: str, package_size: int, shots: int=1) -> list:
    bitstring = bit_flip_encode(bitstring)
    results = simulate_normal(simulator, bitstring, package_size, shots)
    return list(bit_flip_decode(result) for result in results)


def simulate_both(simulator, bitstring: str, package_size: int, shots: int=1, n: int=3) -> list:
    bitstring = bit_flip_encode(bitstring)
    bitstring = error_correction_encode(bitstring, n)

    results = simulate_normal(simulator, bitstring, package_size, shots)

    results = list(error_correction_decode(result, n) for result in results)
    results = list(bit_flip_decode(result) for result in results)
    return results
