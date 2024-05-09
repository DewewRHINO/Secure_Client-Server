import socket
import ssl
import threading

# Server configuration
HOST = '192.168.56.1'
PORT = 12345
BACKLOG = 10

# SSL context creation
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Shared data
clients = []

# Function to handle client messages
def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"Received message: {message}")
            broadcast(message, client_socket)
        except ssl.SSLError as e:
            print(f"SSL error: {e}")
            break

# Function to broadcast messages to all clients
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.sendall(message.encode())
            except ssl.SSLError as e:
                print(f"SSL error: {e}")
                clients.remove(client)

# Main server code
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(BACKLOG)
        print(f"Server listening on {HOST}:{PORT}")

        with context.wrap_socket(server_socket, server_side=True) as ssl_socket:
            while True:
                client_socket, address = ssl_socket.accept()
                print(f"Connected to {address}")
                clients.append(client_socket)

                # Start a new thread for each client
                threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    main()
