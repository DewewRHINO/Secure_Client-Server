import socket
import threading
import ssl
from termcolor import colored
import random

clients = {}  # Dictionary to hold connected clients and their sockets
user_colors = {}  # Dictionary to hold user-color mappings
usable_colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']  # List of available colors

def set_color():
    # sets a silly color for those who join in 
    if not usable_colors:
        raise Exception("No more colors available")
    color = random.choice(usable_colors)  # Randomly select a color
    usable_colors.remove(color)  # Remove the color from the available list
    return color

def remove_color(color):
    """ Removes a color back to the list when not being used """
    usable_colors.append(color)  # Add the color back to the available list

def show(message):
    # shows a message to its connected clients
    for client_socket in list(clients.keys()):  # Iterate over a copy of the keys to avoid modification during iteration
        try:
            client_socket.send(message)
        except Exception as e:
            print(colored(f"Failed to send message to {clients[client_socket]}: {e}", "red"))

def set_client(client_socket, address):
    # sets up communications with a client
    try:
        username = client_socket.recv(1024).decode('utf-8').strip()  # Receive username from client
        if username in clients.values():
            client_socket.send("This username is already taken. Please try another one.".encode('utf-8'))
            client_socket.close()
            return
        color = set_color()  # set a color to the user
        user_colors[client_socket] = color  # Map the user to their color
        clients[client_socket] = username  # Add the client to the dictionary of connected clients
        print(colored(f"{username} has joined the chat.", color))

        welcome_message = colored(f"{username} has joined the chat!", color).encode('utf-8')
        show(welcome_message)  # show a welcome message to all clients

        while True:
            message = client_socket.recv(1024)  # Receive message from client
            if message:
                formatted_message = colored(f"{username}: {message.decode('utf-8')}", user_colors[client_socket]).encode('utf-8')
                show(formatted_message)  # show the message to all clients
            else:
                break
    except Exception as e:
        print(colored(f"Error with client {address}: {e}", "red"))
    finally:
        if client_socket in clients:
            leave_message = colored(f"{username} has left the chat.", color).encode('utf-8')
            show(leave_message)  # show a leave message to all clients
            print(colored(f"{username} connection closed.", "cyan"))
            remove_color(user_colors[client_socket])  
            del user_colors[client_socket]  
            del clients[client_socket] 
            client_socket.close()  

def set_server():
    # Sets up the server socket and SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='resources/server.crt', keyfile='resources/server.key')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 55656))
    server_socket.listen()
    return server_socket, context

def s_main():
    server_socket, ssl_context = set_server()
    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_socket = ssl_context.wrap_socket(client_socket, server_side=True)
            threading.Thread(target=set_client, args=(client_socket, addr)).start()
    except Exception as e:
        print(colored(f"Server error: {e}", "red"))
    finally:
        server_socket.close()  

if __name__ == "__main__":
    s_main()
