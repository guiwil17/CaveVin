import tkinter.filedialog
import tkinter as tk

class PageAjouterCave(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(width=600, height=400)
        can = tk.Canvas(self, width=600, height=400)
        self.img = tk.PhotoImage(file="img/cave2.png")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)


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