#FRANCOIS Liu

import socket, threading, time, Crypto.Util.number
from tkinter import *


sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
xobs = [sbox.index(i) for i in range(16)]

def round(k, s):
    return sbox[(k ^ s)]

def back_round(k, s):
    return xobs[s] ^ k 

def enc(k, m):
    t = round(k[0], m)
    c = round(k[1], t)
    return c

def dec(k, m):
    t = back_round(k[1], m)
    c = back_round(k[0], t)
    return c

def enc_byte(k, s):
    s0 = s & 15
    s1 = s >> 4
    s0 = enc(k, s0)
    s1 = enc(k, s1)
    return (s0 + (s1 << 4))

def dec_byte(k, s):
    s0 = s & 15
    s1 = s >> 4
    s0 = dec(k, s0)
    s1 = dec(k, s1)
    return (s0 + (s1 << 4))

def chiffrer_cle(cle_rsa):
    s = ""
    for i in cle_rsa:
        s += chr(enc_byte([5, 11], ord(i)))
    return s

def dechiffrer_cle(cle_rsa):
    d = ""
    for i in cle_rsa:
        d += chr(dec_byte([5, 11], i))
    return d

def horaire():
    t=[time.localtime().tm_mday, time.localtime().tm_mon, time.localtime().tm_year, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec]
    return f"{t[0]}/{t[1]}/{t[2]} || {t[3]}h {t[4]}m {t[5]}s"


class S(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.l = []
        self.start()
        return

    def run(self):
        self.l.append(Messagerie())
        self.l[0].mainloop()


class Demande(Tk): 
    """ demande le nom """
    def __init__(self):
        super().__init__()
        self.name = ""
        self.dem = Entry(self)
        self.dem.place(x = 0, y = 0)
        self.b = Button(self, text = "send", command = self.stop)
        self.b.place(x = 100, y = 0)

    def stop(self):
        self.name = self.dem.get()
        self.quit()


class Messagerie(Tk):
    """affichage"""
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.configure(bg = "#1e1e1e")
        self.resizable(False, False)
        self.title("messagerie")
        self.msg = ""

        self.scroll = Scrollbar(self,width=1)
        self.scroll.place(x = 1200, y = 700)
        self.liste = Listbox(self, yscrollcommand = self.scroll.set, width = 200, height = 44, background = "#1e1e1e", fg = "white")

    def scrollbar(self, texte):
        self.liste.insert(END, texte)
        self.liste.place(x = 0, y = 0)


class Thread(threading.Thread):
    def __init__(self, name, name2, cle_pub, cle_pub2):
        threading.Thread.__init__(self)
        self.marche = True
        self.name = name
        self.name2 = name2
        self.cle_s = cle_pub
        self.cle_p2 = cle_pub2

        self.msg = Entry(Sta.l[0], width = 1200)
        self.msg.place(x = 0, y = 700)
        self.b = Button(Sta.l[0], text = "send", command = self.envoyer)
        self.b.place(x = 1200, y = 700)

    def recevoir(self):
        while self.marche:
            msg = my_socket.recv(1024)
            msg = self.dechiffrer_message(msg.decode())
            Sta.l[0].scrollbar(f"[{horaire()}]  {self.name2.decode()}: {msg}")

    def envoyer(self):
        Sta.l[0].scrollbar(f"[{horaire()}]  {self.name}: {self.msg.get()}")
        my_socket.sendall(bytes(str(self.chiffrer_message(str(self.msg.get()))), 'utf-8'))
        self.msg.delete(0, END)

    def run(self): #recevoir
        self.recevoir()

    def chiffrer_message(self, message):
        msg = int.from_bytes(message.encode('utf-8'), 'big')
        msg = pow(msg, self.cle_s[0], self.cle_s[1])
        msg = pow(msg, self.cle_p2[0], self.cle_p2[1])
        return msg

    def dechiffrer_message(self, message):
        m = pow(int(message), self.cle_s[0], self.cle_s[1])
        m = pow(int(m), self.cle_p2[0], self.cle_p2[1])
        return m.to_bytes((m.bit_length() + 7) // 8, 'big').decode('utf-8')



SERVER = "127.0.0.1"
PORT = 65432

p = Crypto.Util.number.getPrime(512)
q = Crypto.Util.number.getPrime(512)
if p != q:
    n = p * q
else:
    exit()
phi_n = (p - 1) * (q - 1)
e = 65537
assert(phi_n % e != 0)
d = pow(e, -1, phi_n)
cle_rsa = [(e, n), (d, n)]

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((SERVER, PORT))


Sta = S()

N = Demande()
N.mainloop()
name = N.name
my_socket.sendall(bytes(name, 'utf-8'))
my_socket.sendall(bytes(str(chiffrer_cle(str(cle_rsa[1][0]))), 'utf-8'))
my_socket.sendall(bytes(str(chiffrer_cle(str(cle_rsa[1][1]))), 'utf-8'))
name2 = my_socket.recv(1024)
cle2A = my_socket.recv(1024)
cle2B = my_socket.recv(1024)
cle2 = (int(dechiffrer_cle(cle2A)), int(dechiffrer_cle(cle2B)))
client = Thread(name, name2, cle_rsa[0], cle2) #Name A, Name B, cle_secrete A, cle_pub B
client.start()