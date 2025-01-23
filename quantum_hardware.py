# from qiskit import QuantumCircuit
# from qiskit.quantum_info import SparsePauliOp
# from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
# from qiskit_ibm_runtime import EstimatorV2 as Estimator
# from qiskit_ibm_runtime import QiskitRuntimeService
#
# # Create a new circuit with two qubits
# qc = QuantumCircuit(2)
#
# # Add a Hadamard gate to qubit 0
# qc.h(0)
#
# # Perform a controlled-X gate on qubit 1, controlled by qubit 0
# qc.cx(0, 1)
#
# # Return a drawing of the circuit using MatPlotLib ("mpl"). This is the
# # last line of the cell, so the drawing appears in the cell output.
# # Remove the "mpl" argument to get a text drawing.
#
# observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
# observables = [SparsePauliOp(label) for label in observables_labels]


from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.primitives import PrimitiveResult
import circuit


class ExperimentResult:
    bitstring: str
    fidelity: float
    detailed_results: list[tuple[str, float]]

    def __init__(
        self, bitstring: str, fidelity: float, detailed_results: list[tuple[str, float]]
    ):
        self.bitstring = bitstring
        self.fidelity = fidelity
        self.detailed_results = detailed_results


# You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
def run(bitstring: str, package_size: int, shots: int = 1024) -> ExperimentResult:
    service = QiskitRuntimeService()
    backend = service.least_busy(operational=True, simulator=False)

    sampler = Sampler(backend)
    sampler.options.default_shots = shots

    circs = circuit.build_circuits(bitstring, package_size)

    circs_transpiled = list(transpile(circ, backend) for circ in circs)

    job = sampler.run(circs_transpiled)
    print(f"Job ID: {job.job_id()} on backend {backend.name}")
    results: PrimitiveResult = job.result()

    return _parse_job_result(results, package_size, shots)


def fetch_previous_job(job_id: str, package_size: int, shots: int = 1024):
    service = QiskitRuntimeService()

    job = service.job(job_id)
    results: PrimitiveResult = job.result()

    return _parse_job_result(results, package_size, shots)


def _parse_job_result(
    results: PrimitiveResult, package_size: int, shots: int = 1024
) -> ExperimentResult:
    candidates: list[tuple[str, float]] = []
    avg_fidelity: float = 0.0

    for result in results:
        counts = result.data.meas.get_counts()

        candidate: str = max(counts, key=counts.get)
        candidate_count: int = counts[candidate]
        fidelity: float = candidate_count / shots

        # get the average fidelity waited by the length of the candidate compared to the package_size
        avg_fidelity += fidelity * (len(candidate) / package_size)

        candidates.append((candidate, fidelity))

    avg_fidelity /= len(candidates)
    total_bitstring = "".join(candidate[0] for candidate in candidates)

    return ExperimentResult(total_bitstring, avg_fidelity, candidates)
