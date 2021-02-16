import json
from collections import namedtuple
from hashlib import sha256
from time import time

import pytest

from funcoin.blockchain import Blockchain
from funcoin.messages import (
    create_peers_message,
    create_ping_message,
    create_transaction_message,
    create_block_message,
)
from funcoin.transactions import create_transaction


@pytest.fixture
def keys():
    return namedtuple("KP", ["private", "public"])(
        "c6cb8da9acedf03db25326f6aa99aa136e61031eec458736cd51b0527319c1bc",
        "b3ecab7644ac12eac3d548b6de410fda3754d528d360d1fbee0a34f4267ef8b9",
    )


@pytest.fixture
def blockchain():
    bc = Blockchain()
    bc.chain.append(bc.new_block())
    return bc


@pytest.fixture
def peer(faker):
    def w():
        return {
            "ip": faker.ipv4(),
            "port": faker.port_number(),
            "last_seen": faker.unix_time(),
        }

    return w


@pytest.fixture
def peers(peer):
    return [peer() for _ in range(0, 40)]


@pytest.fixture
def peers_message(peers, faker):
    def w(ip=faker.ipv4(), port=faker.port_number(), _peers=peers):
        return json.loads(create_peers_message(ip, port, _peers))

    return w


@pytest.fixture
def block(faker, tx):
    def w(
        height=10,
        mined_by="someone",
        transactions=10,
        previous_hash="something",
        nonce="123",
        target="fff",
        timestamp=int(time()),
    ):
        block = {
            "height": height,
            "mined_by": mined_by,
            "transactions": [tx() for _ in range(0, transactions)],
            "previous_hash": previous_hash,
            "nonce": nonce,
            "target": target,
            "timestamp": timestamp,
        }
        block_string = json.dumps(block, sort_keys=True).encode()
        block["hash"] = sha256(block_string).hexdigest()
        return block

    return w


@pytest.fixture
def block_message(block, faker):
    def w(ip=faker.ipv4(), port=faker.port_number()):
        return json.loads(create_block_message(ip, port, block()))

    return w


@pytest.fixture
def ping_message(faker):
    def w(
        ip=faker.ipv4(),
        port=faker.port_number(),
        height=faker.pyint(),
        peer_count=faker.pyint(),
        is_miner=faker.pybool(),
    ):
        return json.loads(create_ping_message(ip, port, height, peer_count, is_miner))

    return w


@pytest.fixture
def tx(keys):
    def w():
        return create_transaction(keys.private, keys.public, "someone", 123)

    return w


@pytest.fixture
def transaction_message(faker, tx):
    def w(ip=faker.ipv4(), port=faker.port_number()):
        return json.loads(create_transaction_message(ip, port, tx()))

    return w


@pytest.fixture
def server(mocker, peers, blockchain):
    server = mocker.Mock()
    server.blockchain = blockchain
    server.connection_pool.get_alive_peers.return_value = peers
    server.external_ip = "192.168.0.1"
    server.external_port = 8888

    return server


@pytest.fixture
def writer(mocker):
    w = mocker.Mock()
    w.is_miner = False
    return w
