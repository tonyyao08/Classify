
# https://soumilshah1995.blogspot.com/2019/04/server-and-client-send-actual-sensor.html
import socket
import threading
import time


HOST = '192.168.0.111'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


def my_client():
    #run client every 11 seconds
    threading.Timer(11, my_client).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))


#put file name here
        my = filename

#encode the filename
        my_inp = my.encode('utf-8')

#send filename
        s.sendall(my_inp)

        #data = s.recv(1024).decode('utf-8')
        #if we want some sort of confirmation message

        s.close()
        time.sleep(5)


if __name__ == "__main__":
    while 1:
        my_client()