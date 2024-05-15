import socket
import threading
import ssl
from termcolor import colored
import random

clients = {}
user_colors = {}  # Dictionary to hold username-color mappings
available_colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']  # Removed 'white'

def assign_color():
    """ Assigns a unique color to each new user. """
    if not available_colors:
        raise Exception("No more colors available")  # Handle case where more users than colors exist
    color = random.choice(available_colors)
    available_colors.remove(color)  # Remove the color from available pool to ensure uniqueness
    return color

def release_color(color):
    """ Releases a color back to the available pool when a user leaves. """
    available_colors.append(color)

def broadcast(message):
    """ Broadcasts a message to all clients. """
    for client in clients:
        try:
            client.send(message)
        except Exception as e:
            print(colored(f"Failed to send message to {clients[client]}: {e}", "red"))

def handle_client(client_socket, address):
    try:
        username = client_socket.recv(1024).decode('utf-8').strip()
        if username in clients.values():
            client_socket.send("This username is already taken. Please try another one.".encode('utf-8'))
            client_socket.close()
            return
        color = assign_color()
        user_colors[client_socket] = color
        clients[client_socket] = username
        print(colored(f"{username} has joined the chat.", color))

        welcome_message = colored(f"{username} has joined the chat!", color).encode('utf-8')
        broadcast(welcome_message)

        while True:
            message = client_socket.recv(1024)
            if message:
                # Do not append the username here, as it's already included by the client.
                formatted_message = colored(f"{message.decode('utf-8')}", color).encode('utf-8')
                broadcast(formatted_message)
            else:
                break
    except Exception as e:
        print(colored(f"Error with client {address}: {e}", "red"))
    finally:
        if client_socket in clients:
            leave_message = colored(f"{username} has left the chat.", color).encode('utf-8')
            broadcast(leave_message)
            print(colored(f"{username} connection closed.", "cyan"))
            release_color(user_colors[client_socket])  # Release the color back to the pool
            del user_colors[client_socket]
            del clients[client_socket]
            client_socket.close()

def setup_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='resources/server.crt', keyfile='resources/server.key')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 55656))
    server_socket.listen()
    return server_socket, context

def server_main():
    server_socket, ssl_context = setup_server()
    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_socket = ssl_context.wrap_socket(client_socket, server_side=True)
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()
    except Exception as e:
        print(colored(f"Server error: {e}", "red"))
    finally:
        server_socket.close()

if __name__ == "__main__":
    server_main()