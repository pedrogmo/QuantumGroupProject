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


from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# Create empty circuit
example_circuit = QuantumCircuit(2)
example_circuit.measure_all()

# You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)

sampler = Sampler(backend)
job = sampler.run([example_circuit])
print(f"job id: {job.job_id()}")
result = job.result()
print(result)