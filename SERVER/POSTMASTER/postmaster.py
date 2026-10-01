
import socket
import sys
from CLI_USER_INPUT.user_input import cli
import threading 
from datetime import date
from dotenv import load_dotenv
import os
from CLI_QUERY_DISTRIBUTER.cli_data_base_multi_server_file_distributer import multi_server_file_distributer



load_dotenv()

HOST = ''
PORT = 8020

def handle_client(conn, address):
    today = date.today()
    file_name = f'LOGS_{today}.txt'

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

            if "select" in message.lower():
                conn.sendall(response.replace("\n", "\r\n").encode("utf-8"))
                #print()
            else:
                conn.sendall(f' {response}\n'.encode())
                base = os.getenv("BASE_FILE_PATH") 

                with( open(f"{base}/LOGS/{file_name}","a",encoding="UTF_8") as log_file ):
                    new_label = f"{today} ---  {response} \n"
                    log_file.write(new_label)
                
            #print(multi_server_file_distributer())
            
                


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
