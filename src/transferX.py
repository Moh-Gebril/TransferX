"""
TransferX

This script provides a command-line interface to send and receive files using
an efficient and stable socket implementation. It supports running as both
a server and a client.

Example usage:
    Start the server:
    python3 src/transferX.py --server --host "192.168.1.10" --port 1515

    Start the client to send a file:
    python3 src/transferX.py --client --file-path "src/test.pdf" --host "192.168.1.10" --port 1515
"""

import argparse
import asyncio
import os
from socket_manager.client import FileClient
from socket_manager.server import FileServer


def main():
    parser = argparse.ArgumentParser(
        description="TransferX command-line tool for reliable and efficient file transfer."
    )
    parser.add_argument("-s", "--server", action="store_true", help="Start the server.")
    parser.add_argument(
        "-c",
        "--client",
        action="store_true",
        help="Start the client and send a file.",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host IP address (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port", type=int, default=12345, help="Port number (default: 12345)."
    )
    parser.add_argument(
        "--file-path", type=str, help="Path of the file to send to the server."
    )

    args = parser.parse_args()

    if args.server:
        server = FileServer(args.host, args.port)
        asyncio.run(server.start())
    elif args.client:
        file_path = args.file_path
        if os.path.isfile(file_path):
            client = FileClient(args.host, args.port)
            asyncio.run(client.send_file(file_path))
        else:
            print(f"File '{file_path}' does not exist.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
