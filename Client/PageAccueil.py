import tkinter.filedialog
import tkinter as tk
import socket
import json
import PageAjouterCave
import PageAjouterVin
import PageRecherche
import PageConnexion
import PageInscription
import MesCaves
import Pages
from PIL import Image, ImageTk

class PageAccueil(tk.Frame, Pages.Pages):
    def __init__(self, parent, controller):

        def Caves() :           
           
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "get_vins", "paramètres": [2]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)

            if (data["status"] == 200 and data["valeurs"]):
                Pages.Pages.MesCaves = data["valeurs"]

            controller.show_frame(MesCaves.MesCaves, "MesCaves")

        tk.Frame.__init__(self, parent)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/accueil.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)

        can.create_text(630, 200, text="Accueil", font=("Montserrat", 38, "bold"), fill="white")

        button1 = tk.Button(can, text="Mes Caves", padx=59, font=("Montserrat", 18, "bold"), pady=10, bg="#AC1E44",
                         fg="white", command=Caves)
        button1.place(x=300, y=400)
        button2 = tk.Button(can, text="Visiter des Caves", padx=30, font=("Montserrat", 18, "bold"), pady=10, bg="#AC1E44",
                         fg="white", command=lambda: controller.show_frame(PageRecherche.PageRecherche))
        button2.place(x=700, y=400)