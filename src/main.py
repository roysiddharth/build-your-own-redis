import socket

PORT = 6379

def main():
    server_socket = socket.create_server(("localhost", PORT))

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        with conn:
            buffer = b""
            
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                buffer += data
                if b"\r\n" in buffer:
                    command = buffer.decode().strip()
                    print(f"Received command: {command}")

                    if command.upper() == "PING":
                        conn.sendall(b"+PONG\r\n")
                    else:
                        conn.sendall(b"-ERR unknown command\r\n")

                    buffer = b"" # Clear buffer for next input

if __name__ == "__main__":
    main()