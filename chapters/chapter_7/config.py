import json
from json.decoder import JSONDecodeError

import structlog
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey

logger = structlog.get_logger(__name__)


def generate_wallet():
    private_key = SigningKey.generate()
    public_key = private_key.verify_key
    payload = {
        "private_key": private_key.encode(encoder=HexEncoder).decode(),
        "public_key": public_key.encode(encoder=HexEncoder).decode(),
    }
    with open("wallet.json", "w") as file:
        json.dump(payload, file)
    logger.info("Generated new wallet: wallet.json")
    return payload


try:
    with open("wallet.json", "r") as file:
        keys = json.load(file)
    logger.info("Loaded keys from wallet.json")
except (JSONDecodeError, FileNotFoundError):
    keys = generate_wallet()

PRIVATE_KEY = keys["private_key"]
PUBLIC_KEY = keys["public_key"]
