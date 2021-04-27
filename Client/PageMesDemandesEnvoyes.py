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


class PageMesDemandesEnvoyes(tk.Frame):
    def __init__(self, parent, controller,id_user):

        tk.Frame.__init__(self, parent)
        self.data = []
        def recupEnvoie():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "get_demandeEnvoye", "paramètres": [id_user]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)
            if (data["status"] == 200 and data["valeurs"]):
                return data['valeurs']
            else:
                return []

        self.data = recupEnvoie()

        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/echange2.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)
        style = Style(can)
        style.configure('Treeview', rowheight=50)

        self.imgHome = tk.PhotoImage(file="img/home.png")
        self.imgcave = tk.PhotoImage(file="img/MesCaves.png")
        self.imgEmailReceive = tk.PhotoImage(file="img/email_recu.png")
        self.imgEmailSend = tk.PhotoImage(file="img/email_envoye.png")

        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame("PageAccueil",[id_user]))
        buttonHome.place(x=5,y=5)

        button_Ajouter_cave = tk.Button(can, image=self.imgcave, command=lambda: controller.show_frame("MesCaves", [id_user]))
        button_Ajouter_cave.place(x=60, y=5)

        titre = ("Time New Roman", 30, "bold")

        can.create_text(630, 90, text="Mes demandes envoyées", font=titre, fill="white")

        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]

        style = Style()
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))

    
        #Tableau
        self.tableau = Treeview(can, columns=('','Vin demandé', 'Mon vin', 'Receveur', 'Date de la demande'))
        self.tableau.pack(padx=147, pady=180)

        vsb = Scrollbar(can, orient="vertical", command=self.tableau.yview)
        vsb.pack(side='right', fill='y')
        self.tableau.configure(yscrollcommand=vsb.set)

        vsb.place(x=1081, y=180, height=527)

        self.tableau.column('',  width=150, stretch=tk.NO, anchor='center')
        self.tableau.column('Vin demandé', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Mon vin', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Receveur', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Date de la demande', width=200, stretch=tk.NO, anchor='center')

        self.tableau.heading('Vin demandé', text='Vin demandé')

        self.tableau.heading('Mon vin', text='Mon vin')

        self.tableau.heading('Receveur', text='Receveur')
        self.tableau.heading('Date de la demande', text='Date de la demande')

        self.tableau['show'] = 'headings'  # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert

        self.tableau.tag_configure('accept', background="green")
        self.tableau.tag_configure('refuse', background="red")

        if(len(self.data) != 0):
            for d in self.data:
                if(d["Reponse"] == 0):
                    self.tableau.insert('', 'end', values=(
                        "En attente de réponse", d["Nom_vin_moi"], d["Nom_vin_demandeur"], d["Pseudo"], d["Date_demande"]))
                else:

                    if(d["Echange"] == 0):
                        self.tableau.insert('', 'end', values=("accepté",d["Nom_vin_moi"], d["Nom_vin_demandeur"], d["Pseudo"], d["Date_demande"]), tags = ('accept',))
                    else:
                        self.tableau.insert('', 'end', values=("refusé",d["Nom_vin_moi"], d["Nom_vin_demandeur"], d["Pseudo"], d["Date_demande"]), tags = ('refuse',))


        #for d in self.data:
            #self.tableau.insert('', 'end', values=(
            #d["Image"], d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"], d["Echangeable"]))
        #for d in self.data:
            #self.tableau.insert('', 'end', values=(
            #{d["Image"], d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"], d["Echangeable"]))




