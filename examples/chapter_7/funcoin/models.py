class Block:
    def __init__(
        self,
        mined_by,
        transactions,
        height,
        difficulty,
        hash,
        previous_hash,
        nonce,
        timestamp,
    ):
        self.mined_by = mined_by
        self.transactions = transactions
        self.height = height
        self.difficulty = difficulty
        self.hash = hash
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = timestamp


class Peer:
    def __init__(self, ip, port, last_seen):
        self.ip = ip
        self.port = port
        self.last_seen = last_seen


class Ping:
    def __init__(self, block_height, peer_count, is_miner):
        self.block_height = block_height
        self.peer_count = peer_count
        self.is_miner = is_miner


class Transaction:
    def __init__(self, hash, sender, receiver, signature, timestamp, amount):
        self.hash = hash
        self.sender = sender
        self.receiver = receiver
        self.signature = signature
        self.timestamp = timestamp
        self.amount = amount
