#FRANCOIS Liu

import socket, threading, time

client=[]

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, nb):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.csocket = clientsocket
        self.nb = nb
        if nb == 0:
            self.autre = 1
        else:
            self.autre = 0

    def add_name(self, nom):
        self.name = nom

    def add_cle(self, cle):
        self.cle = cle

    def run(self):
        while True:
            data = self.csocket.recv(1024)
            client[self.autre].csocket.sendall(bytes(f"{str(data.decode())}", 'utf-8'))

def horaire():
    t=[time.localtime().tm_mday, time.localtime().tm_mon, time.localtime().tm_year, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec]
    return f"{t[0]}/{t[1]}/{t[2]} || {t[3]}h {t[4]}m {t[5]}s"

LOCALHOST = "127.0.0.1"
PORT = 65432
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Start")
while True:
    server.listen(1)
    if len(client) == 0:
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientAddress, clientsock, 0)
        name = clientsock.recv(1024)
        newthread.add_name(name.decode())
        cleA = clientsock.recv(1024)
        cleB = clientsock.recv(1024)
        cle = [cleA.decode(), cleB.decode()]
        newthread.add_cle(cle)
        client.append(newthread)

    elif len(client) == 1:
        clientsock1, clientAddress1 = server.accept()
        newthread1 = ClientThread(clientAddress1, clientsock1, 1)
        name1 = clientsock1.recv(1024)
        newthread1.add_name(name1.decode())
        cle1A = clientsock1.recv(1024)
        cle1B = clientsock1.recv(1024)
        cle1 = (cle1A.decode(), cle1B.decode())
        newthread1.add_cle(cle1)
        client.append(newthread1)
        clientsock1.sendall(bytes(client[0].name, 'utf-8'))
        clientsock1.sendall(bytes(client[0].cle[0], 'utf-8'))
        time.sleep(0.01)
        clientsock1.sendall(bytes(client[0].cle[1], 'utf-8'))
        clientsock.sendall(bytes(client[1].name, 'utf-8'))
        clientsock.sendall(bytes(client[1].cle[0], 'utf-8'))
        time.sleep(0.01)
        clientsock.sendall(bytes(client[1].cle[1], 'utf-8'))
        newthread.start()
        newthread1.start()

        print(f"Relation entre {client[0].name}({client[0].clientAddress}) et {client[1].name}({client[1].clientAddress})")
    else:
        break