import tkinter.filedialog
import tkinter as tk
from PIL import Image, ImageTk

import PageAccueil

class PageAjouterCave(tk.Frame):
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

        can.create_text(300, 60, text="Ajouter une Cave", font=("Montserrat", 22, "bold"), fill="white")

        can.create_text(150, 125, text="Numéro", font=("Montserrat", 12, "bold"), fill="white")
        entryNumero = tk.Entry(can, font=("Montserrat", 12, "bold"), bg="white", fg="black", justify="center")
        entryNumero.place(x=230, y=115)

        can.create_text(150, 175, text="Rue", font=("Montserrat", 12, "bold"), fill="white")
        entryRue = tk.Entry(can, font=("Montserrat", 12, "bold"), bg="white", fg="black", show="*", justify="center")
        entryRue.place(x=230, y=165)

        can.create_text(150, 225, text="Ville", font=("Montserrat", 12, "bold"), fill="white")
        entryVille = tk.Entry(can, font=("Montserrat", 12, "bold"), bg="white", fg="black", show="*", justify="center")
        entryVille.place(x=230, y=215)

        can.create_text(150, 275, text="Code Postal", font=("Montserrat", 12, "bold"), fill="white")
        entryCP = tk.Entry(can, font=("Montserrat", 12, "bold"), bg="white", fg="black", show="*", justify="center")
        entryCP.place(x=230, y=265)

        buttonRecherche = tk.Button(can, text="Créer", padx=23, font=("Montserrat", 12, "bold"), pady=0, bg="#AC1E44",
                                 fg="white")
        buttonRecherche.place(x=250, y=320)