import socket
import ssl
import threading

def broadcast_messages(client_message, all_clients, sender_socket):
    for client_socket in all_clients:
        if client_socket is not sender_socket:
            try:
                client_socket.send(client_message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                close_client_connection(client_socket, all_clients)

def close_client_connection(client_socket, all_clients):
    if client_socket in all_clients:
        all_clients.remove(client_socket)
    client_socket.close()

def client_thread(client_socket, all_clients):
    try:
        client_socket.send(b'Welcome to the chat room!\n')
        while True:
            message = client_socket.recv(2048)
            if message:
                print(f"Broadcasting message: {message.decode('utf-8').strip()}")
                broadcast_messages(message, all_clients, client_socket)
            else:
                raise Exception("Client disconnected")
    except Exception as e:
        print(f"Client disconnected: {e}")
    finally:
        close_client_connection(client_socket, all_clients)




