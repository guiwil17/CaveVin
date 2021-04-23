import tkinter.filedialog
import tkinter as tk
import hashlib
import socket
import json
import Pages
from PIL import Image, ImageTk

import PageInscription
import PageAccueil

class PageConnexion(tk.Frame, Pages.Pages):
    def __init__(self, parent, controller):


        def connexion(event=None):
            entryUser = self.entryUser.get()
            password = self.entryPass.get()
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "login", "paramètres": [entryUser, password_hash]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)
            print(self.focus_get())
            if(data["status"] == 200 and data["valeurs"]):
                Pages.Pages.id_utilisateur = data["valeurs"]
                controller.show_frame(PageAccueil.PageAccueil)


        tk.Frame.__init__(self, parent)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/login.jpg")
        can.create_image(0, 0, anchor="nw", image=self.img)
        can.place(x=0, y=0)
        titre = ("Time New Roman", 35, "bold")
        fonts = ("Time New Roman", 18, "bold")
        fonts2 = ("Time New Roman", 16)

        can.create_text(500, 100, text="Connexion", font=titre)
        can.create_text(300, 285, text="Pseudo", font=fonts)
        can.create_text(270, 335, text="Mot de passe", font=fonts)

        self.entryUser = tk.Entry(can, font=fonts, fg="black", justify="center")
        self.entryUser.place(x=370, y=270)

        self.entryPass = tk.Entry(can, font=fonts, fg="black", show="*", justify="center")
        self.entryPass.place(x=370, y=320)

        buttonValid = tk.Button(can, text="Se connecter", padx=50, font=fonts, pady=0, bg="#AC1E44", fg="white", command=connexion)
        buttonValid.place(x=370, y=400)

        buttonCreer = tk.Button(can, text="Créer un compte", font=fonts2, pady=0, bg="#AC1E44",
                                 fg="white", command=lambda: controller.show_frame(PageInscription.PageInscription))
        buttonCreer.place(x=420, y=480)