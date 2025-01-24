"""
File Client

A lightweight and efficient client implementation using asyncio to send files
to a remote server. The client ensures reliable file transfer and logs detailed
information.

Attributes:
    BUFFER_SIZE (int): Size of the buffer for reading data.
    TIMEOUT (int): Timeout in seconds for reading data.
"""

import asyncio
import os
import logging

BUFFER_SIZE = 2**16
TIMEOUT = 60

logging.basicConfig(level=logging.INFO)


class FileClient:
    """
    Represents the file client for sending files to a server.

    Args:
        server_ip (str): The server's IP address.
        server_port (int): The server's port number.

    Methods:
        read_with_timeout(stream_reader): Reads data from the stream with a timeout.
        send_file(file_name): Sends a file to the connected server.
    """

    def __init__(self, server_ip: str, server_port: int):
        self.server_ip = server_ip
        self.server_port = server_port

    async def read_with_timeout(self, stream_reader):
        try:
            return await asyncio.wait_for(stream_reader.read(BUFFER_SIZE), TIMEOUT)
        except asyncio.TimeoutError:
            logging.error("Timeout while reading from server")
            return None

    async def send_file(self, file_name):
        try:
            stream_reader, stream_writer = await asyncio.wait_for(
                asyncio.open_connection(self.server_ip, self.server_port), timeout=5
            )
        except ConnectionRefusedError:
            logging.error("Connection refused by server.")
            return
        except asyncio.TimeoutError:
            logging.error("Connection timed out.")
            return
        except OSError as e:
            logging.error(f"OS error occurred: {e}")
            return

        try:
            # Added newline for clarity
            stream_writer.write(os.path.basename(file_name).encode() + b"\n")
            await stream_writer.drain()
            await asyncio.sleep(0.1)
            logging.info(f"Sent file name: {file_name}")

            file_size = str(os.stat(file_name).st_size)
            # Added newline for clarity
            stream_writer.write(file_size.encode() + b"\n")
            await stream_writer.drain()
            await asyncio.sleep(0.1)
            logging.info(f"Sent file size: {file_size}")

            with open(file_name, "rb") as file:
                while chunk := file.read(BUFFER_SIZE):
                    stream_writer.write(chunk)
                    await stream_writer.drain()
                    await asyncio.sleep(0.1)

            logging.info(f"File '{file_name}' sent successfully")

            response = await self.read_with_timeout(stream_reader)
            if response:
                response = response.decode().strip()
                if response == "Success":
                    logging.info("File transfer confirmed by server.")
                else:
                    logging.error("Error during file transfer.")

        except Exception as e:
            logging.error(f"Error while sending file: {e}")
        finally:
            stream_writer.close()
            await stream_writer.wait_closed()
