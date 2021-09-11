# Script for the Server

# Imports
import socket
import sys
import _thread as thread

# Default IP and Port
ip_address = '127.0.0.1'
port = 6969

# Check arguments
if len(sys.argv) != 3:
    print('Using default IP and Port "127.0.0.1:4242"\nYou can specify an IP and Port while starting the client: '
          '"python3 script ip port"\n')
if len(sys.argv) == 3:
    ip_address = str(sys.argv[1])
    port = int(sys.argv[2])

# Create the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip_address, port))
server.listen(100)                                                  # Maximum of 100 client connections

client_list = []

print(f'Chat-Server on IP {ip_address}:{str(port)} started!')


def clientthread(connection, address):
    # Welcome Message
    connection.send('Welcome to this hairy chatroom!'.encode())

    # Receive and send Messages
    while True:
        try:
            message = connection.recv(2048).decode()
            if message:
                # Log the message
                print(message)

                # Broadcast message
                broadcast(message, connection, address)
            else:
                # Cut the connection
                remove(connection, address)
        except:
            continue


def broadcast(send_message, connection, address):
    for clients in client_list:
        if clients != connection:
            try:
                clients.send(send_message.encode())
            except:
                clients.close()
                remove(clients, address)


def remove(connection, address):
    if connection in client_list:
        client_list.remove(connection)
        print(f'{address[0]} left')
        broadcast(f'{address[0]} left', connection, address)


while True:
    # Accept connection
    conn, addr = server.accept()
    client_list.append(conn)

    # Log new connection
    print(f'{addr[0]} connected')
    broadcast(f'{addr[0]} joined', conn, addr)

    # Start thread for each client
    thread.start_new_thread(clientthread, (conn, addr))
