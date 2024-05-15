# Secure_Client-Server
Secure Client Server Chat Application. 

$ openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
$ openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt

Make sure these are in the resources file.