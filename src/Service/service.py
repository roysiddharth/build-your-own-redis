import os
import socket

from Utility import handler, parseUtil
from DatabaseManager import database

PORT = int(os.environ.get("PORT"))

def run():
    database.load_data_from_mongodb()
    server_socket = socket.create_server(("localhost", PORT))  # Use port 6379

    print("Server is listening on port 6379...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        with conn:
            buffer = b""
            while True:
                data = conn.recv(1024)
                if not data:
                    break  # Client disconnected

                for byte in data:
                    if byte == 8:  # ASCII backspace character (\x08 or \b)
                        buffer = buffer[:-1]  # Remove the last byte from the buffer
                    else:
                        buffer += bytes([byte])

                # Check if the buffer contains a full command (ends with \r\n)
                if buffer.endswith(b'\r\n'):
                    # Parse the RESP-encoded data only when a full command is received
                    command = parseUtil.parse_resp(buffer)
                    print(f"Command ---> {command}")
                    if command:
                        handler.handle_command(command, conn)
                    
                    # Clear the buffer for the next command after processing
                    buffer = b""