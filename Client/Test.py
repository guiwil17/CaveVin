import tkinter as tk
import socket
import json
import hashlib

LARGE_FONT = ("Verdana", 12)



class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (PageOne, PageTwo):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageOne)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class PageOne(tk.Frame):

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
        # LabelTitre = Label(can, text="Connexion", font=fonts, bg="#717113",fg="white")
        # LabelTitre.place(x=250, y=40)

        can.create_text(180, 165, text="Pseudo", font=fonts)

        # labelUser = Label(can, text="Pseudo", font=fonts, bg="#717113", fg="white")
        # labelUser.place(x=140, y=150)

        can.create_text(150, 215, text="Mot de passe", font=fonts)

        # labelpass = Label(can, text="Mot de passe", font=fonts, fg="black")
        # labelpass.place(x=85, y=200)


        self.entryUser = tk.Entry(can, font=fonts, fg="black", justify="center")
        self.entryUser.place(x=220, y=150)

        self.entryPass = tk.Entry(can, font=fonts, fg="black", show="*", justify="center")
        self.entryPass.place(x=220, y=200)

        buttonValid = tk.Button(can, text="Se connecter", padx=50, font=fonts, pady=0, bg="#AC1E44", fg="white", command=connexion)
        buttonValid.place(x=210, y=300)

        buttonRetour = tk.Button(can, text="Créer un compte", font=fonts2, pady=0, bg="#AC1E44",
                                 fg="white", command=lambda: controller.show_frame(PageTwo))
        buttonRetour.place(x=280, y=350)



class PageTwo(tk.Frame):

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

        buttonRetour = tk.Button(can, text="Retour à la page de connexion", font=fonts2, pady=0, bg="#AC1E44", fg="white", command=lambda: controller.show_frame(PageOne))
        buttonRetour.place(x=230, y=350)


app = SeaofBTCapp()
app.geometry('600x400')
app.resizable(width=False, height=False)



app.mainloop()