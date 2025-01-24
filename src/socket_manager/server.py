"""
File Server

A high-performance and stable server implementation using asyncio to receive files
from clients. The server ensures data integrity and logs detailed transfer information.

Attributes:
    BUFFER_SIZE (int): Size of the buffer for reading data.
    TIMEOUT (int): Timeout in seconds for reading data.
"""

import asyncio
import logging

BUFFER_SIZE = 2**16
TIMEOUT = 60

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class FileServer:
    """
    Represents the file server for handling file transfers.

    Args:
        host (str): The IP address to bind the server to.
        port (int): The port number to listen on.

    Methods:
        read_with_timeout(stream_reader): Reads data from the stream with a timeout.
        handle_client(stream_reader, stream_writer): Handles incoming client connections and file transfers.
        start(): Starts the server and listens for incoming connections.
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def read_with_timeout(self, stream_reader):
        try:
            return await asyncio.wait_for(stream_reader.read(BUFFER_SIZE), TIMEOUT)
        except asyncio.TimeoutError:
            logging.error("Timeout while reading from stream")
            return None

    async def handle_client(
        self, stream_reader: asyncio.StreamReader, stream_writer: asyncio.StreamWriter
    ):
        try:
            # Read the filename
            file_name = await self.read_with_timeout(stream_reader)
            if file_name is None:
                return

            file_name = file_name.decode().strip()

            # Read the file size
            file_size_data = await self.read_with_timeout(stream_reader)
            if file_size_data is None:
                return

            try:
                file_size = int(file_size_data.decode().strip())
            except ValueError:
                logging.error(f"Invalid file size received: {file_size_data}")
                return

            logging.info(f"Receiving file: {file_name} with size {file_size} bytes")

            total_length = 0
            try:
                with open(file_name, "wb") as file:
                    while total_length < file_size:
                        data = await self.read_with_timeout(stream_reader)
                        if not data:
                            logging.error(
                                "Failed to receive file data. Incomplete transfer."
                            )
                            return
                        total_length += len(data)
                        file.write(data)

                if total_length == file_size:
                    logging.info(f"File '{file_name}' received successfully")
                    stream_writer.write(b"Success")
                else:
                    logging.error(
                        f"File size mismatch: expected {file_size}, got {total_length}"
                    )
                    stream_writer.write(b"Error")

                await stream_writer.drain()

            except FileNotFoundError:
                logging.error(f"File '{file_name}' not found or inaccessible.")
                stream_writer.write(b"File not found")
                await stream_writer.drain()

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            stream_writer.close()
            await stream_writer.wait_closed()

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        logging.info(f"Serving on {addr}")

        async with server:
            await server.serve_forever()
