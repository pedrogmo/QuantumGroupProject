import matplotlib.pyplot as plt
import matplotlib.image as mpimg

images_path = "images/hardware/sherbrooke/"

qubit_counts = [16, 32, 64, 80, 96, 100, 112, 126]

fig, axes = plt.subplots(2, 4, figsize=(16, 8))

axes = axes.flatten()

for ax, qubit_count in zip(axes, qubit_counts):
    img_path = f"{qubit_count}_qubits.png"

    img = mpimg.imread(images_path + img_path)
    ax.imshow(img)
    ax.axis('off')

    caption = f"{qubit_count} qubits" if qubit_count != 16 else "4-16 qubits"
    ax.text(0.5, -0.05, caption, fontsize=12, ha='center', transform=ax.transAxes)

for ax in axes[len(qubit_counts):]:
    ax.axis('off')


plt.tight_layout()
plt.show()
