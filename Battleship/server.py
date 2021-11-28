#Koddumdunya Chat Uygulaması
import socket
from threading import Thread

clients = {}
addresses = {}

SERVER = socket.gethostbyname(socket.gethostname())#'127.0.0.1' # localhost, IP adressi yerel, dyndns
PORT = 34000
BUFFERSIZE = 1024
ADDR = (SERVER, PORT)
print(SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def gelen_mesaj():
    """Gelen mesajların kontrolünü sağlayan fonksiyondur."""
    while True:
        client, client_address = server.accept()
        print("%s:%s bağlandı." %client_address)
        client.send(bytes("Kodunyam.net Chat Uygulaması! \n"+
                          "Lütfen adınızı giriniz: ", "utf8"))
        addresses[client] = client_address
        Thread(target=baglan_clien, args=(client,)).start()


def baglan_clien(client):
    """Client baglanmasini sorgular."""
    isim = client.recv(BUFFERSIZE).decode("utf8")
    hosgeldin = "Hoşgeldin %s! Cikmak için {cikis} yaziniz!" %isim
    client.send(bytes(hosgeldin,"utf8"))
    msg = "%s Chat Kanalına baglandi !" %isim
    yayin(bytes(msg, "utf8"))
    clients[client] = isim
    while True:
        msg = client.recv(BUFFERSIZE)
        if msg != bytes("{cikis}", "utf8"):
            yayin(msg, isim + ": ") # Ahmet:
        else:
            client.send("{cikis}","utf8")
            client.close()
            del clients[client]
            yayin(bytes("%s Kanaldan cikis yapti." %isim, "utf8"))
            break

def yayin(msg, kisi=""):
    for yayim in clients:
        yayim.send(bytes(kisi, "utf8")+msg)

if __name__ == "__main__":
    server.listen(10) # Max 10 baglantiya izin verir
    print("Baglanti bekleniyor ...")
    ACCEPT_THREAD = Thread(target=gelen_mesaj())
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()