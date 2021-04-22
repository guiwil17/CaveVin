import tkinter.filedialog
import tkinter as tk
from PIL import Image, ImageTk

import PageAccueil


class PageRecherche(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/cave.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)


        can.create_text(600, 180, text="Rechercher une Cave", font=("Montserrat", 30, "bold"), fill="white")

        self.imgHome = tk.PhotoImage(file="img/home.png")
        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame(PageAccueil.PageAccueil))
        buttonHome.place(x=5,y=5)

        can.create_text(416, 300, text="Nom du propriétaire", font=("Montserrat", 18, "bold"), fill="white")

        can.create_text(400, 350, text="Prénom du propriétaire", font=("Montserrat", 18, "bold"), fill="white")

        entryNom = tk.Entry(can, font=("Montserrat", 18, "bold"), bg="white", fg="black", justify="center")
        entryNom.place(x=670, y=285)

        entryPrenom = tk.Entry(can, font=("Montserrat", 18, "bold"), bg="white", fg="black", show="*", justify="center")
        entryPrenom.place(x=670, y=335)

        buttonRecherche = tk.Button(can, text="Rechercher", padx=28, font=("Montserrat", 18, "bold"), pady=0, bg="#AC1E44",
                                 fg="white")
        buttonRecherche.place(x=500, y=430)

        buttonAleatoire = tk.Button(can, text="Cave Aléatoire", padx=10, font=("Montserrat", 18, "bold"), pady=0,
                                 bg="#AC1E44", fg="white")
        buttonAleatoire.place(x=500, y=500)