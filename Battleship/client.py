#Client bağlantısı
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time


def gonder(msg):
    msg = "Deneme "
    client_socket.send(bytes(msg,"utf8"))

def gelen_mesaj():
    while True:
        try:
            msg = client_socket.recv(BUFFERSIZE).decode("utf8")
            print(msg)
        except:
            break


HOST = input("Get host's IP : ")
PORT = 34000
BUFFERSIZE = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


gelen_thread = Thread(target=gelen_mesaj)
gelen_thread.start()

