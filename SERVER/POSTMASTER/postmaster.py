
import socket
import sys
from CLI_USER_INPUT.userInput import cli
import threading 



HOST = ''
PORT = 8020

def handle_client(conn, address):
    print('Connected with ' + address[0] + ':' + str(address[1]))
    with conn:

        file = conn.makefile('r')
        conn.sendall(b'>> ')  # prompt before first input

        while True:
            line = file.readline()
            if not line:
                print('Client disconnected')
                break
                        
                        
            message = line.strip()
            print(f'Received: {message}')
            response = cli(message)

            if message.lower() == 'quit':
                break
            
            conn.sendall(f' {response}\n'.encode())


            #conn.sendall(message.encode())
            conn.sendall(b'>> ')  # prompt before first input




def create_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Deals with cases when port is time waiting after code is exited


    try:
        soc.bind((HOST,PORT))
    except socket.error as message:
        print(f'Bind failed. Error Code: {message.errno} Message: {message.strerror}')
        sys.exit()

    print('Socket binding operation completed')

    soc.listen(9)
    

    while True:
        conn,address = soc.accept()
        t = threading.Thread(target=handle_client, args=(conn, address), daemon=True) #Daemon=True close any threading in a weird state)
        t.start()
