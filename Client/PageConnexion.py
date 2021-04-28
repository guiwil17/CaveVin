import tkinter.filedialog
import tkinter as tk
import hashlib
import socket
import json
from PIL import Image, ImageTk
import PageInscription
import PageAccueil

class PageConnexion(tk.Frame):
    def __init__(self, parent, controller):


        def connexion(event=None):
            entryUser = self.entryUser.get()
            password = self.entryPass.get()
            param = []
            if(entryUser == ""):
                param.append("Pseudo")
            if(password == ""):
                param.append("Password")
            if(len(param) != 0):
                Mbox(param, "Invalide")
            else:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("93.7.175.167", 1111))

                m = {"fonction": "login", "paramètres": [entryUser, password_hash]}
                data = json.dumps(m)

                s.sendall(bytes(data, encoding="utf-8"))

                r = s.recv(9999999)
                r = r.decode("utf-8")
                data = json.loads(r)
                s.close()
                if(data["status"] == 200 and data["valeurs"]):
                    controller.show_frame("PageAccueil", [data["valeurs"]])
                else:
                    Mbox(param, "")


        tk.Frame.__init__(self, parent)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/login.jpg")
        can.create_image(0, 0, anchor="nw", image=self.img)
        can.place(x=0, y=0)
        titre = ("Time New Roman", 35, "bold")
        fonts = ("Time New Roman", 18, "bold")
        fonts2 = ("Time New Roman", 16)

        class Mbox(object):

            root = None

            def __init__(self, param, type):
                tki = tkinter
                self.top = tki.Toplevel(Mbox.root)
                self.top.geometry("400x250")
                self.top.title("Erreur")

                frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
                frm.pack(fill='both', expand=True)


                if(type == "Invalide"):
                    label = tki.Label(frm, text="Des erreurs ont été observées : ")
                    label.place(x=80, y=10)

                    label = tki.Label(frm, text="")
                    label.place(x=100, y=100)

                    for i in param:
                        if (i == "Pseudo"):
                            label = tki.Label(frm, text="Le pseudo est vide")
                            label.place(x=80, y=30)
                        else:
                            label = tki.Label(frm, text="Le mot de passe ne doit pas être vide")
                            label.place(x=80, y=50)

                    b_modifier = tki.Button(frm, text='Ok')
                    b_modifier['command'] = lambda: self.Ok()
                    b_modifier.place(x=190, y=150)
                else:
                    label = tki.Label(frm, text="L'utilisateur n'existe pas ou le mot de passe est incorrect ")
                    label.place(x=50, y=70)

                    b_modifier = tki.Button(frm, text='Ok')
                    b_modifier['command'] = lambda: self.Ok()
                    b_modifier.place(x=190, y=150)

            def Ok(self):
                self.top.destroy()

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
                                 fg="white", command=lambda: controller.show_frame("PageInscription"))
        buttonCreer.place(x=420, y=480)