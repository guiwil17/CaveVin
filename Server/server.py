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
        mydb.close()
        cursor.close()


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
        mydb.close()
        cursor.close()


    def create_cave(self, label, Id_Personne):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='mywine'
        )

        cursor = mydb.cursor()
        query = ("INSERT INTO Cave VALUES(null, %s, %s)")

        try:
            cursor.execute(query, (label, Id_Personne))
            self.retour = {"status": 200, "valeurs": True}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg }
        mydb.close()
        cursor.close()


    def get_caves(self, id_utilisateur):

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='mywine'
        )

        cursor = mydb.cursor()
        query = ("SELECT label FROM Cave WHERE id_Personne = %s;")

        try:
            tab = []
            cursor.execute(query, (id_utilisateur,))
            for (label) in cursor:
                 tab.append(label[0])
            self.retour = {"status": 200, "valeurs": tab}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()


    def get_vins(self, id_utilisateur):

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='mywine'
        )

        cursor = mydb.cursor()
        query = ("SELECT Nom, Type, Notation, Echangeable, Année, Quantité, Image, label FROM Vin JOIN Cave on Cave.id_Cave = Vin.id_Cave WHERE id_Personne = %s;")

        try:
            tab = []
            cursor.execute(query, (id_utilisateur,))
            for (Nom, Type, Notation, Echangeable, Année, Quantité, Image, label) in cursor:
                 tab.append(
                     {"Nom": Nom, "Type": Type,"Notation": Notation, "Echangeable": Echangeable, "Année": Année, "Quantité": Quantité, "Image": Image, "label": label})
            self.retour = {"status": 200, "valeurs": tab}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

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
        elif (test['fonction'] == "get_vins"):
            self.get_vins(test['paramètres'][0])
        elif (test['fonction'] == "create_cave"):
            self.create_cave(test['paramètres'][0], test['paramètres'][1])
        elif (test['fonction'] == "get_caves"):
            self.get_caves(test['paramètres'][0])

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

