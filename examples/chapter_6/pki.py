from nacl.public import PrivateKey, Box

# Generate Bob's private key, which must be kept secret
bobs_secret_key = PrivateKey.generate()
alices_secret_key = PrivateKey.generate()

# Bob's public key can be given to anyone wishing to send Bob an encrypted message
bobs_public_key = bobs_secret_key.public_key
# Alice does the same and then Alice and Bob exchange public keys
alices_public_key = alices_secret_key.public_key

# Bob wishes to send Alice an encrypted message so Bob must make a Box with his private key and Alice's public key
bobs_box = Box(bobs_secret_key, alices_public_key)

# This is our message to send, it must be a bytestring as Box will treat it
#   as just a binary blob of data.
secret_message = b"I am Satoshi"
encrypted = bobs_box.encrypt(secret_message)

# Alice creates a second box with her private key to decrypt the message
alices_box = Box(alices_secret_key, bobs_public_key)

# Decrypt our message, an exception will be raised if the encryption was
#   tampered with or there was otherwise an error.
plaintext = alices_box.decrypt(encrypted)
print(plaintext.decode('utf-8'))
