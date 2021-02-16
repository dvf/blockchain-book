import nacl.encoding
import nacl.signing

# Generate a new random private key for Bob (we call this a signing key)
bobs_private_key = nacl.signing.SigningKey.generate()

# Sign a message with it
signed = bobs_private_key.sign(b"Attack at Dawn")

# Obtain the verify key for a given signing key
bobs_public_key = bobs_private_key.verify_key

# Serialize the verify key to send it to a third party
bobs_public_key_hex = bobs_public_key.encode(encoder=nacl.encoding.HexEncoder)
