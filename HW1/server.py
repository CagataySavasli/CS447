import socket
from threading import Thread

clients = {}
addresses = {}

SERVER = socket.gethostbyname(socket.gethostname())#'127.0.0.1' # localhost, IP adresi yerel, dyndns
PORT = 34231
BUFFERSIZE = 1024
ADDR = (SERVER, PORT)
print(SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def recv_msg():
    while True:
        client, client_address = server.accept()
        print("%s:%s connected." %client_address)
        addresses[client] = client_address
        Thread(target=conn_client, args=(client,)).start()


def conn_client(client):

    name = client.recv(BUFFERSIZE).decode("utf8")
    print(name)
    clients[client] = name
    while True:
        msg = client.recv(BUFFERSIZE)
        stream(msg)


def stream(msg):
    for st in clients:
        st.send(bytes(msg))

if __name__ == "__main__":
    try:
        server.listen(2)
        print("Connection is waited ...")
        ACCEPT_THREAD = Thread(target=recv_msg())
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except Exception as e:
        print("could not established a connection")
        server.close()