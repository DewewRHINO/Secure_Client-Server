import socket
import ssl
import threading
import sys
from termcolor import colored

def clearInstance():
    print("\033c", end="")  # Clear screen for both Windows and Unix systems

def intro_menu():
    clearInstance()
    print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "green"))
    print(colored("ʕっ•ᴥ•ʔっ Holay Molay Chat Room", "green"))
    print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "green"))
    print("Enter your username to join the chat room:")

def get_user():
    intro_menu()
    return input("Username: ")

def set_connection():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='resources/server.crt')
    context.load_cert_chain(certfile='client.crt', keyfile='client.key')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = context.wrap_socket(client_socket, server_side=False, server_hostname='chet.com')
    client.connect(('127.0.0.1', 55656))
    return client

def receive_messages(client, stop_event):
    while not stop_event.is_set():
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print("\r" + message + "\n> ", end='')
                sys.stdout.flush()
        except Exception as e:
            print(colored(f"An error occurred: {e}", "red"))
            stop_event.set()

def send_messages(client, username, stop_event):
    while not stop_event.is_set():
        message = input("> ")
        if message.lower() == 'exit':
            client.send(f"{username} has left the chat.".encode('utf-8'))
            stop_event.set()
            break
        client.send(f"{username}: {message}".encode('utf-8'))

def main():
    client = set_connection()
    username = get_user()

    try:
        client.send(username.encode('utf-8'))
    except Exception as e:
        print(colored(f"Failed to send username: {str(e)}", "red"))
        client.close()
        return

    stop_event = threading.Event()
    threading.Thread(target=receive_messages, args=(client, stop_event)).start()
    send_messages(client, username, stop_event)

    try:
        stop_event.wait()
    finally:
        client.close()
        print(colored("Connection closed. Exiting...", "green"))

if __name__ == "__main__":
    main()
