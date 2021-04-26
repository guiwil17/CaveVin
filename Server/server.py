# coding: utf-8

import socket
import threading
import mysql.connector
import mysql.connector
import json
import ast

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
        query = ("SELECT Id_Personne FROM personne WHERE Pseudo = %s AND Password = %s ")
        cursor.execute(query, (pseudo, password))


        for (Id_Personne) in cursor:
            self.retour = {"status": 200, "valeurs": Id_Personne[0]}


    def get_id_cave(self, id_personne, label):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='mywine'
        )

        cursor = mydb.cursor()
        print("Label")
        print(label)
        query = ("SELECT Id_Cave FROM cave WHERE label = %s AND Id_Personne = %s")
        id = -1;

        try:
            cursor.execute(query, (label, id_personne))
            for (Id_Cave) in cursor:
                self.retour = {"status": 200, "valeurs": Id_Cave[0]}
                id = Id_Cave[0]

        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()
        return id


    def create_account(self, nom, prenom, pseudo, telephone, password):

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
        query = ("SELECT Vin.Id_Vin, Nom, Type, Notation, Echangeable, Année, Quantité, Image, label FROM Vin JOIN Cave on Cave.id_Cave = Vin.id_Cave WHERE id_Personne = %s;")

        try:
            tab = []
            cursor.execute(query, (id_utilisateur,))
            for (Id_Vin, Nom, Type, Notation, Echangeable, Année, Quantité, Image, label) in cursor:
                 tab.append(
                     {"Nom": Nom, "Type": Type,"Notation": Notation, "Echangeable": Echangeable, "Année": Année, "Quantité": Quantité, "Image": Image, "label": label, "Id": Id_Vin})
            self.retour = {"status": 200, "valeurs": tab}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

    def filtre(self, id_utilisateur, valeurs):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='mywine'
        )
        tab = []

        cursor = mydb.cursor()
        if("Id_Cave" in valeurs):
            index = valeurs.index("Id_Cave")
            valeurs[index] = "Vin.Id_Cave"
            print(valeurs[index])
        if(len(valeurs) == 2):
            print(valeurs)
            query = ("SELECT Nom, Type, Notation, Echangeable, Année, Quantité, Image, label FROM Vin JOIN Cave on Cave.id_Cave = Vin.id_Cave WHERE id_Personne = %s AND " + valeurs[0] + " = %s;")
            try:

                cursor.execute(query, (id_utilisateur, valeurs[1]))
                for (Nom, Type, Notation, Echangeable, Année, Quantité, Image, label) in cursor:
                    print("bnbbbbbbbbbbbbbbbbb")
                    tab.append(
                        {"Nom": Nom, "Type": Type, "Notation": Notation, "Echangeable": Echangeable, "Année": Année,
                         "Quantité": Quantité, "Image": Image, "label": label})
                print(tab)
                self.retour = {"status": 200, "valeurs": tab}
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)
                self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        elif (len(valeurs) == 4):
            query = ("SELECT Nom, Type, Notation, Echangeable, Année, Quantité, Image, label FROM Vin JOIN Cave on Cave.id_Cave = Vin.id_Cave WHERE id_Personne = %s AND " + valeurs[0] + " = %s AND " + valeurs[2] + " = %s;")
            try:
                cursor.execute(query, (id_utilisateur, valeurs[1], valeurs[3]))
                for (Nom, Type, Notation, Echangeable, Année, Quantité, Image, label) in cursor:
                    tab.append(
                        {"Nom": Nom, "Type": Type, "Notation": Notation, "Echangeable": Echangeable, "Année": Année,
                         "Quantité": Quantité, "Image": Image, "label": label})
                    self.retour = {"status": 200, "valeurs": tab}
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)
                self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}

        elif (len(valeurs) == 6):
            query = ("SELECT Nom, Type, Notation, Echangeable, Année, Quantité, Image, label FROM Vin JOIN Cave on Cave.id_Cave = Vin.id_Cave WHERE id_Personne = %s AND " + valeurs[0] + " = %s AND " + valeurs[2] + " = %s AND " + valeurs[4] + " = %s;")
            try:
                cursor.execute(query, (id_utilisateur, valeurs[1], valeurs[3], valeurs[5]))
                for (Nom, Type, Notation, Echangeable, Année, Quantité, Image, label) in cursor:
                    tab.append(
                        {"Nom": Nom, "Type": Type, "Notation": Notation, "Echangeable": Echangeable, "Année": Année,
                         "Quantité": Quantité, "Image": Image, "label": label})
                    self.retour = {"status": 200, "valeurs": tab}
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)
                self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        else:
            query = (
                "SELECT Nom, Type, Notation, Echangeable, Année, Quantité, Image, label FROM Vin JOIN Cave on Cave.id_Cave = Vin.id_Cave WHERE id_Personne = %s AND " + valeurs[0] + " = %s AND " + valeurs[2] + " = %s AND " + valeurs[4] + " = %s AND " + valeurs[6] + " = %s;")
            try:
                cursor.execute(query, (id_utilisateur, valeurs[1], valeurs[3], valeurs[5], valeurs[7]))
                for (Nom, Type, Notation, Echangeable, Année, Quantité, Image, label) in cursor:
                    tab.append(
                        {"Nom": Nom, "Type": Type, "Notation": Notation, "Echangeable": Echangeable, "Année": Année,
                         "Quantité": Quantité, "Image": Image, "label": label})
                    self.retour = {"status": 200, "valeurs": tab}
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)
                self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}


    def get_random_id(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='mywine'
        )

        cursor = mydb.cursor()
        query = (
            "SELECT Utilisateur.Id_Personne, Pseudo FROM utilisateur  JOIN Personne on Personne.Id_Personne = utilisateur.Id_Personne ORDER BY RAND() LIMIT 1")

        try:
            cursor.execute(query)
            for (Id_Personne, Pseudo) in cursor:
               self.retour = {"status": 200, "valeurs": [Id_Personne,Pseudo]}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

    def ajouter_vin(self, nom, annee, type, cave, commentaire, image, echangeable, quantite, user_id ):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='mywine'
        )

        echange = False
        if(echangeable == 'True'):
            echange = True
        cursor = mydb.cursor()
        query = ("INSERT INTO Vin (Id_Vin,Nom,Type,Notation,Echangeable,Année,Quantité,Id_Cave, Image) VALUES(null, %s, %s, %s, %s, %s, %s, %s, %s)")

        id = self.get_id_cave(user_id, cave)
        try:
            cursor.execute(query, (nom, type, commentaire, echange, int(annee),  quantite, id,  image))
            self.retour = {"status": 200, "valeurs": True}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}



    def run(self):

        print("Connexion de %s %s" % (self.ip, self.port,))
        r = ""
        while 1:
            message = self.clientsocket.recv(10000000000)
            message = message.decode("utf-8")

            #test = json.loads(r)
            r = r + message
            if "}" in message:
                break

        test = json.loads(r)

        print(test)


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
        elif(test['fonction'] == "ajouter_vin"):
            self.ajouter_vin(test['paramètres'][0], test['paramètres'][1],test['paramètres'][2],test['paramètres'][3],test['paramètres'][4],test['paramètres'][5],test['paramètres'][6], test['paramètres'][7], test['paramètres'][8])
        elif (test['fonction'] == "get_random_id"):
            self.get_random_id()
        elif(test['fonction'] == "filtre"):
            self.filtre(test['paramètres'][0], test['paramètres'][1])
        elif (test['fonction'] == "get_id_cave"):
            print("ici")
            print(test['paramètres'][1])
            self.get_id_cave(test['paramètres'][0], test['paramètres'][1])
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

