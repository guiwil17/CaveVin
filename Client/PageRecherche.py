import tkinter.filedialog
import tkinter as tk
from PIL import Image, ImageTk
import Pages
import PageAccueil


class PageRecherche(tk.Frame, Pages.Pages):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/cave.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)
        titre = ("Time New Roman", 35, "bold")
        fonts = ("Time New Roman", 18, "bold")
        fonts2 = ("Time New Roman", 16)

        can.create_text(600, 80, text="Rechercher une Cave", font=titre, fill="white")

        self.imgHome = tk.PhotoImage(file="img/home.png")
        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame(PageAccueil.PageAccueil))
        buttonHome.place(x=5,y=5)

        can.create_text(360, 260, text="Nom du propriétaire", font=fonts, fill="white")

        can.create_text(340, 310, text="Prénom du propriétaire", font=fonts, fill="white")

        entryNom = tk.Entry(can,  font=fonts, bg="white", fg="black", justify="center")
        entryNom.place(x=500, y=250)

        entryPrenom = tk.Entry(can, font=fonts, bg="white", fg="black", show="*", justify="center")
        entryPrenom.place(x=500, y=300)

        buttonRecherche = tk.Button(can, text="Rechercher", padx=23, font=fonts2, pady=0, bg="#AC1E44",
                                 fg="white")
        buttonRecherche.place(x=550, y=400)

        buttonAleatoire = tk.Button(can, text="Cave Aléatoire", padx=10, font=fonts2, pady=0,
                                 bg="#AC1E44", fg="white")
        buttonAleatoire.place(x=550, y=470)