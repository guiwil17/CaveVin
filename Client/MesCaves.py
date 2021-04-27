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
from tkinter.messagebox import *

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

        data = recupVins()

        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
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

        button_Ajouter_vin = tk.Button(can,font=titre,text="Ajouter un vin", fg="white", pady=0, bg="#AC1E44", command=lambda: controller.show_frame("PageAjouterVin", [id_user]))
        button_Ajouter_vin.place(x=560, y=40)

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
        tableau.column('Quantité', width=80, stretch=tk.NO, anchor='center')
        tableau.column('Echangeable', width=70, stretch=tk.NO, anchor='center')

        tableau.heading('Nom', text='Nom')

        tableau.heading('Type', text='Type')

        tableau.heading('Année', text='Année')
        tableau.heading('Cave', text='Cave')
        tableau.heading('Commentaire', text='Commentaire')
        tableau.heading('Quantité', text='Quantité')
        tableau.heading('Echangeable', text='Echangeable')

        tableau['show'] = 'headings'  # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert

        class Mbox(object):

            root = None

            def __init__(self,id_user, id_vin, quantite):



                tki = tkinter
                self.top = tki.Toplevel(Mbox.root)
                self.quantite = quantite
                self.top.title("Action")
                frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
                frm.pack(fill='both', expand=True)

                label = tki.Label(frm, text="Quelle action voulez-vous réaliser ?")
                label.pack(padx=4, pady=4)

                b_modifier = tki.Button(frm, text='Modifier le Vin')
                b_modifier['command'] = lambda: self.modifier(id_user, id_vin)
                b_modifier.pack()

                self.label_quantite = tki.Label(frm, text = 'Quantité : '+str(self.quantite))
                self.label_quantite.pack()

                b_increm = tki.Button(frm, text='Augmenter quantité')
                b_increm['command'] = lambda: self.increm(id_user, id_vin, self.quantite)
                b_increm.pack()

                b_decrem = tki.Button(frm, text='Diminuer quantité')
                b_decrem['command'] = lambda: self.decrem(id_user, id_vin, self.quantite)
                b_decrem.pack()



                b_delete = tki.Button(frm, text='Supprimer')
                b_delete['command'] = lambda: self.supprimer(id_user, id_vin)
                b_delete.pack(padx=4, pady=4)

            def decrem(self, id_user, id_vin, quantite):
                if(self.quantite>0):
                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.connect(("93.7.175.167", 1111))
                    self.quantite=quantite-1
                    self.label_quantite["text"] = "Quantité : "+str(self.quantite)
                    m = {"fonction": "decrementer_quantite", "paramètres": [id_user, id_vin]}
                    data = json.dumps(m)

                    self.s.sendall(bytes(data, encoding="utf-8"))


                    refresh()

            def increm(self, id_user, id_vin, quantite):
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect(("93.7.175.167", 1111))
                self.quantite = quantite + 1
                self.label_quantite["text"] = "Quantité : " + str(self.quantite)
                m = {"fonction": "incrementer_quantite", "paramètres": [id_user, id_vin]}
                data = json.dumps(m)

                self.s.sendall(bytes(data, encoding="utf-8"))


                refresh()

            def modifier(self, id_user, id_vin):
                print("modifier")
                controller.show_frame("ModifierVin", [id_user, id_vin])
                self.top.destroy()

            def supprimer(self, id_user, id_vin):
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect(("93.7.175.167", 1111))
                m = {"fonction": "supprimer_vin", "paramètres": [id_user, id_vin]}
                data = json.dumps(m)
                self.s.sendall(bytes(data, encoding="utf-8"))
                r = self.s.recv(9999999)
                r = r.decode("utf-8")
                data = json.loads(r)
                refresh()
                self.top.destroy()

        def selectItem(a):
            curItem = tableau.focus()
            msg = Mbox(id_user, tableau.item(curItem)["values"][8], tableau.item(curItem)["values"][6])

        def refresh():
            data = recupVins()
            tableau.delete(*tableau.get_children())
            for d in data:
                tableau.insert('', 'end', values=(
                    d["Image"], d["Nom"], d["Type"], d["Année"], d["label"], d["Notation"], d["Quantité"],
                    ("Oui" if d["Echangeable"] == 1 else "Non"), d["Id"]))
            tableau.bind('<Double-1>', selectItem)

        for d in data:
            tableau.insert('', 'end', values=(
            d["Image"], d["Nom"], d["Type"], d["Année"], d["label"], d["Notation"], d["Quantité"], ("Oui" if d["Echangeable"]==1  else "Non"), d["Id"]))
        tableau.bind('<Double-1>', selectItem)


