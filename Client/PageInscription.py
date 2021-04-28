import tkinter.filedialog
import tkinter as tk
import hashlib
import socket
import json
from PIL import Image, ImageTk

import PageConnexion

class PageInscription(tk.Frame):

    def __init__(self, parent, controller):
        def get_Pseudos():

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "get_Pseudos",
                 "paramètres": []}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            s.close()
            data = json.loads(r)

            return data["valeurs"]

        def inscription(event=None):
            entryName = self.entryName.get()
            entryFirstName = self.entryFirstName.get()
            entryLogin = self.entryLogin.get()
            entryPhone = self.entryPhone.get()
            entryPass = self.entryPass.get()
            entryConfirmPass = self.entryConfirmPass.get()
            param = []
            data = get_Pseudos()
            if(entryLogin=="" or entryLogin in data):
                param.append("Pseudo")
            if(entryPass!=entryConfirmPass or entryPass==""):
                param.append("Password")
            if(entryPhone == "" or len(entryPhone) != 10 or entryPhone.isdigit() != True):
                param.append("Phone")
            if(entryName == ""):
                param.append("Name")
            if (entryFirstName == ""):
                param.append("Prenom")
            if(len(param) != 0):
                Mbox(param)
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
                s.close()

                controller.show_frame("PageConnexion")


        class Mbox(object):

            root = None

            def __init__(self,param):
                tki = tkinter
                self.top = tki.Toplevel(Mbox.root)
                self.top.geometry("400x250")
                self.top.title("Erreur")

                frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
                frm.pack(fill='both', expand=True)

                label = tki.Label(frm, text="Des erreurs ont été observées : ")
                label.place(x=80, y=10)

                label = tki.Label(frm, text="")
                label.place(x=100, y=100)

                for i in param:
                    if (i == "Pseudo"):
                        label = tki.Label(frm, text="Le pseudo est vide")
                        label.place(x=80, y=30)
                    elif (i == "Phone"):
                        label = tki.Label(frm, text="Le téléphone doit avoir 10 chiffres uniquement")
                        label.place(x=80, y=50)
                    elif (i == "Name"):
                        label = tki.Label(frm, text="Le Nom ne doit pas être vide")
                        label.place(x=80, y=70)
                    elif (i == "Prenom"):
                        label = tki.Label(frm, text="Le Prénom ne doit pas être vide")
                        label.place(x=80, y=90)
                    else:
                        label = tki.Label(frm, text="Le mot de passe et la confirmation doivent être identique")
                        label.place(x=80, y=110)
                b_modifier = tki.Button(frm, text='Ok')
                b_modifier['command'] = lambda: self.Ok()
                b_modifier.place(x=190, y=150)

            def Ok(self):
                self.top.destroy()


        tk.Frame.__init__(self, parent)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/signin.jpg")
        can.create_image(0, 0, anchor="nw", image=self.img)
        can.place(x=0, y=0)
        fonts = ("Time New Roman", 35, "bold")
        fonts2 = ("Time New Roman", 18)
        can.create_text(400, 100, text="Création de compte", font=fonts, fill="black")

        can.create_text(240, 250, text="Nom", font=fonts2, fill="black")
        can.create_text(225, 300, text="Prénom", font=fonts2, fill="black")
        can.create_text(225, 350, text="Pseudo", font=fonts2, fill="black")
        can.create_text(210, 400, text="Téléphone", font=fonts2, fill="black")
        can.create_text(195, 450, text="Mot de passe", font=fonts2, fill="black")
        can.create_text(195, 500, text="Confirmation \nmot de passe", font=fonts2, fill="black")

        self.entryName = tk.Entry(can, font=fonts2, fg="black", justify="center")
        self.entryName.place(x=280, y=235)

        self.entryFirstName = tk.Entry(can, font=fonts2, fg="black", justify="center")
        self.entryFirstName.place(x=280, y=285)

        self.entryLogin = tk.Entry(can, font=fonts2, fg="black", justify="center")
        self.entryLogin.place(x=280, y=335)

        self.entryPhone = tk.Entry(can, font=fonts2, fg="black", justify="center")
        self.entryPhone.place(x=280, y=385)

        self.entryPass = tk.Entry(can, font=fonts2, fg="black", show="*", justify="center")
        self.entryPass.place(x=280, y=435)

        self.entryConfirmPass = tk.Entry(can, font=fonts2, fg="black", show="*", justify="center")
        self.entryConfirmPass.place(x=280, y=485)


        buttonValid = tk.Button(can, text="Créer le compte", padx=50, font=fonts2, pady=0, bg="#AC1E44", fg="white", command=inscription)
        buttonValid.place(x=270, y=580)

        buttonRetour = tk.Button(can, text="Retour à la page de connexion", font=("Time New Roman", 16), pady=0, bg="#AC1E44", fg="white", command=lambda: controller.show_frame("PageConnexion"))
        buttonRetour.place(x=263, y=650)