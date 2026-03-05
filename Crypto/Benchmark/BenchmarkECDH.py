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
    # Create the P-256 curve (SECP256R1)
    curveCrypto = ec.SECP256R1()

    # Create persons Alice and Bob
    alice = Person(curveCrypto, "alice")
    bob = Person(curveCrypto, "bob")

    # Compute shared secret key via ECDH
    alice_secret = alice.calcul_secret_key_ECDH(bob.public_key)
    bob_secret = bob.calcul_secret_key_ECDH(alice.public_key)

    # Verify that the derived secret keys are identical
    if alice_secret != bob_secret:
        print("Error: the secret keys do not match!")
    else:
        print("The shared secret keys are identical.")

    # ------ AES ------ #
    # The derived key is already 256 bits (for AES-256)
    aes_key = alice_secret

    plaintext = b"Secret message from Alice to Bob"
    nonce = os.urandom(12)

    # AES encryption in GCM mode (Alice)
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag

    # AES decryption in GCM mode (Bob)
    cipher_dec = Cipher(algorithms.AES(aes_key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher_dec.decryptor()
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()

    end = time.time()

def nb_bits_taille_ecdh_cle():
    print("ECDH key sizes:")
    # Using the P-256 curve (SECP256R1)
    curveCrypto = ec.SECP256R1()

    # Create persons Alice and Bob
    alice = Person(curveCrypto, "alice")
    bob = Person(curveCrypto, "bob")

    # Print key sizes
    print("Alice's public key size in bits: ", alice.public_key.x.bit_length() + alice.public_key.y.bit_length())
    print("Alice's private key size in bits: ", alice.private_key.bit_length())
    print("Bob's public key size in bits: ", bob.public_key.x.bit_length() + bob.public_key.y.bit_length())
    print("Bob's private key size in bits: ", bob.private_key.bit_length())

