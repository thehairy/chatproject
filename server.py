# Script for the Server

# Imports
import socket
import select
import sys
import _thread as thread

# Check arguments
if len(sys.argv) != 3:
    print("Please provide an IP address and port.")
    exit()

# Save IP and Port
ip_address = str(sys.argv[1])
port = int(sys.argv[2])

# Create the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip_address, port))
server.listen(2)                                                  # Maximum of 100 client connections

client_list = []

print('Chat-Server on IP ' + ip_address + ':' + str(port) + ' started!')


def clientthread(connection, address):
    # Welcome Message
    connection.send("Welcome to this hairy chatroom!".encode())

    # Receive and send Messages
    while True:
        try:
            message = connection.recv(2048).decode()
            if message:
                send_message = "<" + address[0] + "> " + message
                # Log the message
                print(send_message)

                # Broadcast message
                broadcast(send_message, connection, address)
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
        print(address[0] + ' left')
        broadcast(address[0] + ' left', connection, address)


while True:
    # Accept connection
    conn, addr = server.accept()
    client_list.append(conn)

    # Log new connection
    print(addr[0] + " connected")
    broadcast(addr[0] + ' joined', conn, addr)

    # Start thread for each client
    thread.start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()
