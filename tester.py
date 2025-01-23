from qiskit_ibm_runtime import fake_provider as q_fp
from statistics import mean
from matplotlib import pyplot as plt

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


def bit_flip_example():
    n = 8
    simulator = q_fp.FakeAlgiers()
    bitstrings = list((n - i) * "0" + i * "1" for i in range(n+1))
    package_length = 8
    shots = 100000

    method_1 = []
    method_2 = [(error_correction.bit_flip_encode, error_correction.bit_flip_decode, [4])]

    success_rates_1 = list()
    success_rates_2 = list()

    for bitstring in bitstrings:
        print(bitstring)
        results = simulation.simulate_full(simulator, bitstring, package_length, shots, method_1)
        success = mean(list(get_success_rate(bitstring, result) for result in results))
        success_rates_1.append(success)

        results = simulation.simulate_full(simulator, bitstring, package_length, shots, method_2)
        success = mean(list(get_success_rate(bitstring, result) for result in results))
        success_rates_2.append(success)

    plt.figure()
    plt.plot(list(range(n+1)), success_rates_1)
    plt.plot(list(range(n+1)), success_rates_2)
    plt.show()


def provider_example():
    simulators = q_fp.FakeProviderForBackendV2().backends()
    bitstring = "01010101"
    package_length = 8
    shots = 1000

    success_rates = list()

    for simulator in simulators:
        try:
            results = simulation.simulate_full(simulator, bitstring, package_length, shots, [])
            success = mean(list(get_success_rate(bitstring, result) for result in results))
            print(f"{simulator.backend_name}: {success}")
            success_rates.append(success)
        except Exception as inst:
            print(f"{inst}: {simulator.backend_name} does not work")
