import socket

def test_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 6479))  # Adjust port if necessary

    client_socket.sendall(b'PING\r\n')
    response = client_socket.recv(1024)
    print("Response from server:", response.decode())

if __name__ == "__main__":
    test_client()
