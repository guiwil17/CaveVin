import tkinter.filedialog
import tkinter as tk
from PIL import Image, ImageTk
import PageAccueil
import socket
import json

class PageRecherche(tk.Frame):
    def __init__(self, parent, controller, id_user):


        tk.Frame.__init__(self, parent)


        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/cave.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)
        titre = ("Time New Roman", 35, "bold")
        fonts = ("Time New Roman", 18, "bold")
        fonts2 = ("Time New Roman", 16)

        can.create_text(610, 80, text="Rechercher une Cave", font=titre, fill="white")

        self.imgHome = tk.PhotoImage(file="img/home.png")
        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame("PageAccueil",[id_user] ))
        buttonHome.place(x=5,y=5)

        can.create_text(330, 265, text="Pseudo du propriétaire", font=fonts, fill="white")

        self.entryPseudo = tk.Entry(can,  font=fonts, bg="white", fg="black", justify="center")
        self.entryPseudo.place(x=480, y=250)
        def recherche():
            entryPseudo = self.entryPseudo.get()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "get_id_user", "paramètres": [entryPseudo]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)
            s.close()
            if(data["status"] == 200 and data["valeurs"]):
                controller.show_frame("VisiterCaves", [id_user, int(data["valeurs"][0])])
            else:
                can.create_text(600, 300, text="Pseudo inconnu", font=fonts, fill="white")

        def random():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "get_random_id"}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)
            s.close()
            if(data["status"] == 200 and data["valeurs"][0]!=id_user):
                controller.show_frame("VisiterCaves", [id_user, int(data["valeurs"][0])])
            else:
                random()
        buttonRecherche = tk.Button(can, text="Rechercher", padx=23, font=fonts2, pady=0, bg="#AC1E44",
                                 fg="white", command=recherche)
        buttonRecherche.place(x=515, y=400)

        buttonAleatoire = tk.Button(can, text="Cave Aléatoire", padx=10, font=fonts2, pady=0,
                                 bg="#AC1E44", fg="white", command=random)
        buttonAleatoire.place(x=515, y=470)

