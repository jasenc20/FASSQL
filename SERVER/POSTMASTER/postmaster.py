
import socket
import sys
from CLI_USER_INPUT.userInput import cli
import threading 



HOST = ''
PORT = 8020

def handle_client(conn, address):
    print('Connected with ' + address[0] + ':' + str(address[1]))
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print('Client disconnected')
                break

            message = data.decode().strip()
            print(f'Received: {message}')

            if message.lower() == 'quit':
                break

            conn.sendall(message.encode())



def create_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        soc.bind((HOST,PORT))
    except socket.error as message:
        print(f'Bind failed. Error Code: {message.errno} Message: {message.strerror}')
        sys.exit()

    print('Socket binding operation completed')

    soc.listen(9)

    conn, address = soc.accept()

    print('Connected with '+ address[0] + 
            ':' + str(address[1]))
    

    while True:
        conn,address = soc.accept()
        t = threading.Thread(target=handle_client, args=(conn, address))
        t.start()
