import tkinter.filedialog
import tkinter as tk
from PIL import Image, ImageTk, Image
import socket
import json
import PageAccueil
import base64
import requests

class ModifierVin(tk.Frame):
    def __init__(self, parent, controller, id_user, id_vin):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("93.7.175.167", 1111))

        m = {"fonction": "get_vin", "paramètres": [id_user, id_vin]}
        data = json.dumps(m)


        s.sendall(bytes(data, encoding="utf-8"))
        r = s.recv(9999999)
        r = r.decode("utf-8")
        data = json.loads(r)
        s.close()
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect(("93.7.175.167", 1111))

        m2 = {"fonction": "get_caves", "paramètres": [id_user]}
        data2 = json.dumps(m2)

        s2.sendall(bytes(data2, encoding="utf-8"))
        r = s2.recv(9999999)
        r = r.decode("utf-8")
        data2 = json.loads(r)

        s2.close()

        tk.Frame.__init__(self, parent)
        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/bouteilles.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)
        self.entryPhoto = ""

        can.create_text(700, 110, text="Modifier un Vin", font=("Montserrat", 35, "bold"), fill="white")

        self.imgHome = tk.PhotoImage(file="img/home.png")
        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame("PageAccueil", [id_user]))
        buttonHome.place(x=5, y=5)

        def choisir_photo(event=None):
            filename = tk.filedialog.askopenfilename(initialdir="/", title="Choisir une photo", filetypes=(
            ("jpg files", "*.jpg"), ("PNG files", "*.png"), ("all files", "*.*")))
            self.entryPhoto = filename

        can.create_text(475, 200, text="Photo", font=("Montserrat", 18, "bold"), fill="white")

        buttonPhoto = tk.Button(can, text="Choisir une photo", padx=49, font=("Montserrat", 15), pady=0, bg="#AC1E44",
                                fg="white", command=choisir_photo)
        buttonPhoto.place(x=550, y=185)

        can.create_text(480, 250, text="Nom", font=("Montserrat", 18, "bold"), fill="white")
        entryNom = tk.Entry(can, font=("Montserrat", 18, "bold"), bg="white", fg="black", justify="center")
        entryNom.place(x=550, y=235)
        entryNom.insert(0, data["valeurs"][0]["Nom"])

        can.create_text(472, 300, text="Année", font=("Montserrat", 18, "bold"), fill="white")
        entryAnnee = tk.Entry(can, font=("Montserrat", 18, "bold"), bg="white", fg="black", justify="center")
        entryAnnee.place(x=550, y=285)
        entryAnnee.insert(0, data["valeurs"][0]["Annee"])

        can.create_text(478, 350, text="Type", font=("Montserrat", 18, "bold"), fill="white")
        entryType = tk.Entry(can, font=("Montserrat", 18, "bold"), bg="white", fg="black", justify="center")
        entryType.place(x=550, y=335)
        entryType.insert(0, data["valeurs"][0]["Type"])

        if (data2["status"] == 200 and data2["valeurs"]):
            OptionList = data2["valeurs"]
        variable = tk.StringVar(self)
        variable.set(OptionList[OptionList.index(data["valeurs"][0]["label"])])

        can.create_text(478, 400, text="Cave", font=("Montserrat", 18, "bold"), fill="white")
        entryCave = tk.OptionMenu(self, variable, *OptionList)
        entryCave.config(bg="#AC1E44", fg="white", font=12, width=20)
        entryCave["highlightthickness"] = 0
        entryCave["menu"].config(bg="#AC1E44", fg="white", font=12)
        entryCave.pack(side="top")
        entryCave.place(x=550, y=385)

        can.create_text(458, 450, text="Quantité", font=("Montserrat", 18, "bold"), fill="white")
        entryQuantity = tk.Entry(can, font=("Montserrat", 18, "bold"), bg="white", fg="black", justify="center")
        entryQuantity.place(x=550, y=435)
        entryQuantity.insert(0, data["valeurs"][0]["Quantite"])

        can.create_text(435, 500, text="Échangeable", font=("Montserrat", 18, "bold"), fill="white")
        self.tradable = tk.BooleanVar()
        self.tradable.set(True if (data["valeurs"][0]["Echangeable"]) else False)

        self.cb = tk.Checkbutton(self, onvalue=True, offvalue=False,
                                 variable=self.tradable,
                                 )
        self.cb.place(x=550, y=485)

        can.create_text(435, 550, text="Commentaire", font=("Montserrat", 18, "bold"), fill="white")
        entryCommentaire = tk.Text(can, font=("Montserrat", 18, "bold"), bg="white", fg="black", height=3, width=21)
        entryCommentaire.place(x=550, y=535)
        entryCommentaire.insert("1.0", data["valeurs"][0]["Notation"])
        def modifier_vin():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            with open("img/cave.jpg", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())

            my_string = my_string.decode('utf-8')

            m = {"fonction": "change_vin",
                 "paramètres": [entryNom.get(), entryAnnee.get(), entryType.get(), variable.get(),
                                entryCommentaire.get("1.0", 'end-1c'),
                                my_string,
                                str(self.tradable.get()),
                                entryQuantity.get(), id_vin, id_user]}
            data = json.dumps(m)
            # data = json.loads(my_string)

            s.sendall(bytes(data, encoding="utf-8"))
            # envoi de l'image

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)

            if (data["status"] == 200 and data["valeurs"]):
                controller.show_frame("MesCaves", [id_user])


        buttonModifier = tk.Button(can, text="Modifier", padx=23, font=("Montserrat", 18, "bold"), pady=0, bg="#AC1E44",
                                    fg="white", command=modifier_vin)
        buttonModifier.place(x=600, y=650)