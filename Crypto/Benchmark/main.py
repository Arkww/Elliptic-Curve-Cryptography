import matplotlib.pyplot as plt
from benchmark import benchmark_crypto, get_key_sizes
from crypto import ECCEncryption, RSAEncryption
from cryptography.hazmat.primitives.asymmetric import ec

def plot_comparison(title, metric, name1, name2, benchmarks):
    """ Generates a chart comparing a single type of time (e.g., encryption, decryption, key generation) """
    time1 = benchmarks[name1][metric]
    time2 = benchmarks[name2][metric]
    times = [time1, time2]

    # Create the chart
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([name1, name2], times, color=['blue', 'green'])
    ax.set_ylabel("Time (seconds)")
    ax.set_title(title)

    # Calculate the speed factor
    if time1 < time2:
        speedup_factor = time2 / time1
        speed_text = f"{name1} is approximately {speedup_factor:.1f}x faster than {name2}"
    else:
        speedup_factor = time1 / time2
        speed_text = f"{name2} is approximately {speedup_factor:.1f}x faster than {name1}"

    # Add text below the chart
    plt.subplots_adjust(bottom=0.2)
    ax.text(0.5, -0.15, speed_text, ha="center", fontsize=12, fontweight="bold", transform=ax.transAxes)

    plt.tight_layout()
    plt.show()

def plot_key_size_comparison(key_sizes):
    """ Chart comparing private and public key sizes """
    labels = key_sizes.keys()
    private_sizes = [key_sizes[label][0] for label in labels]
    public_sizes = [key_sizes[label][1] for label in labels]

    x = range(len(labels))
    width = 0.3

    plt.figure(figsize=(10, 5))
    plt.bar([i - width / 2 for i in x], private_sizes, width=width, label='Private key', color='red')
    plt.bar([i + width / 2 for i in x], public_sizes, width=width, label='Public key', color='orange')

    plt.xticks(x, labels, rotation=45, ha='right')
    plt.ylabel("Size (bytes)")
    plt.title("Key Size Comparison")
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    message = "salétaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAAAAAAAAAAAAAAAAAAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    num_iterations = 10

    test_cases = {
        "ECC (256 bits)": {"class": ECCEncryption, "params": {"curve": ec.SECP256R1()}},
        "RSA (3072 bits)": {"class": RSAEncryption, "params": {"key_size": 3072}}
    }

    benchmarks = {}
    key_sizes = {}

    for name, test in test_cases.items():
        print(f"Running benchmark for {name}...")
        benchmarks[name] = benchmark_crypto(test["class"], message, num_iterations, **test["params"])
        instance = test["class"](**test["params"])
        key_sizes[name] = get_key_sizes(instance)

    # ECC vs RSA comparisons
    pairs = [("ECC (256 bits)", "RSA (3072 bits)")]

    for name1, name2 in pairs:
        plot_comparison(f"Total time ({name1} vs {name2})", "total_time", name1, name2, benchmarks)

    # Key size comparison
    plot_key_size_comparison(key_sizes)

if __name__ == "__main__":
    main()
