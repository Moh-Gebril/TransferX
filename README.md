# TransferX

## Overview

TransferX is a high-performance, professional-grade command-line utility built for efficient and reliable file transfers over a network.TransferX is designed to handle large file transfers with minimal latency and robust socket communication. Whether for simple file sharing or advanced transfer operations, TransferX provides a seamless and scalable solution for managing file transfers asynchronously.

## Features

- **Robust Socket Communication**: Ensures stable and reliable file transfers.
- **High Efficiency**: Optimized for performance using asynchronous I/O.
- **Cross-Platform**: Compatible with Linux, macOS, and Windows.
- **Easy to Use**: Simple command-line interface for both server and client operations.
- **Any File Type Support**: Transfer any type of file, including text, images, videos, and more.

## Usage

### Server

To start the server, run the following command:

```bash
python3 src/transferX.py --server --host "server-ip" --port port-number
```

- **`--server`**: Starts the server.
- **`--host`**: Specifies the IP address to bind the server (default: `127.0.0.1`).
- **`--port`**: Specifies the port to listen on (default: `12345`).

### Client

To send a file from the client to the server, run:

```bash
python3 src/transferX.py --client --file-path "path/to/file" --host "192.168.1.10" --port 1515
```

- **`--client`**: Starts the client.
- **`--file-path`**: Specifies the path of the file to send.
- **`--host`**: Specifies the server's IP address.
- **`--port`**: Specifies the server's port.

## Installation

Clone the repository:
   ```bash
   git clone https://github.com/Moh-Gebril/TransferX.git
   cd transferx
   ```

## How It Works

- The **server** listens for incoming connections and handles file reception using asynchronous streams.
- The **client** connects to the server and sends the file name, size, and data in sequential order.
- Both server and client implement timeouts and error handling to ensure a robust transfer process.

## File Structure

```plaintext
src/
├── transferX.py       # Main entry point for the tool
├── socket_manager/
│   ├── __init__.py       # Package initializer
│   ├── client.py         # Client implementation
│   └── server.py         # Server implementation
```

## Example Scenarios

### Example 1: Start a Server

1. Run the server on the target machine:
   ```bash
   python3 src/transferX.py --server --host "192.168.1.10" --port 8080
   ```
2. The server is now ready to receive files.

### Example 2: Send a File

1. On another machine, send a file to the server:
   ```bash
   python3 src/transferX.py --client --file-path "path/to/file" --host "192.168.1.10" --port 8080
   ```
2. The server will save the file in the same directory where it was started.

## Logging

Logs are automatically generated for both client and server operations to provide detailed insights into the transfer process. These logs include:

- File names and sizes being transferred.
- Connection status and errors.
- Completion status of file transfers.

## Future Enhancements

- **TLS Integration**: Enhance security by incorporating Transport Layer Security (TLS) for encrypted communication.
- **Encryption**: Secure file transfers with end-to-end encryption.
- **Resume Support**: Allow interrupted transfers to resume from the last completed byte.
- **Multiple Clients**: Handle concurrent file transfers from multiple clients.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to enhance the tool.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Built with the power of Python's `asyncio` library.

## Authors
Mohamed Gebril
