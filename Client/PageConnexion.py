import tkinter.filedialog
import tkinter as tk
import hashlib
import socket
import json

import PageInscription

class PageConnexion(tk.Frame):
    def __init__(self, parent, controller):

        def connexion(event=None):
            entryUser = self.entryUser.get()
            password = self.entryPass.get()
            print("ici")
            print(entryUser)
            print(password)
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "login", "paramètres": [entryUser, password_hash]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)

            print(data)

        tk.Frame.__init__(self, parent)
        can = tk.Canvas(self, width=600, height=400)
        self.img = tk.PhotoImage(file="img/login.png")
        can.create_image(0, 0, anchor="nw", image=self.img)
        can.place(x=0, y=0)
        titre = ("Time New Roman", 20, "bold")
        fonts = ("Time New Roman", 15, "bold")
        fonts2 = ("Time New Roman", 10)

        can.create_text(330, 20, text="Connexion", font=titre)
        can.create_text(180, 165, text="Pseudo", font=fonts)
        can.create_text(150, 215, text="Mot de passe", font=fonts)

        self.entryUser = tk.Entry(can, font=fonts, fg="black", justify="center")
        self.entryUser.place(x=220, y=150)

        self.entryPass = tk.Entry(can, font=fonts, fg="black", show="*", justify="center")
        self.entryPass.place(x=220, y=200)

        buttonValid = tk.Button(can, text="Se connecter", padx=50, font=fonts, pady=0, bg="#AC1E44", fg="white", command=connexion)
        buttonValid.place(x=210, y=300)

        buttonRetour = tk.Button(can, text="Créer un compte", font=fonts2, pady=0, bg="#AC1E44",
                                 fg="white", command=lambda: controller.show_frame(PageInscription.PageInscription))
        buttonRetour.place(x=280, y=350)