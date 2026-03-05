import time
from crypto import ECCEncryption, RSAEncryption, serialization
from cryptography.hazmat.primitives.asymmetric import ec

def benchmark_crypto(crypto_class, message, num_iterations=10, **params):
    start_key_gen = time.time()
    for _ in range(num_iterations):
        crypto_instance = crypto_class(**params)
    end_key_gen = time.time()
    key_gen_time = (end_key_gen - start_key_gen) / num_iterations

    crypto_instance = crypto_class(**params)
    start_encrypt = time.time()
    ciphertext = None
    for _ in range(num_iterations):
        ciphertext = crypto_instance.encrypt(message)
    end_encrypt = time.time()
    encrypt_time = (end_encrypt - start_encrypt) / num_iterations

    start_decrypt = time.time()
    for _ in range(num_iterations):
        _ = crypto_instance.decrypt(ciphertext)
    end_decrypt = time.time()
    decrypt_time = (end_decrypt - start_decrypt) / num_iterations

    return {
        'key_gen_time': key_gen_time,
        'encrypt_time': encrypt_time,
        'decrypt_time': decrypt_time,
        'total_time': key_gen_time + encrypt_time + decrypt_time
    }

def get_key_sizes(crypto_instance):
    private_size = len(crypto_instance.private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))
    public_size = len(crypto_instance.public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))
    return private_size, public_size
