# Secure_Client-Server

## Requirements: 
1. Download SSL whether it's from Choco or the executable it does not matter.

## Creating the Keys 
2. `openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt`
3. `openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt`

## Running the program
4. `python3 server.py`
5. `python3 client.py`

Note: If you are trying to connect multiple virtual machines you must change the socket in which it connects with. It is typically localhost, so for each file in server.py and client.py you would re-name them to the the IP Address of the server you are runnning. 
