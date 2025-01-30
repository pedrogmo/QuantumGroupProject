import numpy as np
from matplotlib import pyplot as plt

save_figs = False


def plot_preset(results_path: str, filename: str, x_label: str, x_ticks: list=None):
    # General method of plotting results
    data = np.loadtxt(results_path)
    variable = data[:,0]
    results = 100 * data[:,1]

    plt.figure()
    plt.tight_layout()
    plt.grid()
    if x_ticks is not None:
        plt.xticks(x_ticks)
    plt.xlabel(x_label)
    plt.ylabel("Accuracy (%)")
    plt.ylim(0, 105)
    plt.plot(variable, results, c="blue")
    plt.plot(variable, results, "o", c="blue")
    if save_figs:
        plt.savefig(f"results/figures/error_correction {filename}.pdf", bbox_inches="tight")
        plt.savefig(f"results/figures/error_correction {filename}.png", bbox_inches="tight")
    plt.show()


def plot_backends():
    # Plot the data of the accuracy of each backend
    data = np.loadtxt("results/backends.txt", dtype=str, delimiter=",")
    backends = data[:,0]
    results = 100 * np.array([float(result) for result in data[:,1]])

    args = np.argsort(results)[::-1]
    backends = backends[args]
    results = results[args]

    plt.figure()
    plt.tight_layout()
    plt.xticks(rotation=90)
    plt.ylabel("Accuracy (%)")
    plt.ylim(0, 100)
    plt.bar(backends, results)
    if save_figs:
        plt.savefig("results/figures/backend accuracy.pdf", bbox_inches="tight")
        plt.savefig("results/figures/backend accuracy.png", bbox_inches="tight")
    plt.show()


def plot_pre_encode_optimize():
    # Plot the data of the accuracy of encoding off/on of 24-bit strings with increasing '1' count
    data_off = np.loadtxt("results/FakeCusco/bit_flip_off.txt")
    data_on = np.loadtxt("results/FakeCusco/bit_flip_on.txt")
    bit_1_count = data_off[:,0]
    results_off = 100 * data_off[:,1]
    results_on = 100 * data_on[:,1]

    plt.figure()
    plt.tight_layout()
    plt.grid()
    plt.xlabel("1-bit count")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0, 105)
    plt.plot(bit_1_count, results_off, c="blue")
    plt.plot(bit_1_count, results_off, "o", label="Encoding: off", c="blue")
    plt.plot(bit_1_count, results_on, c="orange")
    plt.plot(bit_1_count, results_on, "o", label="Encoding: on", c="orange")
    plt.legend()
    if save_figs:
        plt.savefig("results/figures/error_correction bit flip.pdf", bbox_inches="tight")
        plt.savefig("results/figures/error_correction bit flip.png", bbox_inches="tight")
    plt.show()


def plot_package_length():
    # Plot the data of the accuracy of increasing package lengths
    plot_preset("results/FakeCusco/package_length.txt", "package length",
                "Package length", [0, 6, 12, 18, 24, 30])


def plot_repetitions():
    # Plot the data of the accuracy of increasing repetition counts
    plot_preset("results/FakeCusco/repetitions.txt", "repetitions",
                "Repetitions", [1, 3, 5, 7])


def main():
    plot_backends()
    plot_pre_encode_optimize()
    plot_package_length()
    plot_repetitions()


if __name__ == '__main__':
    main()
