import asyncio


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


asyncio.run(main())
