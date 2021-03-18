# Script for the Client

# Imports
import socket
import select
import sys

# Check arguments
if len(sys.argv) != 4:
    print("Please provide the server IP, port and a name.")
    exit()

# Save IP and Port
ip_address = str(sys.argv[1])
port = int(sys.argv[2])
name = str(sys.argv[3])

# Connect to Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip_address, port))


while True:
    # List with possible input streams
    sockets_list = [sys.stdin, server]

    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048).decode()
            if message:
                print(message)
            else:
                print('Server connection dropped!')
                server.close()
                exit()
        else:
            message = sys.stdin.readline().replace('\n', '')
            if message == '/quit':
                print('Cutting connection...')
                exit()
            sys.stdout.write("<You> ")
            sys.stdout.write(message)
            sys.stdout.flush()
            server.sendto(message.encode(), (ip_address, port))

server.close()
