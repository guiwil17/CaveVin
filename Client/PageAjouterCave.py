import tkinter.filedialog
import tkinter as tk
from PIL import Image, ImageTk
import Pages
import PageAccueil

class PageAjouterCave(tk.Frame, Pages.Pages):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/cave2.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)

        self.imgHome = tk.PhotoImage(file="img/home.png")
        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame(PageAccueil.PageAccueil))
        buttonHome.place(x=5, y=5)

        can.create_text(600, 150, text="Ajouter une Cave", font=("Montserrat", 30, "bold"), fill="white")

        can.create_text(390, 300, text="Nom", font=("Montserrat", 18, "bold"), fill="white")
        entryLabel = tk.Entry(can, font=("Montserrat", 18, "bold"), bg="white", fg="black", justify="center")
        entryLabel.place(x=430, y=285)

        buttonRecherche = tk.Button(can, text="Créer", padx=23, font=("Montserrat", 18, "bold"), pady=0, bg="#AC1E44",
                                 fg="white")
        buttonRecherche.place(x=550, y=420)