import time
import os
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Benchmark.Person import Person

def benchmark_ECDH():
    print("ECDH benchmark:")
    # Création de la courbe P-256 (SECP256R1)
    curveCrypto = ec.SECP256R1()

    # Création des Personnes Alice et Bob
    alice = Person(curveCrypto, "alice")
    bob = Person(curveCrypto, "bob")

    # Calcul de la clé secrète partagée via ECDH
    alice_secret = alice.calcul_secret_key_ECDH(bob.public_key)
    bob_secret = bob.calcul_secret_key_ECDH(alice.public_key)

    # Vérification que les clés secrètes dérivées sont identiques
    if alice_secret != bob_secret:
        print("Erreur: les clés secrètes ne correspondent pas!")
    else:
        print("Les clés secrètes partagées sont identiques.")

    # ------ AES ------ #
    # La clé dérivée est déjà de 256 bits (pour AES-256)
    aes_key = alice_secret  

    plaintext = b"Message secret d'Alice vers Bob"
    nonce = os.urandom(12)

    # Chiffrement AES en mode GCM (Alice)
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag
    
    # Déchiffrement AES en mode GCM (Bob)
    cipher_dec = Cipher(algorithms.AES(aes_key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher_dec.decryptor()
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
    # print("Message déchiffré :", decrypted_text.decode())

    end = time.time()

def nb_bits_taille_ecdh_cle():
    print("ECDH key sizes:")
    # Utilisation de la courbe P-256 (SECP256R1)
    curveCrypto = ec.SECP256R1()
    
    # Création des Personnes Alice et Bob
    alice = Person(curveCrypto, "alice")
    bob = Person(curveCrypto, "bob")
    
    # Ecrire la taille des clés
    print("Taille de la clé publique d'Alice en bits: ", alice.public_key.x.bit_length() + alice.public_key.y.bit_length())
    print("Taille de la clé privée d'Alice en bits: ", alice.private_key.bit_length())
    print("Taille de la clé publique de Bob en bits: ", bob.public_key.x.bit_length() + bob.public_key.y.bit_length())
    print("Taille de la clé privée de Bob en bits: ", bob.private_key.bit_length())

