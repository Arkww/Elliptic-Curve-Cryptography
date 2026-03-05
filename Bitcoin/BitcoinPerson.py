import random
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Point import Point
import os
import hashlib
import base58


class BitcoinPerson:

    def __init__(self, curve, name):
        self.name = name
        self.curve = curve
        self.private_key = None
        self.public_key = None
        self.bitcoin_address = None


    def generate_private_key(self):
        """Generates the base private key for creating a Bitcoin address, 32 bytes format"""
        key = random.randint(1, self.curve.ordre - 1)
        self.private_key = key.to_bytes(32, 'big')


    def private_key_to_public_key(self):
        """Computes the public key from the private key using secp256k1."""
        private_key_int = int.from_bytes(self.private_key, 'big')  # Convert to integer
        point = self.curve.mult_scalaire(private_key_int, self.curve.points[1])
        if point is None:
            raise ValueError("The point is at infinity")
        x, y = point
        x_bytes = x.to_bytes(32, 'big')
        y_bytes = y.to_bytes(32, 'big')
        # Prefix 0x04 for an uncompressed public key
        return b'\x04' + x_bytes + y_bytes

    def double_hash(self, public_key):
        """Performs SHA-256 followed by RIPEMD-160."""
        sha256_hash = hashlib.sha256(public_key).digest()
        return hashlib.new('ripemd160', sha256_hash).digest()

    def base58check_encode(self,prefixed_hash):
        """Adds a checksum (double SHA-256 at the end of the address) and encodes in Base58Check."""
        checksum = hashlib.sha256(hashlib.sha256(prefixed_hash).digest()).digest()[:4]
        return base58.b58encode(prefixed_hash + checksum).decode()

    def generate_bitcoin_address(self):
        """Generates a valid Bitcoin address."""
        # Generate the private key
        self.generate_private_key()

        # Get the public key in uncompressed format
        public_key = self.private_key_to_public_key()

        # Store the key in uncompressed format, it will be used for verification
        self.public_key = public_key

        # Hash with SHA-256 then RIPEMD-160
        public_key_hash = self.double_hash(public_key)

        # Add the prefix (0x00 for Bitcoin mainnet)
        prefixed_hash = b'\x00' + public_key_hash

        # Encode in Base58Check and add the checksum suffix
        self.bitcoin_address = self.base58check_encode(prefixed_hash)


    def compute_transaction_hash(self,transaction_data):
        # Transaction hash
        sha256_hash = hashlib.sha256(transaction_data.encode('utf-8')).hexdigest()
        return sha256_hash


    # Compute the signature with ECDSA
    def ecdsa_sign(self, transaction_hash, curve):
        # Compute the transaction hash
        z = int(transaction_hash, 16)  # Convert to integer

        # Generate a random number k
        k = random.randint(1, curve.ordre-1)

        # Compute r = (k * G) % n
        r = (k * curve.Gx) % curve.ordre

        private_key_int = int.from_bytes(self.private_key, 'big')
        # Compute s = (k^-1 * (z + r * d)) % n
        k_inv = pow(k,-1, curve.ordre)  # k^-1 modulo n
        s = (k_inv * (z + r * private_key_int)) % curve.ordre

        return r, s

    def ecdsa_verify(self, transaction_hash, signature, curve, public_key):
        """Signature verification function"""
        r, s = signature  # Retrieve r and s values
        if not (1 <= r < curve.ordre and 1 <= s < curve.ordre):
            return False  # Bounds check for r and s

        # Convert the hash to integer
        z = int(transaction_hash, 16)

        # Compute w = s^(-1) mod n
        w = pow(s, -1, curve.ordre)

        # Compute u1 = (z * w) mod n and u2 = (r * w) mod n
        u1 = (z * w) % curve.ordre
        u2 = (r * w) % curve.ordre

        # Retrieve the public key point of the sender
        x = int.from_bytes(self.public_key[1:33], "big")
        y = int.from_bytes(self.public_key[33:], "big")
        Q = Point(x,y,"Q")

        # Compute the point P = u1 * G + u2 * Q (public key)
        x1, y1 = curve.mult_scalaire(u1, curve.G)  # u1 * G
        x2, y2 = curve.mult_scalaire(u2, Q)  # u2 * Q

        x, y = curve.addition((x1, y1), (x2, y2))  # Sum of points

        # Check if r' = x mod n equals r
        if x % curve.ordre == r:
            print("Valid signature")
            return True
        else:
            print("Invalid signature")
            return False



    def generate_fictive_transaction(self, recipient_address):
        """Generates a fictitious Bitcoin transaction"""
        transaction = {
            "version": 1,
            "inputs": [{
                "txid": 00000, # Previous transaction ID
                "vout": 11111, # Output index in the previous transaction
                "scriptSig": "",
                "sequence": 4294967295
            }],
            "outputs": [{
                "value": 0.1, # Amount to send in BTC
                "n": 0,
                "scriptPubKey": recipient_address # Recipient address
            }],
            "locktime": 0
        }
        return str(transaction)
