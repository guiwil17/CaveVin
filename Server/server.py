# coding: utf-8

import socket
import threading
import mysql.connector
import mysql.connector
import json

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        self.retour = {"status": 500, "valeurs": "erreur"}
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def login(self, pseudo, password ):

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='mywine'
        )

        cursor = mydb.cursor()
        query = ("SELECT Nom FROM personne WHERE Pseudo = %s AND Password = %s ")
        cursor.execute(query, (pseudo, password))


        for (name) in cursor:
            self.retour = {"status": 200, "valeurs": True}
            print(name)

    def create_account(self, nom, prenom, pseudo, telephone, password):

        print(pseudo)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='mywine'
        )

        cursor = mydb.cursor()
        query = ("INSERT INTO Personne VALUES(null, %s, %s, %s, %s, %s)")

        try:
            cursor.execute(query, (nom, prenom, telephone, password, pseudo))
            self.retour = {"status": 200, "valeurs": True}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg }


    def run(self):

        print("Connexion de %s %s" % (self.ip, self.port,))

        r = self.clientsocket.recv(2048)

        r = r.decode("utf-8")


        test = json.loads(r)
        print(test['fonction'])
        if(test['fonction'] == "login"):
            self.login(test['paramètres'][0], test['paramètres'][1])
        elif(test['fonction'] == "create_account"):
            self.create_account(test['paramètres'][0], test['paramètres'][1],test['paramètres'][2],test['paramètres'][3],test['paramètres'][4])

        #for v in r :
         #   print(v)

        self.retour = json.dumps(self.retour)
        self.clientsocket.send(bytes(self.retour,encoding="utf-8"))

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

