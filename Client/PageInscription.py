import tkinter.filedialog
import tkinter as tk
import hashlib
import socket
import json
from PIL import Image, ImageTk

import PageConnexion

class PageInscription(tk.Frame):

    def __init__(self, parent, controller,p):
        def inscription(event=None):
            entryName = self.entryName.get()
            entryFirstName = self.entryFirstName.get()
            entryLogin = self.entryLogin.get()
            entryPhone = self.entryPhone.get()
            entryPass = self.entryPass.get()
            entryConfirmPass = self.entryConfirmPass.get()
            if(entryLogin==""):
                can.create_text(600, 200, text=" Erreur : \n Pseudo vide", font=fonts2,
                                fill="#AC1E44")
            elif(entryPass!=entryConfirmPass or entryPass==""):
                can.create_text(650, 300, text=" Erreur : \n Mots de passes\n non identiques ou vide", font=fonts2, fill="#AC1E44")
            else:
                password_hash = hashlib.sha256(entryPass.encode()).hexdigest()

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("93.7.175.167", 1111))

                m = {"fonction": "create_account", "paramètres": [entryName, entryFirstName, entryLogin, entryPhone, password_hash]}
                data = json.dumps(m)

                s.sendall(bytes(data, encoding="utf-8"))

                r = s.recv(9999999)
                r = r.decode("utf-8")
                data = json.loads(r)

                controller.show_frame(PageConnexion.PageConnexion)


        tk.Frame.__init__(self, parent)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/signin.jpg")
        can.create_image(0, 0, anchor="nw", image=self.img)
        can.place(x=0, y=0)
        fonts = ("Time New Roman", 35, "bold")
        fonts2 = ("Time New Roman", 18)
        can.create_text(325, 100, text="Création de compte", font=fonts, fill="black")

        can.create_text(180, 250, text="Nom", font=fonts2, fill="black")
        can.create_text(170, 300, text="Prénom", font=fonts2, fill="black")
        can.create_text(170, 350, text="Pseudo", font=fonts2, fill="black")
        can.create_text(160, 400, text="Téléphone", font=fonts2, fill="black")
        can.create_text(150, 450, text="Mot de passe", font=fonts2, fill="black")
        can.create_text(150, 500, text="Confirmation \nmot de passe", font=fonts2, fill="black")

        self.entryName = tk.Entry(can, font=fonts2, fg="black", justify="center")
        self.entryName.place(x=250, y=235)

        self.entryFirstName = tk.Entry(can, font=fonts2, fg="black", justify="center")
        self.entryFirstName.place(x=250, y=285)

        self.entryLogin = tk.Entry(can, font=fonts2, fg="black", justify="center")
        self.entryLogin.place(x=250, y=335)

        self.entryPhone = tk.Entry(can, font=fonts2, fg="black", justify="center")
        self.entryPhone.place(x=250, y=385)

        self.entryPass = tk.Entry(can, font=fonts2, fg="black", show="*", justify="center")
        self.entryPass.place(x=250, y=435)

        self.entryConfirmPass = tk.Entry(can, font=fonts2, fg="black", show="*", justify="center")
        self.entryConfirmPass.place(x=250, y=485)


        buttonValid = tk.Button(can, text="Créer le compte", padx=50, font=fonts2, pady=0, bg="#AC1E44", fg="white", command=inscription)
        buttonValid.place(x=160, y=580)

        buttonRetour = tk.Button(can, text="Retour à la page de connexion", font=("Time New Roman", 16), pady=0, bg="#AC1E44", fg="white", command=lambda: controller.show_frame(PageConnexion.PageConnexion))
        buttonRetour.place(x=155, y=650)