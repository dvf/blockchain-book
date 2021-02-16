import asyncio
from textwrap import dedent


class ConnectionPool:
    def __init__(self):
        self.connection_pool = set()

    def send_welcome_message(self, writer):
        message = dedent(f"""
        ===        
        ✨ Welcome {writer.nickname}!

        There are {len(self.connection_pool) - 1} user(s) here beside you
        ===
        """)

        writer.write(f"{message}\n".encode())

    def broadcast(self, writer, message):
        pass

    def broadcast_user_join(self, writer):
        pass

    def broadcast_user_quit(self, writer):
        pass

    def broadcast_new_message(self, writer, message):
        pass

    def list_users(self, writer):
        pass

    def add_new_user_to_pool(self, writer):
        self.connection_pool.add(writer)

    def remove_user_from_pool(self, writer):
        self.connection_pool.remove(writer)


async def handle_connection(reader, writer):
    # Get a nickname for the new client
    writer.write("> Choose your nickname: ".encode())

    response = await reader.readuntil(b"\n")
    writer.nickname = response.decode().strip()

    connection_pool.add_new_user_to_pool(writer)
    connection_pool.send_welcome_message(writer)
    await writer.drain()

    # Let's close the connection and clean up
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_connection, "0.0.0.0", 8888)

    async with server:
        await server.serve_forever()


connection_pool = ConnectionPool()
asyncio.run(main())
