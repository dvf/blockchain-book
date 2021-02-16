from funcoin.transactions import create_transaction, validate_transaction


def test_create_transaction(keys):
    tx = create_transaction(keys.private, keys.public, "someone", 123)

    assert tx["sender"] == keys.public
    assert tx["receiver"] == "someone"
    assert tx["amount"] == 123
    assert tx["timestamp"]
    assert tx["signature"]


def test_validate_valid_transaction(keys):
    tx = create_transaction(keys.private, keys.public, "someone", 123)

    assert validate_transaction(tx) is True


def test_validate_invalid_transaction(keys):
    tx = create_transaction(keys.private, keys.public, "someone", 123)

    # Forge it
    tx["amount"] = 1234

    assert validate_transaction(tx) is False
