import sys

import EllipticFiniteCurve as ecf
import random
from Point import Point
import numpy as np

# Import modules for AES and HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
sys.path.append(os.path.abspath("Crypto/"))
from Benchmark.Person import Person

print("TEST CRYPTO: ")

# Create the curve and cyclic group
curveCrypto = ecf.EllipticFiniteCurve(-7, 10, 97)
generator_start_point = curveCrypto.generate_subgroup_start_point()
curveCrypto.add_point((generator_start_point[0], generator_start_point[1]))
subgroup = curveCrypto.generate_cyclic_subgroup(curveCrypto.points[1])
print("Generated subgroup:", str(subgroup))

# Create persons Alice and Bob
alice = Person(curveCrypto, "alice",len(subgroup))
bob = Person(curveCrypto,  "bob",len(subgroup))

# Display private and public keys
print("Alice private key:", alice.private_key)
print("Alice public key:", alice.public_key)
print("Bob private key:", bob.private_key)
print("Bob public key:", bob.public_key)

# Compute the shared secret key
alice_secret = alice.calcul_secret_key_ECDH(alice.private_key, bob.public_key)
print("Alice secret key:", alice_secret)
bob_secret = bob.calcul_secret_key_ECDH(bob.private_key, alice.public_key)

# Verify that the secret keys match


# ------ AES ------ #
shared_secret_int = alice_secret.x
byte_length = (shared_secret_int.bit_length() + 7) // 8
shared_secret_bytes = shared_secret_int.to_bytes(byte_length, 'big')

# Use HKDF to derive a 256-bit key for AES-256
hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
    backend=default_backend()
)
aes_key = hkdf.derive(shared_secret_bytes)
print("Derived AES key:", aes_key.hex())


plaintext = b"Secret message from Alice to Bob"

nonce = os.urandom(12)

# Create the AES cipher in GCM mode for encryption (Alice)
cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce), backend=default_backend())
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()
tag = encryptor.tag

print("Encrypted message:", ciphertext.hex())
print("Authentication tag:", tag.hex())
print("Nonce used:", nonce.hex())

# 3. AES decryption in GCM mode (Bob)
cipher_dec = Cipher(algorithms.AES(aes_key), modes.GCM(nonce, tag), backend=default_backend())
decryptor = cipher_dec.decryptor()
decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
print("Decrypted message:", decrypted_text.decode())
