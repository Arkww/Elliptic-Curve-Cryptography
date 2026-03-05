import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class ECCEncryption:
    def __init__(self, curve=ec.SECP256R1()):
        self.curve = curve
        self.private_key = ec.generate_private_key(curve, default_backend())
        self.public_key = self.private_key.public_key()

    def encrypt(self, message):
        if isinstance(message, str):
            message = message.encode('utf-8')

        shared_key = self.private_key.exchange(ec.ECDH(), self.public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'encryption',
            backend=default_backend()
        ).derive(shared_key)

        nonce = os.urandom(12)
        cipher = Cipher(algorithms.AES(derived_key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(message) + encryptor.finalize()
        tag = encryptor.tag

        return (nonce, ciphertext, tag)

    def decrypt(self, encrypted_data):
        nonce, ciphertext, tag = encrypted_data
        shared_key = self.private_key.exchange(ec.ECDH(), self.public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'encryption',
            backend=default_backend()
        ).derive(shared_key)

        cipher = Cipher(algorithms.AES(derived_key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()

        return decrypted.decode('utf-8')


class RSAEncryption:
    def __init__(self, key_size=3072):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def encrypt(self, message):
        if isinstance(message, str):
            message = message.encode('utf-8')

        return self.public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt(self, ciphertext):
        return self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode('utf-8')
