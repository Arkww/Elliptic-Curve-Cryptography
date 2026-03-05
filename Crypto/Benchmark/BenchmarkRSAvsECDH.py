# benchmark_RSA_vs_ECDH.py
import sys
import os
import time
import matplotlib.pyplot as plt

# Ajout des chemins pour les dossiers RSA et Crypto (celui contenant le benchmark ECDH)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "RSA")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Crypto")))

from BenchmarkRSA import benchmark_RSA, nb_bits_taille_rsa_cle
from BenchmarkECDH import benchmark_ECDH, nb_bits_taille_ecdh_cle

# Benchmark RSA
start_rsa = time.time()
benchmark_RSA()
end_rsa = time.time()
rsa_time = end_rsa - start_rsa

# Benchmark ECDH
start_ecdh = time.time()
benchmark_ECDH()
end_ecdh = time.time()
ecdh_time = end_ecdh - start_ecdh

# Affichage des tailles de clés
nb_bits_taille_rsa_cle()
nb_bits_taille_ecdh_cle()

# Get RSA key size (3072 bits) and ECDH key size (256 bits)
rsa_key_size = 3072  # RSA key size in bits
ecdh_key_size = 256  # ECDH key size in bits

# Plot the results with two y-axes
fig, ax1 = plt.subplots()

# Bar chart for execution times
ax1.bar('RSA', rsa_time, color='blue', width=0.4, label="RSA Time")
ax1.bar('ECDH', ecdh_time, color='green', width=0.4, label="ECDH Time")

ax1.set_xlabel('Algorithm')
ax1.set_ylabel('Time (seconds)', color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Create a second y-axis for key sizes
ax2 = ax1.twinx()
ax2.bar('RSA', rsa_key_size, color='blue', alpha=0.3, width=0.4, label="RSA Key Size")
ax2.bar('ECDH', ecdh_key_size, color='green', alpha=0.3, width=0.4, label="ECDH Key Size")

ax2.set_ylabel('Key Size (bits)', color='black')
ax2.tick_params(axis='y', labelcolor='black')

plt.title('Benchmark: RSA vs ECDH')
fig.tight_layout()  # Adjust layout to prevent clipping
plt.show()

