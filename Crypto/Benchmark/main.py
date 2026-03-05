import matplotlib.pyplot as plt
from benchmark import benchmark_crypto, get_key_sizes
from crypto import ECCEncryption, RSAEncryption
from cryptography.hazmat.primitives.asymmetric import ec

def plot_comparison(title, metric, name1, name2, benchmarks):
    """ Génère un graphique comparant un seul type de temps (ex: chiffrement, déchiffrement, génération de clé) """
    time1 = benchmarks[name1][metric]
    time2 = benchmarks[name2][metric]
    times = [time1, time2]

    # Création du graphique
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([name1, name2], times, color=['blue', 'green'])
    ax.set_ylabel("Temps (secondes)")
    ax.set_title(title)

    # Calcul du facteur de rapidité
    if time1 < time2:
        speedup_factor = time2 / time1
        speed_text = f"{name1} est environ {speedup_factor:.1f}x plus rapide que {name2}"
    else:
        speedup_factor = time1 / time2
        speed_text = f"{name2} est environ {speedup_factor:.1f}x plus rapide que {name1}"

    # Ajouter le texte sous le graphique
    plt.subplots_adjust(bottom=0.2) 
    ax.text(0.5, -0.15, speed_text, ha="center", fontsize=12, fontweight="bold", transform=ax.transAxes)

    plt.tight_layout()
    plt.show()

def plot_key_size_comparison(key_sizes):
    """ Graphique comparant la taille des clés privées et publiques """
    labels = key_sizes.keys()
    private_sizes = [key_sizes[label][0] for label in labels]
    public_sizes = [key_sizes[label][1] for label in labels]

    x = range(len(labels))
    width = 0.3

    plt.figure(figsize=(10, 5))
    plt.bar([i - width / 2 for i in x], private_sizes, width=width, label='Clé privée', color='red')
    plt.bar([i + width / 2 for i in x], public_sizes, width=width, label='Clé publique', color='orange')

    plt.xticks(x, labels, rotation=45, ha='right')
    plt.ylabel("Taille (octets)")
    plt.title("Comparaison des tailles des clés")
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
        print(f"Exécution du benchmark pour {name}...")
        benchmarks[name] = benchmark_crypto(test["class"], message, num_iterations, **test["params"])
        instance = test["class"](**test["params"])
        key_sizes[name] = get_key_sizes(instance)

    # Comparaisons ECC vs RSA
    pairs = [("ECC (256 bits)", "RSA (3072 bits)")]

    for name1, name2 in pairs:
        plot_comparison(f"Temps total ({name1} vs {name2})", "total_time", name1, name2, benchmarks)

    # Comparaison des tailles de clé
    plot_key_size_comparison(key_sizes)

if __name__ == "__main__":
    main()
