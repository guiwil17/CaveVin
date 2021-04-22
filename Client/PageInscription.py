import tkinter.filedialog
import tkinter as tk
import hashlib
import socket
import json
from PIL import Image, ImageTk

import PageConnexion

class PageInscription(tk.Frame):

    def __init__(self, parent, controller):
        def inscription(event=None):
            entryName = self.entryName.get()
            entryFirstName = self.entryFirstName.get()
            entryLogin = self.entryLogin.get()
            entryPhone = self.entryPhone.get()
            entryPass = self.entryPass.get()
            entryConfirmPass = self.entryConfirmPass.get()
            if(entryPass!=entryConfirmPass):
                can.create_text(520, 230, text=" Erreur : \n Mots de passes\n non identiques", font=fonts, fill="#AC1E44")
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

                print(data)


        tk.Frame.__init__(self, parent)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/signin.jpg")
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

        self.entryName = tk.Entry(can, font=fonts, fg="black", justify="center")
        self.entryName.place(x=220, y=65)

        self.entryFirstName = tk.Entry(can, font=fonts, fg="black", justify="center")
        self.entryFirstName.place(x=220, y=100)

        self.entryLogin = tk.Entry(can, font=fonts, fg="black", justify="center")
        self.entryLogin.place(x=220, y=133)

        self.entryPhone = tk.Entry(can, font=fonts, fg="black", justify="center")
        self.entryPhone.place(x=220, y=166)

        self.entryPass = tk.Entry(can, font=fonts, fg="black", show="*", justify="center")
        self.entryPass.place(x=220, y=200)

        self.entryConfirmPass = tk.Entry(can, font=fonts, fg="black", show="*", justify="center")
        self.entryConfirmPass.place(x=220, y=235)


        buttonValid = tk.Button(can, text="Créer le compte", padx=50, font=fonts, pady=0, bg="#AC1E44", fg="white", command=inscription)
        buttonValid.place(x=190, y=300)

        buttonRetour = tk.Button(can, text="Retour à la page de connexion", font=fonts2, pady=0, bg="#AC1E44", fg="white", command=lambda: controller.show_frame(PageConnexion.PageConnexion))
        buttonRetour.place(x=230, y=350)