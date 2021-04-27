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
import PageConnexion
from PIL import Image, ImageTk

class PageAccueil(tk.Frame):
    def __init__(self, parent, controller, id_user):

        def Caves() :
            controller.show_frame("MesCaves", [id_user])

        tk.Frame.__init__(self, parent)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/accueil.jpg")
        self.logout = ImageTk.PhotoImage(file="img/logout.png")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)
        buttonLogout = tk.Button(can, image=self.logout, command=lambda: controller.show_frame("PageConnexion"))
        buttonLogout.place(x=5, y=5)
        can.create_text(630, 200, text="Accueil", font=("Montserrat", 38, "bold"), fill="white")

        button1 = tk.Button(can, text="Mes Caves", padx=59, font=("Montserrat", 18, "bold"), pady=10, bg="#AC1E44",
                         fg="white", command=Caves)
        button1.place(x=300, y=400)
        button2 = tk.Button(can, text="Visiter des Caves", padx=30, font=("Montserrat", 18, "bold"), pady=10, bg="#AC1E44",
                         fg="white", command=lambda: controller.show_frame("PageRecherche",[id_user] ))
        button2.place(x=700, y=400)