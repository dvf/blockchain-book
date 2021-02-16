import asyncio
from collections import deque
from time import time

import aiohttp
from aiohttp import ServerTimeoutError, ClientConnectorError
from sanic import Sanic
from sanic.log import logger
from sanic.response import json


INFO = {
    "version": "funcoin 0.1",
    "peers": [("ip", 2000)]
}

app = Sanic(name="funcoin")


class PeerManager:
    def __init__(self):
        self.peers = deque(maxlen=200)


    def add_peer(self, peer):
        if peer not in self.peers:
            self.peers.appendleft(peer)

    @staticmethod
    async def contact_peer(ip, port):
        try:
            async with app.client_session.get(f'http://{ip}:{port}/ping') as response:
                return await response.json()
        except (ServerTimeoutError, TimeoutError, ClientConnectorError):
            return

    async def schedule_peer_to_be_contacted(self, peer, delay=60):
        logger.info(f"Contacting peer {peer}")
        ip = peer[0]
        port = peer[1]

        attempt = 1
        while attempt < 4:
            logger.info(f"Attempting to contact peer {peer}")
            response = await self.contact_peer(ip, port)
            if not response:
                attempt += 1
                logger.warning(f"{peer} couldn't be contacted. Trying again in {delay * attempt}s")
                await asyncio.sleep(delay * attempt)
            else:
                attempt = 1  # Reset the number of attempts
                logger.info(f"{peer} contacted")
                self.peers.appendleft((time(), ip, port))
                await asyncio.sleep(delay)

        logger.warning(f"Giving up on contacting peer {ip}:{port} after {attempt} attempts")


@app.route("/ping", methods=["GET"])
async def hey(request):
    contacting_peer = (request.ip, request.port)

    # Add this peer to our set
    peer_manager.add_peer(contacting_peer)

    peers = list(set(peer_manager.peers) - {contacting_peer})

    # Somebody contacts us
    app.loop.create_task(peer_manager.schedule_peer_to_be_contacted(contacting_peer))
    return json({"version": "funcoin 0.1", "peers": peers})


@app.listener('before_server_start')
def init(app, loop):
    timeout = aiohttp.ClientTimeout(total=5)
    session = aiohttp.ClientSession(timeout=timeout)
    app.client_session = session


@app.listener('after_server_stop')
def finish(app, loop):
    loop.run_until_complete(app.client_session.close())
    loop.close()


if __name__ == "__main__":
    import sys

    port = sys.argv[1]
    peer_manager = PeerManager()

    app.run(host="0.0.0.0", port=int(port))
