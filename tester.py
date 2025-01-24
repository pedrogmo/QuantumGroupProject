from qiskit_ibm_runtime import fake_provider as q_fp
from statistics import mean
from matplotlib import pyplot as plt
import numpy as np

import simulation
import error_correction


# def bar_graph(x_axis, results):
#     x_range = np.arange(len(x_axis))
#     width = 0.2
#     multiplier = 0
#
#     fig, ax = plt.subplots(layout="constrained")
#
#     for sim_type, measurement in results.items():
#         offset = width * multiplier
#         rects = ax.bar(x_range + offset, measurement, width, label=sim_type)
#         ax.bar_label(rects, padding=3)
#         multiplier += 1
#
#     ax.set_ylabel("Success rate (%)")
#     ax.set_title("Simulation success rate by method")
#     ax.set_xticks(x_range + width, x_axis)
#     ax.legend()
#     plt.show()


def get_success_rate(bitstring: str, result: str) -> float:
    if len(bitstring) != len(result):
        raise ValueError("Both strings should be the same length")
    return sum(0 if bit1 != bit2 else 1 for bit1, bit2 in zip(bitstring, result)) / len(bitstring)


def success_rate_method_1(bitstring: str, results: list) -> float:
    return mean(list(get_success_rate(bitstring, result) for result in results))


def success_rate_method_2(bitstring: str, results: list) -> float:
    return results.count(bitstring) / len(results)


def results_to_dict(results: list) -> dict:
    return {value: results.count(value) for value in set(results)}


def example():
    simulator = q_fp.FakeAlgiers()
    bitstring = "11111111"
    package_length = 8
    shots = 1000

    print(f"The message {bitstring} will be sent using superdense coding.")

    methods = [
        [],
        [(error_correction.repetition_encode, error_correction.repetition_decode, [3])],
        [(error_correction.bit_flip_encode, error_correction.bit_flip_decode, [2])],
    ]
    descriptions = ["No error correction", "Repetition error correction", "Bit flip error correction"]

    for method, description in zip(methods, descriptions):
        print(description)
        results = simulation.simulate_full(simulator, bitstring, package_length, shots, method)
        print(f"Results: {results_to_dict(results)}")


def provider_fidelity():
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

    backend_names = np.array(["" for i in range(len(simulators))])
    results = np.zeros(len(simulators))

    for i, simulator in enumerate(simulators):
        print(simulator.backend_name)
        bitstring_results = simulation.simulate_full(simulator, bitstring, package_length, shots, [])
        results[i] = success_rate_method_1(bitstring, bitstring_results)

    data = np.column_stack((backend_names, results))
    np.savetxt("results/backends.txt", data, delimiter=", ", fmt="%s")


def bit_flip_fidelity():
    n = 24
    simulator = q_fp.FakeKyiv()
    bitstrings = list((n - i) * "0" + i * "1" for i in range(n+1))
    package_length = 8
    shots = 1000000

    one_count = list(range(n+1))
    results = np.zeros(n+1)

    for i, bitstring in enumerate(bitstrings):
        print(bitstring)
        bitstring_results = simulation.simulate_full(simulator, bitstring, package_length, shots, [])
        results[i] = success_rate_method_1(bitstring, bitstring_results)

    data = np.column_stack((one_count, results))
    np.savetxt("results/bit_flip.txt", data, fmt="%s")


def package_size_fidelity():
    n = 14
    simulator = q_fp.FakeKyiv()
    bitstring = "01010101"
    package_lengths = list(2 * i for i in range(1, n+1))
    shots = 1000000

    results = np.zeros(n)

    for i, package_length in enumerate(package_lengths):
        print(package_length)
        bitstring_results = simulation.simulate_full(simulator, bitstring, package_length, shots, [])
        results[i] = success_rate_method_1(bitstring, bitstring_results)

    data = np.column_stack((package_lengths, results))
    np.savetxt("results/package_length.txt", data, fmt="%s")


def repetition_fidelity():
    simulator = q_fp.FakeKyiv()
    bitstring = "01010101"
    package_length = 8
    shots = 1000000

    n = 4
    repetitions = list(2 * i + 1 for i in range(n))
    results = np.zeros(n)

    for i, repetition in enumerate(repetitions):
        print(repetition)
        methods = [(error_correction.repetition_encode, error_correction.repetition_decode, [repetition])]
        bitstring_results = simulation.simulate_full(simulator, bitstring, package_length, shots, methods)
        results[i] = success_rate_method_1(bitstring, bitstring_results)

    data = np.column_stack((repetitions, results))
    np.savetxt("results/repetitions.txt", data, fmt="%s")
