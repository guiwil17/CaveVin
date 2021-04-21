import tkinter.filedialog
import tkinter as tk

import PageAccueil


class PageRecherche(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(width=600, height=400)
        can = tk.Canvas(self, width=600, height=400)
        self.img = tk.PhotoImage(file="img/cave.png")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)


        can.create_text(300, 80, text="Rechercher une Cave", font=("Montserrat", 22, "bold"), fill="white")

        self.imgHome = tk.PhotoImage(file="img/home.png")
        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame(PageAccueil.PageAccueil))
        buttonHome.place(x=5,y=5)

        can.create_text(164, 165, text="Nom du propriétaire", font=("Montserrat", 12, "bold"), fill="white")

        can.create_text(150, 215, text="Prénom du propriétaire", font=("Montserrat", 12, "bold"), fill="white")

        entryNom = tk.Entry(can, font=("Montserrat", 12, "bold"), bg="white", fg="black", justify="center")
        entryNom.place(x=270, y=150)

        entryPrenom = tk.Entry(can, font=("Montserrat", 12, "bold"), bg="white", fg="black", show="*", justify="center")
        entryPrenom.place(x=270, y=200)

        buttonRecherche = tk.Button(can, text="Rechercher", padx=23, font=("Montserrat", 12, "bold"), pady=0, bg="#AC1E44",
                                 fg="white")
        buttonRecherche.place(x=250, y=260)

        buttonAleatoire = tk.Button(can, text="Cave Aléatoire", padx=10, font=("Montserrat", 12, "bold"), pady=0,
                                 bg="#AC1E44", fg="white")
        buttonAleatoire.place(x=250, y=310)