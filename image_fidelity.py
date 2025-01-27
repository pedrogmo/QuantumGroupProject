import matplotlib.pyplot as plt

# Data
data = {
    "126 qubits": 0.0009718172983479105,
    "112 qubits": 0.0010044642857142856,
    "100 qubits": 0.002626008064516129,
    "96 qubits": 0.0017547607421875,
    "80 qubits": 0.004134537337662338,
    "64 qubits": 0.01025390625,
    "32 qubits": 0.15796915690104166,
    "16 qubits": 0.3507130940755208,
    "8 qubits": 0.6817105611165365,
    "4 qubits": 0.8736782073974609
}

# Extract keys and values
qubits = list(data.keys())
qubits.reverse()
fidelity = [value * 100 for value in data.values()]  # Convert to percentages
fidelity.reverse()

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(qubits, fidelity, marker='o', linestyle='-', color='b', label='Image Fidelity')

# Customize the plot
plt.title('Image Fidelity vs. Qubit Packet Size', fontsize=16)
plt.xlabel('Qubit Packet Size', fontsize=14)
plt.ylabel('Image Fidelity (%)', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.grid(alpha=0.5)
plt.legend(fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()
