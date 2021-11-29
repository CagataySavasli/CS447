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

def recev_msg():
    while True:
        client, client_address = server.accept()
        print("%s:%s connected." %client_address)
        addresses[client] = client_address
        Thread(target=connected_client, args=(client,)).start()


def connected_client(client):

    name = client.recv(BUFFERSIZE).decode("utf8")
    print(name)
    clients[client] = name
    if firstPlayer[0]:
        stream(bytes("first ","utf8"))
        firstPlayer[0] = False
    while True:
        msg = client.recv(BUFFERSIZE)
        stream(msg)


def stream(msg):
    
    for i in clients:
        if firstPlayer[0]:
            i.send(bytes("first ","utf8"))
            firstPlayer[0] = False
        i.send(bytes(msg))

if __name__ == "__main__":
    server.listen(2) 
    print("Connection is waited ...")
    ACCEPT_THREAD = Thread(target=recev_msg())
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()
