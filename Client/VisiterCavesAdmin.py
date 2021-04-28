import tkinter as tk
from tkinter.ttk import *
import socket
import json
import PageAccueil
from PIL import Image, ImageTk
import io
from tkinter import messagebox

class VisiterCavesAdmin(tk.Frame):
    def __init__(self, parent, controller,id_user, id_user_visite):

        tk.Frame.__init__(self, parent)

        def recupVins():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "get_vins", "paramètres": [id_user_visite]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)
            s.close()

            return data['valeurs']

        data = recupVins()

        def get_Pseudo():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "get_Pseudo", "paramètres": [id_user_visite]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)
            s.close()

            return data['valeurs']


        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/vigne2.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)
        style = Style(can)
        style.configure('Treeview', rowheight=50)

        self.imgHome = tk.PhotoImage(file="img/retour.png")


        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame("PageAccueil",[id_user]))
        buttonHome.place(x=5,y=5)

        titre = ("Time New Roman", 30, "bold")

        txt_pseudo = can.create_text(640, 50,fill="white", font=titre,text="Caves de "+get_Pseudo())


        #Tableau

        self.tableau = Treeview(can, columns=('Nom', 'Type', 'Année', 'Cave', 'Commentaire', 'Quantité', 'Echangeable'))
        self.tableau.pack(padx=70, pady=180)

        vsb = Scrollbar(can, orient="vertical", command=self.tableau.yview)
        vsb.pack(side='right', fill='y')
        self.tableau.configure(yscrollcommand=vsb.set)

        vsb.place(x=1170, y=180, height=527)

        self.tableau.column('Nom', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Type', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Année', width=100, stretch=tk.NO, anchor='center')
        self.tableau.column('Commentaire', width=300, stretch=tk.NO, anchor='center')
        self.tableau.column('Cave', width=120, stretch=tk.NO, anchor='center')
        self.tableau.column('Quantité', width=80, stretch=tk.NO, anchor='center')
        self.tableau.column('Echangeable', width=100, stretch=tk.NO, anchor='center')

        self.tableau.heading('Nom', text='Nom')

        self.tableau.heading('Type', text='Type')

        self.tableau.heading('Année', text='Année')
        self.tableau.heading('Commentaire', text='Commentaire')
        self.tableau.heading('Cave', text='Cave')
        self.tableau.heading('Quantité', text='Quantité')
        self.tableau.heading('Echangeable', text='Echangeable')

        self.tableau['show'] = 'headings'  # sans ceci, il y avait une colonne vide à gauche qui a pour rôle d'afficher le paramètre "text" qui peut être spécifié lors du insert

        def selectItem(a):
            curItem = self.tableau.focus()
            id_vin = self.tableau.item(curItem)["values"][8]
            MsgBox = tk.messagebox.askokcancel("Suppression de vin", "Confirmez-vous la suppression du vin ?")
            if MsgBox:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("93.7.175.167", 1111))
                m = {"fonction": "supprimer_vin", "paramètres": [id_user, id_vin]}
                data = json.dumps(m)
                s.sendall(bytes(data, encoding="utf-8"))
                r = s.recv(9999999)
                r = r.decode("utf-8")
                data = json.loads(r)
                s.close()

                refresh()

        def refresh():
            data = recupVins()
            self.tableau.delete(*self.tableau.get_children())
            for d in data:
                self.tableau.insert('', 'end', values=(
                   d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"],
                    ("Oui" if d["Echangeable"] == 1 else "Non"), d["Id"]))
                self.tableau.bind('<Double-1>', selectItem)

        for d in data:
            self.tableau.insert('', 'end', values=(
           d["Nom"], d["Type"], d["Année"], d["Notation"], d["label"], d["Quantité"], ("Oui" if d["Echangeable"]==1  else "Non"), d["Id"]))
            self.tableau.bind('<Double-1>', selectItem)
