import tkinter.filedialog
import tkinter as tk
import PageConnexion

class PageInscription(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        can = tk.Canvas(self, width=600, height=400)
        self.img = tk.PhotoImage(file="img/singin.png")
        can.create_image(0, 0, anchor="nw", image=self.img)
        can.place(x=0, y=0)
        fonts = ("Time New Roman", 15, "bold")
        fonts2 = ("Time New Roman", 10)
        can.create_text(325, 20, text="Création de compte", font=fonts, fill="black")

        can.create_text(180, 75, text="Nom", font=fonts, fill="black")
        can.create_text(170, 110, text="Prénom", font=fonts, fill="black")
        can.create_text(170, 145, text="Pseudo", font=fonts, fill="black")
        can.create_text(160, 175, text="Téléphone", font=fonts, fill="black")
        can.create_text(150, 210, text="Mot de passe", font=fonts, fill="black")
        can.create_text(150, 250, text="Confirmation \nmot de passe", font=fonts, fill="black")

        entryName = tk.Entry(can, font=fonts, fg="black", justify="center")
        entryName.place(x=220, y=65)

        entryFirstName = tk.Entry(can, font=fonts, fg="black", justify="center")
        entryFirstName.place(x=220, y=100)

        entryPhone = tk.Entry(can, font=fonts, fg="black", justify="center")
        entryPhone.place(x=220, y=133)

        entryPhone = tk.Entry(can, font=fonts, fg="black", justify="center")
        entryPhone.place(x=220, y=166)

        entryPass = tk.Entry(can, font=fonts, fg="black", show="*", justify="center")
        entryPass.place(x=220, y=200)

        entryConfirmPass = tk.Entry(can, font=fonts, fg="black", show="*", justify="center")
        entryConfirmPass.place(x=220, y=235)


        buttonValid = tk.Button(can, text="Créer le compte", padx=50, font=fonts, pady=0, bg="#AC1E44", fg="white")
        buttonValid.place(x=190, y=300)

        buttonRetour = tk.Button(can, text="Retour à la page de connexion", font=fonts2, pady=0, bg="#AC1E44", fg="white", command=lambda: controller.show_frame(PageConnexion.PageConnexion))
        buttonRetour.place(x=230, y=350)