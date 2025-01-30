from qiskit_ibm_runtime import fake_provider as q_fp
from statistics import mean
import numpy as np

import simulation
import error_correction


def string_comparison(bitstring: str, result: str) -> float:
    # Compares each string per character and determines the similarity (0 <= similarity <= 1)
    if len(bitstring) != len(result):
        raise ValueError("Both strings should be the same length")
    return sum(0 if bit1 != bit2 else 1 for bit1, bit2 in zip(bitstring, result)) / len(bitstring)


def accuracy_method_1(bitstring: str, results: list) -> float:
    # For each result, determines similarity to the original bitstring and takes the average of all similarities
    return mean(list(string_comparison(bitstring, result) for result in results))


def accuracy_method_2(bitstring: str, results: list) -> float:
    # Counts the amount of perfect matches in results to the original bitstring and divides by the total result amount
    return results.count(bitstring) / len(results)


def results_to_dict(results: list) -> dict:
    # Counts occurrence of each unique entry in results and records it in a dictionary
    return {value: results.count(value) for value in set(results)}


def provider_accuracy():
    # Test the accuracy of each of IBM's simulation backend with one bitstring, package length and shot amount
    simulators = [q_fp.FakeAlgiers(), q_fp.FakeAlmadenV2(), q_fp.FakeAuckland(), q_fp.FakeBoeblingenV2(),
                  q_fp.FakeBrisbane(), q_fp.FakeBrooklynV2(), q_fp.FakeCambridgeV2(), q_fp.FakeCusco(),
                  q_fp.FakeGeneva(), q_fp.FakeGuadalupeV2(), q_fp.FakeHanoiV2(), q_fp.FakeJohannesburgV2(),
                  q_fp.FakeKawasaki(), q_fp.FakeKolkataV2(), q_fp.FakeKyiv(), q_fp.FakeKyoto(), q_fp.FakeManhattanV2(),
                  q_fp.FakeMelbourneV2(), q_fp.FakeMontrealV2(), q_fp.FakeMumbaiV2(), q_fp.FakeOsaka(),
                  q_fp.FakeParisV2(), q_fp.FakePeekskill(), q_fp.FakePrague(), q_fp.FakePoughkeepsieV2(),
                  q_fp.FakeQuebec(), q_fp.FakeRochesterV2(), q_fp.FakeSherbrooke(), q_fp.FakeSingaporeV2(),
                  q_fp.FakeSydneyV2(), q_fp.FakeTorino(), q_fp.FakeTorontoV2(), q_fp.FakeWashingtonV2()]
    bitstring = "01010101"
    package_length = 8
    shots = 1000000

    # Prepare result arrays
    backend_names = np.array([simulator.name for simulator in simulators])
    results = np.zeros(len(simulators))

    # Simulate and record results
    for i, simulator in enumerate(simulators):
        print(simulator.backend_name)
        bitstring_results = simulation.simulate_full(simulator, bitstring, package_length, shots)
        results[i] = accuracy_method_1(bitstring, bitstring_results)

    # Save results
    data = np.column_stack((backend_names, results))
    np.savetxt("results/backends.txt", data, delimiter=", ", fmt="%s")


def pre_coding_accuracy(correction_methods, filename):
    # Test the accuracy of the simulation for 24-bit strings with varying amount of '1'-counts with one simulator,
    # package length and shot amount
    n = 24
    simulator = q_fp.FakeCusco()
    bitstrings = list((n - i) * "0" + i * "1" for i in range(n+1))
    package_length = 8
    shots = 1000000

    # Prepare result arrays
    one_count = list(range(n+1))
    results = np.zeros(n+1)

    # Simulate and record results
    for i, bitstring in enumerate(bitstrings):
        print(bitstring)
        bitstring_results = simulation.simulate_full(simulator, bitstring, package_length, shots, correction_methods)
        results[i] = accuracy_method_1(bitstring, bitstring_results)

    # Save results
    data = np.column_stack((one_count, results))
    np.savetxt(filename, data, fmt="%s")


def pre_coding_on_accuracy():
    # Test the accuracy of the simulation for 24-bit strings with varying amount of '1'-counts with pre_coding on
    pre_coding_accuracy([(error_correction.pre_coding_optimize_encode, error_correction.pre_coding_optimize_decode, [4])],
                      "results/bit_flip_on.txt")


def pre_coding_off_accuracy():
    # Test the accuracy of the simulation for 24-bit strings with varying amount of '1'-counts with pre_coding off
    pre_coding_accuracy([], "results/bit_flip_off.txt")


def package_size_accuracy():
    # Test the accuracy of the simulation for different package sizes with one simulator, bitstring, package length and
    # shot amount
    n = 14
    simulator = q_fp.FakeCusco()
    bitstring = "01010101"
    package_lengths = list(2 * i for i in range(1, n+1))
    shots = 1000000

    # Prepare result array
    results = np.zeros(n)

    # Simulate and record results
    for i, package_length in enumerate(package_lengths):
        print(package_length)
        bitstring_results = simulation.simulate_full(simulator, bitstring, package_length, shots)
        results[i] = accuracy_method_1(bitstring, bitstring_results)

    # Save results
    data = np.column_stack((package_lengths, results))
    np.savetxt("results/package_length.txt", data, fmt="%s")


def repetition_accuracy():
    # Test the accuracy of the simulation for different repetitions with one simulator, bitstring, package length and
    # shot amount
    n = 4
    simulator = q_fp.FakeCusco()
    bitstring = "01010101"
    package_length = 8
    shots = 1000000

    # Prepare result arrays
    repetitions = list(2 * i + 1 for i in range(n))
    results = np.zeros(n)

    # Simulate and record results
    for i, repetition in enumerate(repetitions):
        print(repetition)
        methods = [(error_correction.repetition_encode, error_correction.repetition_decode, [repetition])]
        bitstring_results = simulation.simulate_full(simulator, bitstring, package_length, shots, methods)
        results[i] = accuracy_method_1(bitstring, bitstring_results)

    # Save results
    data = np.column_stack((repetitions, results))
    np.savetxt("results/repetitions.txt", data, fmt="%s")


def main():
    # Possible accuracy measurements to test: uncomment to run
    provider_accuracy()
    # pre_coding_on_accuracy()
    # pre_coding_off_accuracy()
    # package_size_accuracy()
    # repetition_accuracy()


if __name__ == '__main__':
    main()
