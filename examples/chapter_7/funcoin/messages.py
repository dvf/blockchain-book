from marshmallow import Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema

from funcoin.schema import Peer, Block, Transaction, Ping


class PeersMessage(Schema):
    payload = fields.Nested(Peer(many=True))

    @post_load
    def add_name(self, data, **kwargs):
        data["name"] = "peers"
        return data


class BlockMessage(Schema):
    payload = fields.Nested(Block)

    @post_load
    def add_name(self, data, **kwargs):
        data["name"] = "block"
        return data


class TransactionMessage(Schema):
    payload = fields.Nested(Transaction)

    @post_load
    def add_name(self, data, **kwargs):
        data["name"] = "transaction"
        return data


class PingMessage(Schema):
    payload = fields.Nested(Ping)

    @post_load
    def add_name(self, data, **kwargs):
        data["name"] = "ping"
        return data


class MessageDisambiguation(OneOfSchema):
    type_field = "name"
    type_schemas = {
        "ping": PingMessage,
        "peers": PeersMessage,
        "block": BlockMessage,
        "transaction": TransactionMessage,
    }

    def get_obj_type(self, obj):
        if isinstance(obj, dict):
            return obj.get("name")


class MetaSchema(Schema):
    address = fields.Nested(Peer)
    client = fields.Str()


class BaseSchema(Schema):
    meta = fields.Nested(MetaSchema())
    message = fields.Nested(MessageDisambiguation)


def meta(ip, port, version="funcoin-0.1"):
    return {
        "client": version,
        "address": {"ip": ip, "port": port},
    }


def create_peers_message(external_ip, external_port, peers):
    return BaseSchema().dumps(
        {
            "meta": meta(external_ip, external_port),
            "message": {"name": "peers", "payload": peers},
        }
    )


def create_block_message(external_ip, external_port, block):
    return BaseSchema().dumps(
        {
            "meta": meta(external_ip, external_port),
            "message": {"name": "block", "payload": block},
        }
    )


def create_ping_message(external_ip, external_port, block_height, peer_count, is_miner):
    return BaseSchema().dumps(
        {
            "meta": meta(external_ip, external_port),
            "message": {
                "name": "ping",
                "payload": {
                    "block_height": block_height,
                    "peer_count": peer_count,
                    "is_miner": is_miner,
                },
            },
        }
    )


def create_transaction_message(external_ip, external_port, tx):
    return BaseSchema().dumps(
        {
            "meta": meta(external_ip, external_port),
            "message": {
                "name": "transaction",
                "payload": tx,
            },
        }
    )
