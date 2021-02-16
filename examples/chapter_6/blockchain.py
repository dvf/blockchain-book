import asyncio
import json
import math
import random
from hashlib import sha256
from time import time


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.target = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        # Create the genesis block
        print("Creating genesis block")
        self.chain.append(self.new_block())

    def new_block(self):
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'previous_hash': self.last_block["hash"] if self.last_block else None,
            'nonce': format(random.getrandbits(64), "x"),
            'target': self.target
        }

        # Get the hash of this new block, and add it to the block
        block_hash = self.hash(block)
        block["hash"] = block_hash

        # Reset the list of pending transactions
        self.pending_transactions = []

        return block

    @staticmethod
    def hash(block):
        # We ensure the dictionary is sorted or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last block in the chain (if there are blocks)
        return self.chain[-1] if self.chain else None

    def valid_block(self, block):
        # Check if a block's hash is less than the target...
        return block["hash"] < self.target

    def recalculate_target(self, block_index):
        """
        Returns the number we need to get below to mine a block
        """
        if block_index % 10 == 0:
            # We need to recalculate the target
            start = self.chain[-10]["timestamp"]
            end = self.chain[-1]["timestamp"]
            actual = end - start
            expected = 10 * 10  # no of secs expected between 10 blocks
            ratio = actual / expected
            print("ratio", ratio)
            ratio = max(0.25, ratio)
            ratio = min(4.00, ratio)
            print("ratio", ratio)
            # x current target by ratio
            new_target = int(self.target, 16) * ratio
            print(new_target)
            self.target = format(math.floor(new_target), "x").zfill(64)

        return self.target

    def get_blocks_after_timestamp(self, timestamp):
        for index, block in enumerate(self.chain):
            if timestamp < block["timestamp"]:
                return self.chain[index:]

    def get_mining_difficulty(self):
        # We adjust the difficulty every 10 blocks to ensure that we find 1 block every 10 seconds
        # Target is to mine 1 block every 10 seconds
        pass

    async def proof_of_work(self):
        self.recalculate_target(self.last_block["index"] + 1)
        while True:
            new_block = self.new_block()
            if self.valid_block(new_block):
                break

            await asyncio.sleep(0)

        self.chain.append(new_block)
        print("Found a new block: ", new_block)

    async def mine(self):
        while True:
            # Mine if we have transactions, else sleep for 10 seconds
            if len(self.pending_transactions) != 0:
                await self.proof_of_work()
            else:
                await asyncio.sleep(10)

# async def main():
#     bc = Blockchain()
#     await bc.mine()
#
# try:
#     asyncio.run(main())
# except KeyboardInterrupt:
#     print("Gracefully shutting down")
