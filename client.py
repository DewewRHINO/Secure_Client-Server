import socket
import ssl
import threading

# Server configuration
HOST = '192.168.56.1'
PORT = 12345

# SSL context creation
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations("server.crt")

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            print(message)
        except ssl.SSLError as e:
            print(f"SSL error: {e}")
            break

# Main client code
def main():
    with socket.create_connection((HOST, PORT)) as client_socket:
        with context.wrap_socket(client_socket, server_hostname=HOST) as ssl_socket:
            threading.Thread(target=receive_messages, args=(ssl_socket,), daemon=True).start()

            while True:
                message = input()
                ssl_socket.sendall(message.encode())

if __name__ == "__main__":
    main()
