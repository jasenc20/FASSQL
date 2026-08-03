
import socket
import sys
from CLI_USER_INPUT.userInput import cli



HOST = ''
PORT = 8020

def create_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
            soc.bind((HOST,PORT))
    except socket.error as message:
            print('Bind failed. Error Code: ' 
                + str(message[0])+ ' Message' + message[1])
            sys.exit()

    print('Socket binding operation completed')

    soc.listen(9)

    conn, address = soc.accept()

    print('Connected with '+ address[0] + 
            ':' + str(address[1]))
    
    while True:
        data = conn.recv(1024) #READ up to 1024 bytes from the client
        if not data:
            print('Client disconnected')
            break

        message = data.decode().strip()
        print(f'Received: {message}')

        if message.lower() == 'quit':
            break


        conn.sendall(message.encode())

    conn.close()
    soc.close()