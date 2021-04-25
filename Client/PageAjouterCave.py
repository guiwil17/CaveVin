import tkinter.filedialog
import tkinter as tk
from PIL import Image, ImageTk
import Pages
import PageAccueil
import socket
import json

class PageAjouterCave(tk.Frame, Pages.Pages):
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
            print(data)


        tk.Frame.__init__(self, parent)
        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/cave2.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)

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