#Client bağlantısı
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def gonder(event=None):
    msg = mesajim.get()
    mesajim.set("")
    client_socket.send(bytes(msg,"utf8"))
    if msg == "{cikis}":
        client_socket.close()
        app.quit()

def gelen_mesaj():
    while True:
        try:
            msg = client_socket.recv(BUFFERSIZE).decode("utf8")
            mesaj_listesi.insert(tkinter.END, msg)
        except:
            break

def cikis_durumu(event=None):
    mesajim.set("{cikis}")
    gonder()

# App Arayüzü

app = tkinter.Tk()
app.title("Koddunyan.net Chat")

mesaj_alani = tkinter.Frame(app)
mesajim = tkinter.StringVar()
mesajim.set("Mesajinizi giriniz...")
scrollbar = tkinter.Scrollbar(mesaj_alani)
mesaj_listesi = tkinter.Listbox(mesaj_alani, height=20, width=70, yscrollcommand=scrollbar.set)
mesaj_listesi.see("end")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
mesaj_listesi.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
mesaj_alani.pack()
giris_alani = tkinter.Entry(app, textvariable=mesajim)
giris_alani.bind("<Return>", gonder)
giris_alani.pack()
gonder_buton = tkinter.Button(app, text="Gonder", command=gonder)
gonder_buton.pack()

app.protocol("WM_DELETE_WİNDOW", cikis_durumu)

HOST = '192.168.56.1'
PORT = 34231
BUFFERSIZE = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

if not PORT:
    PORT = 32456
else:
    PORT = int(PORT)

gelen_thread = Thread(target=gelen_mesaj)
gelen_thread.start()
tkinter.mainloop()
