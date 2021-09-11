# Script for the Client

# Imports
import datetime
import select
import socket
import sys
from playsound import playsound

# Default IP and Port
ip_address = '127.0.0.1'
port = 4242

# Check arguments
if len(sys.argv) != 3:
    print('Using default IP and Port "127.0.0.1:4242"\nYou can specify an IP and Port while starting the client: '
          '"python3 script ip port"\n')
if len(sys.argv) == 3:
    ip_address = str(sys.argv[1])
    port = int(sys.argv[2])

# Connect to Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip_address, port))

name = input('Please enter your name: ')

while True:
    # List with possible input streams
    sockets_list = [sys.stdin, server]

    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048).decode()
            if message:
                playsound('./res/beep.mp3')
                print(message)
            else:
                print('Server connection dropped!')
                server.close()
                exit()
        else:
            message = sys.stdin.readline().replace('\n', '')
            message = message.strip()

            if len(message) == 0:
                continue
            if message.lower() == '/quit':
                print('Cutting connection...')
                exit()
            if message.lower().startswith('/nickname') and len(message) > 10:
                name = message.split(' ')[1]
                continue

            date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            message = f'[{date_now}] {name}: {message}'
            sys.stdout.write(f'{message}\n')
            sys.stdout.flush()
            server.sendto(message.encode(), (ip_address, port))
