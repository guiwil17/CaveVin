# coding: utf-8

import socket
import threading
import mysql.connector
import mysql.connector
import json
import mariadb

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        self.retour = {"status": 500, "valeurs": "erreur"}
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def login(self, pseudo, password):

        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = ("SELECT Id_Personne FROM Personne WHERE Pseudo = %s AND Password = %s ")
        cursor.execute(query, (pseudo, password))

        for (Id_Personne) in cursor:
            self.retour = {"status": 200, "valeurs": Id_Personne[0]}

    def get_id_cave(self, id_personne, label):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = ("SELECT Id_Cave FROM Cave WHERE label = %s AND Id_Personne = %s;")
        id = -1

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
            user="mywine",
            password="mywine",
            database='MyWine'
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
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}

    def get_Pseudos(self):

        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = ("SELECT Pseudo FROM Personne")

        try:
            tab = []
            cursor.execute(query)
            for (Pseudo) in cursor :
                tab.append(Pseudo[0])
            self.retour = {"status": 200, "valeurs": tab}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}

    def supprimer_cave(self, user_id, label):

        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = ("DELETE FROM Cave WHERE Id_Personne = %s AND label = %s")

        try:
            tab = []
            cursor.execute(query, (user_id, label))
            self.retour = {"status": 200, "valeurs": True}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}


    def create_cave(self, label, Id_Personne):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
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
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

    def get_Pseudo(self, id_user):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = ("SELECT Pseudo FROM Personne WHERE id_Personne = %s;")

        try:
            cursor.execute(query, (id_user,))
            for (Pseudo) in cursor:
                self.retour = {"status": 200, "valeurs": Pseudo[0]}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

    def get_caves(self, id_utilisateur):

        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
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
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "SELECT Vin.Id_Vin, Nom, Type, Notation, Echangeable, Annee, Quantite, label FROM Vin JOIN Cave on Cave.id_Cave = Vin.id_Cave WHERE id_Personne = %s;")

        try:
            tab = []
            cursor.execute(query, (id_utilisateur,))
            for (Id_Vin, Nom, Type, Notation, Echangeable, Annee, Quantite, label) in cursor:
                tab.append(
                    {"Nom": Nom, "Type": Type, "Notation": Notation, "Echangeable": Echangeable, "Année": Annee,
                     "Quantité": Quantite, "Image": "Image", "label": label, "Id": Id_Vin})
            self.retour = {"status": 200, "valeurs": tab}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

    def get_vin(self, id_utilisateur, id_Vin):

        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "SELECT Vin.Id_Vin, Nom, Type, Notation, Echangeable, Annee, Quantite, label FROM Vin JOIN Cave ON cave.Id_Cave=vin.Id_Cave WHERE Cave.Id_Personne = %s AND Vin.Id_Vin = %s;")

        try:
            tab = []
            cursor.execute(query, (id_utilisateur, id_Vin))
            for (Id_Vin, Nom, Type, Notation, Echangeable, Annee, Quantite, label) in cursor:
                tab.append(
                    {"Nom": Nom, "Type": Type, "Notation": Notation, "Echangeable": Echangeable, "Année": Annee,
                     "Quantité": Quantite, "Image": "Image", "label": label, "Id": Id_Vin})
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
            user="mywine",
            password="mywine",
            database='MyWine'
        )
        tab = []

        cursor = mydb.cursor()
        if ("Id_Cave" in valeurs):
            index = valeurs.index("Id_Cave")
            valeurs[index] = "Vin.Id_Cave"
        if (len(valeurs) == 2):
            query = (
                        "SELECT Nom, Type, Notation, Echangeable, Annee, Quantite, Image, label, Id_Vin FROM Vin JOIN Cave on Cave.id_Cave = Vin.id_Cave WHERE Id_Personne = %s AND " +
                        valeurs[0] + " = %s;")
            try:

                cursor.execute(query, (id_utilisateur, valeurs[1]))
                for (Nom, Type, Notation, Echangeable, Annee, Quantite, Image, label,Id_Vin) in cursor:
                    tab.append(
                        {"Nom": Nom, "Type": Type, "Notation": Notation, "Echangeable": Echangeable, "Année": Annee,
                         "Quantité": Quantite, "Image": Image, "label": label, "Id": Id_Vin})
                self.retour = {"status": 200, "valeurs": tab}
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)
                self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        elif (len(valeurs) == 4):
            query = (
                        "SELECT Nom, Type, Notation, Echangeable, Annee, Quantite, Image, label, Id_vin FROM Vin JOIN Cave on Cave.id_Cave = Vin.id_Cave WHERE Id_Personne = %s AND " +
                        valeurs[0] + " = %s AND " + valeurs[2] + " = %s;")
            try:
                cursor.execute(query, (id_utilisateur, valeurs[1], valeurs[3]))
                for (Nom, Type, Notation, Echangeable, Annee, Quantite, Image, label, Id_Vin) in cursor:
                    tab.append(
                        {"Nom": Nom, "Type": Type, "Notation": Notation, "Echangeable": Echangeable, "Année": Annee,
                         "Quantité": Quantite, "Image": Image, "label": label, "Id": Id_Vin})
                    self.retour = {"status": 200, "valeurs": tab}
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)
                self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}

        elif (len(valeurs) == 6):
            query = (
                        "SELECT Nom, Type, Notation, Echangeable, Annee, Quantite, Image, label, Id_Vin FROM Vin JOIN Cave on Cave.id_Cave = Vin.id_Cave WHERE id_Personne = %s AND " +
                        valeurs[0] + " = %s AND " + valeurs[2] + " = %s AND " + valeurs[4] + " = %s;")
            try:
                cursor.execute(query, (id_utilisateur, valeurs[1], valeurs[3], valeurs[5]))
                for (Nom, Type, Notation, Echangeable, Annee, Quantite, Image, label, Id_Vin) in cursor:
                    tab.append(
                        {"Nom": Nom, "Type": Type, "Notation": Notation, "Echangeable": Echangeable, "Année": Annee,
                         "Quantité": Quantite, "Image": Image, "label": label, "Id": Id_Vin})
                    self.retour = {"status": 200, "valeurs": tab}
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)
                self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        else:
            query = (
                    "SELECT Nom, Type, Notation, Echangeable, Annee, Quantite, Image, label, Id_Vin FROM Vin JOIN Cave on Cave.id_Cave = Vin.id_Cave WHERE id_Personne = %s AND " +
                    valeurs[0] + " = %s AND " + valeurs[2] + " = %s AND " + valeurs[4] + " = %s AND " + valeurs[
                        6] + " = %s;")
            try:
                cursor.execute(query, (id_utilisateur, valeurs[1], valeurs[3], valeurs[5], valeurs[7]))
                for (Nom, Type, Notation, Echangeable, Annee, Quantite, Image, label, Id_Vin) in cursor:
                    tab.append(
                        {"Nom": Nom, "Type": Type, "Notation": Notation, "Echangeable": Echangeable, "Année": Annee,
                         "Quantité": Quantite, "Image": Image, "label": label, "Id": Id_Vin})
                    self.retour = {"status": 200, "valeurs": tab}
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)
                self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}

    def get_id_user(self, pseudo):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "SELECT Utilisateur.Id_Personne FROM Utilisateur JOIN Personne on Utilisateur.Id_Personne = Personne.Id_Personne WHERE Pseudo = %s;")
        try:
            cursor.execute(query, (pseudo,))
            for (Id_Personne) in cursor:
                self.retour = {"status": 200, "valeurs": Id_Personne}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}

    def supprimer_vin(self, id_user, id_vin):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "DELETE Vin FROM Vin JOIN Cave ON Cave.Id_Cave=vin.Id_Cave WHERE Id_Personne = %s AND Id_Vin = %s;")

        try:
            cursor.execute(query, (id_user, id_vin))
            self.retour = {"status": 200, "valeurs": True}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

    def get_users(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "SELECT Utilisateur.Id_Personne, Personne.Nom, Personne.Prenom, Personne.Numero_telephone, Personne.Pseudo FROM Utilisateur JOIN Personne on Personne.Id_Personne = Utilisateur.Id_Personne;")

        try:
            tab = []
            cursor.execute(query)
            for (Id_Personne, Nom, Prenom, Numero_telephone, Pseudo) in cursor:
                tab.append({"Id": Id_Personne, "Nom": Nom, "Prénom":Prenom, "Num_tel": Numero_telephone, "Pseudo": Pseudo})
            self.retour = {"status": 200, "valeurs": tab}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

    def delete_user(self, id_user):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "DELETE FROM Personne WHERE Id_Personne = %s; ")

        try:
            cursor.execute(query, (id_user,))
            self.retour = {"status": 200, "valeurs": True}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()


    def incrementer_quantite(self, id_user, id_vin):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "UPDATE Vin JOIN Cave ON Cave.Id_Cave=Vin.Id_Cave SET Quantite = (SELECT Quantite FROM (SELECT * FROM Vin) AS v JOIN cave c ON c.Id_Cave=v.Id_Cave WHERE c.Id_Personne = %s AND v.Id_Vin = %s)+1 WHERE Id_Personne = %s AND Id_Vin = %s;")

        try:
            cursor.execute(query, (id_user, id_vin, id_user, id_vin))
            self.retour = {"status": 200, "valeurs": True}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

    def decrementer_quantite(self, id_user, id_vin):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "UPDATE Vin JOIN Cave ON Cave.Id_Cave=Vin.Id_Cave SET Quantite = (SELECT Quantite FROM (SELECT * FROM Vin) AS v JOIN Cave c ON c.Id_Cave=v.Id_Cave WHERE c.Id_Personne = %s AND v.Id_Vin = %s)-1 WHERE Id_Personne = %s AND Id_Vin = %s;")

        try:
            cursor.execute(query, (id_user, id_vin, id_user, id_vin))
            self.retour = {"status": 200, "valeurs": True}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

    def get_random_id(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "SELECT Utilisateur.Id_Personne, Pseudo FROM Utilisateur  JOIN Personne on Personne.Id_Personne = utilisateur.Id_Personne ORDER BY RAND() LIMIT 1")

        try:
            cursor.execute(query)
            for (Id_Personne, Pseudo) in cursor:
                self.retour = {"status": 200, "valeurs": [Id_Personne, Pseudo]}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

    def ajouter_vin(self, nom, annee, type, cave, commentaire, image, echangeable, quantite, user_id):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        echange = False
        if (echangeable == 'True'):
            echange = True
        cursor = mydb.cursor()
        query = (
            "INSERT INTO Vin (Id_Vin,Nom,Type,Notation,Echangeable,Annee,Quantite,Id_Cave, Image) VALUES(null, %s, %s, %s, %s, %s, %s, %s, %s)")

        id = self.get_id_cave(user_id, cave)
        try:
            cursor.execute(query, (nom, type, commentaire, echange, int(annee), quantite, id, image))
            self.retour = {"status": 200, "valeurs": True}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}

    def demande_echange(self, id_user, id_user_visite, id_vin_demande, id_vin_propose):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "INSERT INTO Echange (Id_Echange, accept, Id_Vin_Recepteur, Id_Vin_Emmetteur, Id_Emmetteur, Id_Recepteur, Date_demande, reponse) VALUES(null, False, %s, %s, %s, %s, NOW(), FALSE)")

        try:
            cursor.execute(query, (id_vin_demande, id_vin_propose, id_user, id_user_visite))
            self.retour = {"status": 200, "valeurs": True}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}

    def accept_echange(self, id_echange):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "Update Echange SET reponse = True, accept = True, Date_reponse = NOW() WHERE Id_Echange = %s;")

        try:
            cursor.execute(query, (id_echange,))
            self.retour = {"status": 200, "valeurs": True}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}

    def refuse_echange(self, id_echange):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "Update Echange SET reponse = True, accept = False, Date_reponse = NOW() WHERE Id_Echange = %s;")

        try:
            cursor.execute(query, (id_echange,))
            self.retour = {"status": 200, "valeurs": True}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}

    def change_vin(self, nom, annee, type, cave, commentaire, image, echangeable, quantite, id_vin, id_user):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        echange = False
        if (echangeable == 'True'):
            echange = True

        cursor = mydb.cursor()
        query = (
            "Update Vin SET Nom = %s, annee = %s, type= %s, Id_Cave= %s, Notation= %s, image= %s, echangeable= %s, quantite= %s WHERE Id_Vin = %s;")
        id = self.get_id_cave(id_user, cave)
        try:
            cursor.execute(query, (nom, annee, type, id, commentaire, image, echange, quantite, id_vin))
            self.retour = {"status": 200, "valeurs": True}
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}


    def get_demandeRecu(self, id_user):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )
        cursor = mydb.cursor()
        query = (
            "SELECT Id_Echange, accept, Personne.Pseudo, vv.Nom, v.Nom, DATE_FORMAT(Date_demande, '%d/%m/%Y'), reponse FROM Echange  JOIN Personne on Personne.Id_Personne = echange.Id_Emmetteur "
            "JOIN Vin vv on vv.Id_Vin = echange.Id_Vin_Emmetteur  JOIN Vin v on v.Id_Vin = echange.Id_Vin_Recepteur WHERE id_Recepteur = %s")

        try:
            cursor.execute(query, (id_user,))
            tab = []
            for (Id_Echange, accept, Pseudo, Nom, Nomv, Date_demande, reponse) in cursor:
                tab.append(
                    {"id": Id_Echange, "Echange": accept, "Pseudo": Pseudo, "Nom_vin_moi": Nomv,
                     "Nom_vin_demandeur": Nom, "Date_demande": Date_demande, "Reponse": reponse})
            self.retour = {"status": 200, "valeurs": tab}
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            self.retour = {"status": 500, "valeurs": "erreur : " + err.msg}
        mydb.close()
        cursor.close()

    def get_demandeEnvoye(self, id_user):
        mydb = mysql.connector.connect(
            host="localhost",
            user="mywine",
            password="mywine",
            database='MyWine'
        )

        cursor = mydb.cursor()
        query = (
            "SELECT accept, Personne.Pseudo, vv.Nom, v.Nom, DATE_FORMAT(Date_demande, '%d/%m/%Y'), reponse FROM Echange  JOIN Personne on Personne.Id_Personne = echange.id_Recepteur "
            "JOIN Vin vv on vv.Id_Vin = echange.Id_Vin_Emmetteur  JOIN Vin v on v.Id_Vin = echange.Id_Vin_Recepteur WHERE Id_Emmetteur = %s")

        try:
            cursor.execute(query, (id_user,))
            tab = []
            for (accept, Pseudo, Nom, Nomv, Date_demande, reponse) in cursor:
                tab.append(
                    {"Echange": accept, "Pseudo": Pseudo, "Nom_vin_moi": Nomv, "Nom_vin_demandeur": Nom,
                     "Date_demande": Date_demande, "Reponse": reponse})
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
        r = ""
        while 1:
            message = self.clientsocket.recv(1248)
            message = message.decode("utf-8")

            # test = json.loads(r)
            r = r + message
            if "}" in message:
                break

        test = json.loads(r)

        print(test['fonction'])

        if (test['fonction'] == "login"):
            self.login(test['paramètres'][0], test['paramètres'][1])
        elif (test['fonction'] == "create_account"):
            self.create_account(test['paramètres'][0], test['paramètres'][1], test['paramètres'][2],
                                test['paramètres'][3], test['paramètres'][4])
        elif (test['fonction'] == "get_vins"):
            self.get_vins(test['paramètres'][0])
        elif (test['fonction'] == "create_cave"):
            self.create_cave(test['paramètres'][0], test['paramètres'][1])
        elif (test['fonction'] == "get_caves"):
            self.get_caves(test['paramètres'][0])
        elif (test['fonction'] == "ajouter_vin"):
            self.ajouter_vin(test['paramètres'][0], test['paramètres'][1], test['paramètres'][2], test['paramètres'][3],
                             test['paramètres'][4], test['paramètres'][5], test['paramètres'][6], test['paramètres'][7],
                             test['paramètres'][8])
        elif (test['fonction'] == "get_random_id"):
            self.get_random_id()
        elif (test['fonction'] == "filtre"):
            self.filtre(test['paramètres'][0], test['paramètres'][1])
        elif (test['fonction'] == "get_id_cave"):
            print("ici")
            print(test['paramètres'][1])
            self.get_id_cave(test['paramètres'][0], test['paramètres'][1])
        elif (test['fonction'] == "get_id_user"):
            self.get_id_user(test['paramètres'][0])
        elif (test['fonction'] == 'get_Pseudo'):
            self.get_Pseudo(test['paramètres'][0])
        elif (test['fonction'] == 'demande_echange'):
            self.demande_echange(test['paramètres'][0], test['paramètres'][1], test['paramètres'][2],
                                 test['paramètres'][3])
        elif (test['fonction'] == 'get_demandeRecu'):
            self.get_demandeRecu(test['paramètres'][0])
        elif (test['fonction'] == 'get_demandeEnvoye'):
            self.get_demandeEnvoye(test['paramètres'][0])
        elif (test['fonction'] == 'supprimer_vin'):
            self.supprimer_vin(test['paramètres'][0], test['paramètres'][1])
        elif (test['fonction'] == 'incrementer_quantite'):
            self.incrementer_quantite(test['paramètres'][0], test['paramètres'][1])
        elif (test['fonction'] == 'decrementer_quantite'):
            self.decrementer_quantite(test['paramètres'][0], test['paramètres'][1])
        elif (test['fonction'] == 'get_vin'):
            self.get_vin(test['paramètres'][0], test['paramètres'][1])
        elif (test['fonction'] == "accept_echange"):
            self.accept_echange(test['paramètres'][0])
        elif (test['fonction'] == "refuse_echange"):
            self.refuse_echange(test['paramètres'][0])
        elif (test['fonction'] == "change_vin"):
            self.change_vin(test['paramètres'][0], test['paramètres'][1], test['paramètres'][2], test['paramètres'][3],
                            test['paramètres'][4], test['paramètres'][5], test['paramètres'][6], test['paramètres'][7],
                            test['paramètres'][8], test['paramètres'][9])
        elif(test['fonction'] == "get_users"):
            self.get_users()
        elif (test['fonction'] == "delete_user"):
            self.delete_user( test['paramètres'][0])
        elif (test['fonction'] == "get_Pseudos"):
            self.get_Pseudos()
        elif (test['fonction'] == "get_caves"):
            self.get_caves(test['paramètres'][0])
        elif(test["fonction"] == "supprimer_cave"):
            self.supprimer_cave(test['paramètres'][0], test['paramètres'][1])

        print(self.retour)
        self.retour = json.dumps(self.retour)
        self.clientsocket.send(bytes(self.retour, encoding="utf-8"))

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