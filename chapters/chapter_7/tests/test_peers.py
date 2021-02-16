from unittest.mock import patch, AsyncMock

import pytest

from funcoin.peers import P2PProtocol


@pytest.mark.asyncio
async def test_handle_ping(writer, server, ping_message):
    msg = ping_message(height=2)
    with patch.object(P2PProtocol, "send_message") as mock_send_message:
        p2p = P2PProtocol(server)

        await p2p.handle_ping(msg["message"], writer)

    assert mock_send_message.call_count == 1


@pytest.mark.asyncio
async def test_handle_ping_and_send_block(writer, server, ping_message):
    msg = ping_message(height=0)
    with patch.object(P2PProtocol, "send_message") as mock_send_message:
        p2p = P2PProtocol(server)

        await p2p.handle_ping(msg["message"], writer)

    assert mock_send_message.call_count == 2


@pytest.mark.asyncio
async def test_handle_transaction(writer, server, transaction_message):
    msg = transaction_message()
    with patch.object(P2PProtocol, "send_message") as mock_send_message:
        p2p = P2PProtocol(server)

        await p2p.handle_transaction(msg["message"], writer)

    assert mock_send_message.call_count > 0
    assert len(p2p.blockchain.pending_transactions) == 1


@pytest.mark.asyncio
async def test_handle_block(writer, server, block_message):
    msg = block_message()
    with patch.object(P2PProtocol, "send_message") as mock_send_message:
        p2p = P2PProtocol(server)

        await p2p.handle_block(msg["message"], writer)

    assert mock_send_message.call_count > 0
    assert len(p2p.blockchain.chain) > 1


@pytest.mark.asyncio
async def test_handle_peers(mocker, writer, server, peers_message):
    msg = peers_message()

    m = mocker.patch("funcoin.peers.asyncio")
    m.open_connection = AsyncMock()
    m.open_connection.return_value = mocker.Mock(), mocker.Mock()

    with patch.object(P2PProtocol, "send_message") as mock_send_message:
        p2p = P2PProtocol(server)

        await p2p.handle_peers(msg["message"], writer)

    assert mock_send_message.call_count > 0
    m.open_connection.assert_called()
    p2p.connection_pool.add_peer.assert_called()
