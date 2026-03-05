from BitcoinPerson import BitcoinPerson
from SECP256k1 import SECP256k1

# Create the secp256k1 curve
Secp256k1 = SECP256k1()

# Initialize persons
Mathieu = BitcoinPerson(Secp256k1,"Mathieu")
Theo = BitcoinPerson(Secp256k1,"Mathieu")

# Generate Bitcoin addresses for both persons
Mathieu.generate_bitcoin_address()
Theo.generate_bitcoin_address()
print("First person's address: " + str(Mathieu.bitcoin_address))
print("Second person's address: " + str(Theo.bitcoin_address))

# Generate the transaction hash from the fictitious transaction
transaction = Mathieu.generate_fictive_transaction(Theo.bitcoin_address)
hash_transaction = Mathieu.compute_transaction_hash(transaction)
print("Transaction hash: " + hash_transaction)

signature_mathieu = Mathieu.ecdsa_sign(hash_transaction,Secp256k1)
print("First person's signature: ", signature_mathieu)

# This doesn't work and I didn't have time to debug it unfortunately
Theo.ecdsa_verify(transaction_hash=hash_transaction,signature=signature_mathieu,curve = Secp256k1, public_key=Mathieu.public_key)
