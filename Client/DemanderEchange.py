import tkinter.filedialog
import tkinter as tk
from tkinter.ttk import *
import socket
import json
import PageAccueil
import Pages
from PIL import Image, ImageTk
import PageAjouterVin
import PageAjouterCave
import base64
import io


class DemanderEchange(tk.Frame):
    def __init__(self, parent, controller, id_user, id_user_visite, id_vin_demande):

        tk.Frame.__init__(self, parent)

        def recupVins():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "get_vins", "paramètres": [id_user]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)

            return data['valeurs']

        def selectItem(a):
            curItem = tableau.focus()
            print("appel")
            if(tableau.item(curItem)["values"][7]=="Demande d'échange (double clic)"):
                #requête envoi demande d'échange
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("93.7.175.167", 1111))

                m = {"fonction": "demande_echange", "paramètres": [id_user, id_user_visite, id_vin_demande, int(tableau.item(curItem)["values"][8])]}
                data = json.dumps(m)

                s.sendall(bytes(data, encoding="utf-8"))

                r = s.recv(9999999)
                r = r.decode("utf-8")
                data = json.loads(r)

                print(data['valeurs'])

        data = recupVins()

        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/vigne1.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)
        style = Style(can)
        style.configure('Treeview', rowheight=50)

        self.imgHome = tk.PhotoImage(file="img/home.png")
        self.imgcave = tk.PhotoImage(file="img/cave.png")
        self.imgEmailReceive = tk.PhotoImage(file="img/email_recu.png")
        self.imgEmailSend = tk.PhotoImage(file="img/email_envoye.png")

        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame("PageAccueil",[id_user]))
        buttonHome.place(x=5,y=5)

        buttonMailReceive = tk.Button(can, image=self.imgEmailReceive, command=lambda: controller.show_frame("PageAccueil",[id_user]))
        buttonMailReceive.place(x=1150, y=5)

        buttonMailSend = tk.Button(can, image=self.imgEmailSend,command=lambda: controller.show_frame("PageAccueil",[id_user]))
        buttonMailSend.place(x=1100, y=5)

        titre = ("Time New Roman", 30, "bold")

        button_filtre = tk.Button(can, text="Filtrer")
        button_filtre.place(x=750, y=150)

        can.create_text(560, 40, text="Choisissez votre vin proposé", font=titre, fill="white")

        #Filtre
        can.create_text(70, 160, text="Filtre", font=titre, fill="white")
        filtreNom = tk.Entry(can, font=("Montserrat", 12, "bold"), width=13, bg="white", fg="black", justify="center")
        filtreNom.place(x=140, y=150)

        filtreType = tk.Entry(can, font=("Montserrat", 12, "bold"), width=15, bg="white", fg="black", justify="center")
        filtreType.place(x=320, y=150)

        filtreAnnee = tk.Entry(can, font=("Montserrat", 12, "bold"), width=7, bg="white", fg="black", justify="center")
        filtreAnnee.place(x=520, y=150)

        filtreCave = tk.Entry(can, font=("Montserrat", 12, "bold"),  width=9, bg="white", fg="black", justify="center")
        filtreCave.place(x=620, y=150)

        button_filtre = tk.Button(can, text="Filtrer")
        button_filtre.place(x=750, y=150)

        #Tableau

        tableau = Treeview(can, columns=('','Nom', 'Type', 'Année', 'Cave', 'Commentaire', 'Quantité', 'Echangeable'))
        tableau.pack(padx=10, pady=180)

        vsb = Scrollbar(can, orient="vertical", command=tableau.yview)
        vsb.pack(side='right', fill='y')
        tableau.configure(yscrollcommand=vsb.set)

        vsb.place(x=1180, y=180, height=527)

        tableau.column('',  width=100, stretch=tk.NO, anchor='center')
        tableau.column('Nom', width=200, stretch=tk.NO, anchor='center')
        tableau.column('Type', width=200, stretch=tk.NO, anchor='center')
        tableau.column('Année', width=100, stretch=tk.NO, anchor='center')
        tableau.column('Commentaire', width=300, stretch=tk.NO, anchor='center')
        tableau.column('Cave', width=120, stretch=tk.NO, anchor='center')
        tableau.column('Quantité', width=100, stretch=tk.NO, anchor='center')
        tableau.column('Echangeable', width=50, stretch=tk.NO, anchor='center')

        tableau.heading('Nom', text='Nom')

        tableau.heading('Type', text='Type')

        tableau.heading('Année', text='Année')
        tableau.heading('Commentaire', text='Commentaire')
        tableau.heading('Cave', text='Cave')
        tableau.heading('Quantité', text='Quantité')
        tableau.heading('Echangeable', text='')

        tableau['show'] = 'headings'  # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert

       # for d in data:

            #if(d["Image"] != None):
            #    byte =  d["Image"].encode('utf-8')
             #   print(byte)
             #   #img = base64.decodebytes(byte)
             #   image = tk.PhotoImage(data=byte)
             #   tableau.insert('', 'end',  text="",image=image,  values=(
             #  d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"], d["Echangeable"]))
           # else:
           #     tableau.insert('', 'end', values=(
            #        d["Image"], d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"],
            #        d["Echangeable"]))
        for d in data:
            tableau.insert('', 'end', values=(
            d["Image"], d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"], ("Demande d'échange (double clic)" if d["Echangeable"]==1  else "Non échangeable"), d["Id"]))
        tableau.bind('<Double-1>', selectItem)




