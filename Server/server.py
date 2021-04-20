# coding: utf-8

import socket
import threading
import mysql.connector
import mysql.connector

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='exo4'
        )
        cursor = mydb.cursor()

        query = ("SELECT nom FROM client")
        cursor.execute(query)
        for (name) in cursor:
            print(name)

        print(mydb)

        print("Connexion de %s %s" % (self.ip, self.port,))

        r = self.clientsocket.recv(2048)
        print("Ouverture du fichier: ", r, "...")
        fp = open(r, 'rb')
        self.clientsocket.send(fp.read())

        print("Client déconnecté...")


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", 1111))

while True:
    tcpsock.listen(10)
    print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()