import socket
import ssl
import sys
import threading

def receive_messages(secure_socket):
    while True:
        try:
            message = secure_socket.recv(2048)
            if message:
                print(message.decode('utf-8'))
            else:
                raise Exception("Server closed the connection")
        except Exception as e:
            print(f"Disconnected from server: {e}")
            secure_socket.close()
            sys.exit()
