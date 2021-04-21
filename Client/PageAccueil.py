import tkinter.filedialog
import tkinter as tk

import PageAjouterCave
import PageAjouterVin
import PageRecherche
import PageConnexion
import PageInscription

class PageAccueil(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        can = tk.Canvas(self, width=600, height=400)
        self.img = tk.PhotoImage(file="img/accueil.png")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)

        can.create_text(300, 80, text="Accueil", font=("Montserrat", 32, "bold"), fill="white")

        button1 = tk.Button(can, text="Mes Caves", padx=59, font=("Montserrat", 12, "bold"), pady=0, bg="#AC1E44",
                         fg="white")
        button1.place(x=50, y=200)
        button2 = tk.Button(can, text="Visiter des Caves", padx=30, font=("Montserrat", 12, "bold"), pady=0, bg="#AC1E44",
                         fg="white", command=lambda: controller.show_frame(PageRecherche.PageRecherche))
        button2.place(x=320, y=200)