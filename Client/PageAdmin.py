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
import io


class PageAdmin(tk.Frame):
    def __init__(self, parent, controller, id_user):

        tk.Frame.__init__(self, parent)

        def recupUsers():
            print("recupusers")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "get_users", "paramètres": [id_user]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)
            print(data)
            return data['valeurs']

        self.data = recupUsers()

        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/admin.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)
        style = Style(can)
        style.configure('Treeview', rowheight=50)

        self.imgHome = tk.PhotoImage(file="img/home.png")

        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame("PageConnexion"))
        buttonHome.place(x=5, y=5)

        titre = ("Time New Roman", 15, "bold")

        can.create_text(600, 150, text="Supprimer des utilisateurs", font=("Montserrat", 30, "bold"), fill="white")

        # Tableau

        self.tableau = Treeview(can, columns=('Nom', 'Prenom', 'Numero', 'Pseudo'))
        self.tableau.pack(padx=220, pady=180)

        vsb = Scrollbar(can, orient="vertical", command=self.tableau.yview)
        vsb.pack(side='right', fill='y')
        self.tableau.configure(yscrollcommand=vsb.set)

        vsb.place(x=1010, y=181, height=525)

        self.tableau.column('Nom', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Prenom', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Numero', width=100, stretch=tk.NO, anchor='center')
        self.tableau.column('Pseudo', width=300, stretch=tk.NO, anchor='center')

        self.tableau.heading('Nom', text='Nom')
        self.tableau.heading('Prenom', text='Prénom')
        self.tableau.heading('Numero', text='Numéro téléphone')
        self.tableau.heading('Pseudo', text='Pseudo')

        self.tableau['show']="headings"

        class Mbox(object):

            root = None

            def __init__(self, id_user):
                tki = tkinter
                self.top = tki.Toplevel(Mbox.root)
                self.top.title("Action")
                frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
                frm.pack(fill='both', expand=True)

                label = tki.Label(frm, text="Quelle action voulez-vous réaliser ?")
                label.pack(padx=4, pady=4)

                b_modifier = tki.Button(frm, text='Voir les Vins')
                b_modifier['command'] = lambda: self.modifier(id_user)
                b_modifier.pack()

                b_delete = tki.Button(frm, text='Supprimer')
                b_delete['command'] = lambda: self.supprimer(id_user)
                b_delete.pack(padx=4, pady=4)

            def modifier(self, id_user):
                controller.show_frame("VisiterCavesAdmin", [1, id_user])
                self.top.destroy()

            def supprimer(self, id_user):
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect(("93.7.175.167", 1111))
                m = {"fonction": "delete_user", "paramètres": [id_user]}
                data = json.dumps(m)
                self.s.sendall(bytes(data, encoding="utf-8"))
                r = self.s.recv(9999999)
                r = r.decode("utf-8")
                data = json.loads(r)
                refresh()
                self.top.destroy()

        def selectItem(a):
            curItem = self.tableau.focus()
            msg = Mbox(self.tableau.item(curItem)["values"][4])

        def refresh():
            data = recupUsers()
            self.tableau.delete(*self.tableau.get_children())
            for d in data:
                self.tableau.insert('', 'end', values=(d["Nom"], d["Prénom"], d["Num_tel"], d["Pseudo"], d["Id"]))
                self.tableau.bind('<Double-1>', selectItem)

        for d in self.data:
            self.tableau.insert('', 'end', values=(d["Nom"], d["Prénom"], d["Num_tel"], d["Pseudo"], d["Id"]))
            self.tableau.bind('<Double-1>', selectItem)



