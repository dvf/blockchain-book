import asyncio


class ConnectionPool:
    def __init__(self):
        self.connection_pool = set()

    def send_welcome_message(self, writer):
        """
        Sends a welcome message to a newly connected client
        """
        pass

    def broadcast(self, writer, message):
        """
        Broadcasts a general message to the entire pool
        """
        pass

    def broadcast_user_join(self, writer):
        """
        Calls the broadcast method with a "user joining" message
        """
        pass

    def broadcast_user_quit(self, writer):
        """
        Calls the broadcast method with a "user quitting" message
        """
        pass

    def broadcast_new_message(self, writer, message):
        """
        Calls the broadcast method with a user's chat message
        """
        pass

    def list_users(self, writer):
        """
        Lists all the users in the pool
        """
        pass

    def add_new_user_to_pool(self, writer):
        """
        Adds a new user to our existing pool
        """
        self.connection_pool.add(writer)

    def remove_user_from_pool(self, writer):
        """
        Removes an existing user from our pool
        """
        self.connection_pool.remove(writer)


async def handle_connection(reader, writer):
    writer.write("Hello new user, type something...\n".encode())

    data = await reader.readuntil(b"\n")

    writer.write("You sent: ".encode() + data)
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
