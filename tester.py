import numpy as np
from qiskit_ibm_runtime import fake_provider as q_fp
from qiskit.transpiler import CircuitTooWideForTarget, TranspilerError
from matplotlib import pyplot as plt

import simulation


def bar_graph(x_axis, results):
    x_range = np.arange(len(x_axis))
    width = 0.2
    multiplier = 0

    fig, ax = plt.subplots(layout="constrained")

    for sim_type, measurement in results.items():
        offset = width * multiplier
        rects = ax.bar(x_range + offset, measurement, width, label=sim_type)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_ylabel("Success rate (%)")
    ax.set_title("Simulation success rate by method")
    ax.set_xticks(x_range + width, x_axis)
    ax.legend()
    plt.show()


def test_bit_flip():
    n = 8
    shots = 1000000
    messages = list((n - i) * "0" + i * "1" for i in range(n+1))
    messages = ["00000000", "00001111", "11111111"]

    results = {
        "Raw": [],
        "Bit flip": [],
        "Error correction": [],
        "Both": []
    }
    simulator = q_fp.FakeAlgiers()

    for message in messages:
        print(message)
        results_raw = simulation.simulate(simulator, message, 8, shots).count(message)
        results_flip = simulation.simulate_bit_flip(simulator, message, 8, shots).count(message)
        results_error = simulation.simulate_error_correction(simulator, message, 8, shots).count(message)
        results_both = simulation.simulate_both(simulator, message, 8, shots).count(message)
        results["Raw"].append(results_raw / shots * 100)
        results["Bit flip"].append(results_flip / shots * 100)
        results["Error correction"].append(results_error / shots * 100)
        results["Both"].append(results_both / shots * 100)


def test_provider():
    n = 8
    shots = 100000
    message = n * "0"

    providers = q_fp.FakeProviderForBackendV2().backends()
    providers = [q_fp.FakeAlgiers(), q_fp.FakeKolkataV2(), q_fp.FakeAuckland(), q_fp.FakeWashingtonV2()]
    results = {provider.backend_name: -1.0 for provider in providers}

    for provider in providers:
        print(provider.backend_name)
        try:
            message_results = simulation.simulate(provider, message, n, shots)
            results[provider.backend_name] = message_results.count(message) / shots * 100
        except CircuitTooWideForTarget:
            print(f"Warning: {provider.backend_name} does not support this many qubits.")
        except TranspilerError:
            print(f"Warning: {provider.backend_name} throws TranspilerError")

    results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
