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
from io import StringIO


class MesCaves(tk.Frame):
    def __init__(self, parent, controller,id_user):

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

        self.data = recupVins()

        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        print("la")
        self.img = ImageTk.PhotoImage(file="img/vigne2.jpg")
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

        button_Ajouter_cave = tk.Button(can, image=self.imgcave, command=lambda: controller.show_frame("PageAjouterCave", [id_user]))
        button_Ajouter_cave.place(x=60, y=5)

        buttonMailReceive = tk.Button(can, image=self.imgEmailReceive, command=lambda: controller.show_frame("PageAccueil",[id_user]))
        buttonMailReceive.place(x=1150, y=5)

        buttonMailSend = tk.Button(can, image=self.imgEmailSend,command=lambda: controller.show_frame("PageAccueil",[id_user]))
        buttonMailSend.place(x=1100, y=5)

        titre = ("Time New Roman", 15, "bold")

        button_filtre = tk.Button(can, text="Filtrer")
        button_filtre.place(x=750, y=150)

        button_Ajouter_vin = tk.Button(can,font=titre,text="Ajouter un vin", pady=0, bg="#AC1E44", command=lambda: controller.show_frame("PageAjouterVin", [id_user]))
        button_Ajouter_vin.place(x=560, y=40)

        def filtrage():

            tab = []
            print(self.filtreNom.get())
            if(self.filtreNom.get() != ""):
                tab.append("Nom")
                tab.append(self.filtreNom.get())
            if (self.filtreType.get() != ""):
                tab.append("Type")
                tab.append(self.filtreType.get())
            if (self.filtreAnnee.get() != ""):
                tab.append("Année")
                tab.append(self.filtreAnnee.get())
            if (self.filtreCave.get() != ""):
                tab.append("Id_Cave")
                m = {"fonction": "get_id_cave", "paramètres": [id_user, self.filtreCave.get()]}
                data = json.dumps(m)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("93.7.175.167", 1111))
                s.sendall(bytes(data, encoding="utf-8"))

                r = s.recv(9999999)
                r = r.decode("utf-8")
                data = json.loads(r)

                tab.append(data["valeurs"])

            if(len(tab) != 0):
                m = {"fonction": "filtre", "paramètres": [id_user, tab]}
                data = json.dumps(m)

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("93.7.175.167", 1111))
                s.sendall(bytes(data, encoding="utf-8"))

                r = s.recv(9999999)
                r = r.decode("utf-8")
                data = json.loads(r)
                print(data)
                self.data = data['valeurs']

            else:
                self.data = recupVins()
            self.tableau.delete(*self.tableau.get_children())
            for d in self.data:
                self.tableau.insert('', 'end', values=(
                    d["Image"], d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"],
                    d["Echangeable"]))
        #Filtre

        can.create_text(70, 160, text="Filtre", font=titre, fill="white")
        self.filtreNom = tk.Entry(can, font=("Montserrat", 12, "bold"), width=13, bg="white", fg="black", justify="center")
        self.filtreNom.place(x=140, y=150)

        self.filtreType = tk.Entry(can, font=("Montserrat", 12, "bold"), width=15, bg="white", fg="black", justify="center")
        self.filtreType.place(x=320, y=150)

        self.filtreAnnee = tk.Entry(can, font=("Montserrat", 12, "bold"), width=7, bg="white", fg="black", justify="center")
        self.filtreAnnee.place(x=520, y=150)

        self.filtreCave = tk.Entry(can, font=("Montserrat", 12, "bold"),  width=9, bg="white", fg="black", justify="center")
        self.filtreCave.place(x=620, y=150)

        button_filtre = tk.Button(can, text="Filtrer", command=filtrage)
        button_filtre.place(x=750, y=150)



        #Tableau

        self.tableau = Treeview(can, columns=('','Nom', 'Type', 'Année', 'Cave', 'Commentaire', 'Quantité', 'Echangeable'))
        self.tableau.pack(padx=10, pady=180)

        vsb = Scrollbar(can, orient="vertical", command=self.tableau.yview)
        vsb.pack(side='right', fill='y')
        self.tableau.configure(yscrollcommand=vsb.set)

        vsb.place(x=1180, y=180, height=527)

        self.tableau.column('',  width=100, stretch=tk.NO, anchor='center')
        self.tableau.column('Nom', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Type', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Année', width=100, stretch=tk.NO, anchor='center')
        self.tableau.column('Commentaire', width=300, stretch=tk.NO, anchor='center')
        self.tableau.column('Cave', width=120, stretch=tk.NO, anchor='center')
        self.tableau.column('Quantité', width=100, stretch=tk.NO, anchor='center')
        self.tableau.column('Echangeable', width=50, stretch=tk.NO, anchor='center')

        self.tableau.heading('Nom', text='Nom')

        self.tableau.heading('Type', text='Type')

        self.tableau.heading('Année', text='Année')
        self.tableau.heading('Commentaire', text='Commentaire')
        self.tableau.heading('Cave', text='Cave')
        self.tableau.heading('Quantité', text='Quantité')
        self.tableau.heading('Echangeable', text='')

        self.tableau['show'] = 'headings'  # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert

        for d in self.data:

            if(d["Image"] != None):
                byte =  d["Image"].encode('utf-8')
                #print(byte)
                t = base64.b64decode(byte)

                # img = base64.decodebytes(byte)
                #image_string = StringIO(d["Image"])
                #img = Image.open(t)


                #print(img)
                #b = image.save(b, format="JPEG")

                image = ImageTk.PhotoImage(data=t)
                #buttonHome = tk.Button(can, image=image,command=lambda: controller.show_frame("PageAccueil", [id_user]))
                #buttonHome.place(x=200, y=5)
                #tableau.insert('', 'end',  text="", image=image,  values=(
               #d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"], d["Echangeable"]))
            else:
                self.tableau.insert('', 'end', values=(
                    d["Image"], d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"],d["Echangeable"]))
        for d in self.data:
            self.tableau.insert('', 'end', values=(
            d["Image"], d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"], d["Echangeable"]))
        for d in self.data:
            self.tableau.insert('', 'end', values=(
            d["Image"], d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"], d["Echangeable"]))




