import socket
import numpy as np
import encodings

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def my_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server Started waiting for client to connect ")
        s.bind((HOST, PORT))
        s.listen(5)
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:

                data = conn.recv(1024).decode('utf-8')

                if  str(data) == "Quit":
                    print("shutting down server ")
                    break



if __name__ == '__main__':
    while 1:
        my_server()
