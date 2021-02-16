import json
from time import time

from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey


def create_transaction(
    private_key: str, public_key: str, receiver: str, amount: int
) -> dict:
    """
    Creates a transaction from a sender's public key to a receiver's public key

    :param private_key: The Sender's private key
    :param public_key: The Sender's public key
    :param receiver: The Receiver's public key
    :param amount: The amount in cents
    :return: <dict> The transaction dict
    """

    tx = {
        "sender": public_key,
        "receiver": receiver,
        "amount": amount,
        "timestamp": int(time()),
    }
    tx_bytes = json.dumps(tx, sort_keys=True).encode("ascii")

    # Generate a signing key from the private key
    signing_key = SigningKey(private_key, encoder=HexEncoder)

    # Now add the signature to the original transaction
    signature = signing_key.sign(tx_bytes).signature
    tx["signature"] = HexEncoder.encode(signature).decode("ascii")

    return tx


def validate_transaction(tx: dict) -> bool:
    """
    Verifies that a given transaction was sent from the sender
    :param tx: The transaction dict
    :return: <bool>
    """

    public_key = tx["sender"]

    # We need to strip the "signature" key from the tx
    signature = tx.pop("signature")
    signature_bytes = HexEncoder.decode(signature)

    tx_bytes = json.dumps(tx, sort_keys=True).encode("ascii")

    # Generate a verifying key from the public key
    verify_key = VerifyKey(public_key, encoder=HexEncoder)

    # Attempt to verify the signature
    try:
        verify_key.verify(tx_bytes, signature_bytes)
    except BadSignatureError:
        return False
    else:
        return True
