import tkinter.filedialog
import tkinter as tk
from PIL import Image, ImageTk
import PageAccueil
import socket
import json
from tkinter.ttk import *

class PageAjouterCave(tk.Frame):
    def __init__(self, parent, controller,id_user):

        def AjoutCave():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "create_cave", "paramètres": [self.entryLabel.get(), id_user]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)
            s.close()
            mise_a_jour()

        def get_Caves():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "get_caves", "paramètres": [id_user]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)
            s.close()

            return data["valeurs"]



        tk.Frame.__init__(self, parent)
        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/cave2.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)

        self.data = get_Caves()

        style = Style(can)
        style.configure('Treeview', rowheight=30)

        self.imgHome = tk.PhotoImage(file="img/home.png")
        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame("PageAccueil", [id_user]))
        buttonHome.place(x=5, y=5)

        can.create_text(600, 150, text="Ajouter une Cave", font=("Montserrat", 30, "bold"), fill="white")

        can.create_text(390, 300, text="Nom", font=("Montserrat", 18, "bold"), fill="white")
        self.entryLabel = tk.Entry(can, font=("Montserrat", 18, "bold"), bg="white", fg="black", justify="center")
        self.entryLabel.place(x=430, y=285)

        buttonRecherche = tk.Button(can, text="Créer", padx=23, font=("Montserrat", 18, "bold"), pady=0, bg="#AC1E44",
                                 fg="white", command=AjoutCave)
        buttonRecherche.place(x=550, y=420)

        class Mbox(object):

            root = None

            def __init__(self, id_user, nom_cave):
                tki = tkinter
                self.top = tki.Toplevel(Mbox.root)
                self.top.title("Action")


                frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
                frm.pack(fill='both', expand=True)

                label = tki.Label(frm, text="Quelle action voulez-vous réaliser ?")
                label.pack(padx=4, pady=4)

                b_modifier = tki.Button(frm, text='Supprimer ' + nom_cave)
                b_modifier['command'] = lambda: self.supprimer_cave(id_user, nom_cave)
                b_modifier.pack()



            def supprimer_cave(self, id_user, nom_cave):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("93.7.175.167", 1111))
                m = {"fonction": "supprimer_cave", "paramètres": [id_user, nom_cave]}
                data = json.dumps(m)

                s.sendall(bytes(data, encoding="utf-8"))
                s.recv(9999999)
                s.close()

                mise_a_jour()
                self.top.destroy()


        def mise_a_jour():
            self.data = get_Caves()
            self.tableau.delete(*self.tableau.get_children())
            for d in self.data:
                self.tableau.insert('', 'end', values=(d, ""))
        def selectItem(a):
            curItem = self.tableau.focus()
            msg = Mbox(id_user, self.tableau.item(curItem)["values"][0])

        # Tableau
        self.tableau = Treeview(can, columns=('Cave', 'test'))
        self.tableau.pack(padx=260, pady=480)

        vsb = Scrollbar(can, orient="vertical", command=self.tableau.yview)
        vsb.pack(side='right', fill='y')
        self.tableau.configure(yscrollcommand=vsb.set)
        vsb.place(x=950, y=480, height=325)

        self.tableau.column('Cave', width=700, anchor='center')
        self.tableau.column('test', width=0, stretch=tk.NO, anchor='center')

        self.tableau.heading('Cave', text='Cave existante')
        self.tableau.heading('test', text='')

        self.tableau['show'] = 'headings'


        for d in self.data:
            self.tableau.insert('', 'end', values=(d, ""))

        self.tableau.bind('<Double-1>', selectItem)