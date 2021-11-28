#Koddumdunya Chat Uygulaması
import socket
from threading import Thread


clients = {}
addresses = {}

SERVER = socket.gethostbyname(socket.gethostname())#'127.0.0.1' # localhost, IP adressi yerel, dyndns
PORT = int(input("PORT : "))
BUFFERSIZE = 1024
ADDR = (SERVER, PORT)
firstPlayer = [True]
print("It is your host ip : "+ SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def gelen_mesaj():
    while True:
        client, client_address = server.accept()
        print("%s:%s connected." %client_address)
        addresses[client] = client_address
        Thread(target=baglan_clien, args=(client,)).start()


def baglan_clien(client):

    isim = client.recv(BUFFERSIZE).decode("utf8")
    print(isim)
    clients[client] = isim
    if firstPlayer[0]:
        yayin(bytes("first ","utf8"))
        firstPlayer[0] = False
    while True:
        msg = client.recv(BUFFERSIZE)
        yayin(msg)


def yayin(msg):
    
    for yayim in clients:
        if firstPlayer[0]:
            yayim.send(bytes("first ","utf8"))
            firstPlayer[0] = False
        yayim.send(bytes(msg))

if __name__ == "__main__":
    server.listen(2) 
    print("Connection is waited ...")
    ACCEPT_THREAD = Thread(target=gelen_mesaj())
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()