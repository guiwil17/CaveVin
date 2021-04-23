import tkinter.filedialog
import tkinter as tk
from PIL import Image, ImageTk, Image
import socket
import json
import PageAccueil
import base64
import requests
from Crypto.Cipher import AES

class PageAjouterVin(tk.Frame):
    def __init__(self, parent, controller, attr=None):
        tk.Frame.__init__(self, parent)
        self.config(width=600, height=400)
        can = tk.Canvas(self, width=600, height=400)
        self.img = ImageTk.PhotoImage(file="img/bouteilles.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)
        print(attr)
        self.entryPhoto = ""

        can.create_text(300, 40, text="Ajouter un Vin", font=("Montserrat", 22, "bold"), fill="white")

        self.imgHome = tk.PhotoImage(file="img/home.png")
        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame(PageAccueil.PageAccueil))
        buttonHome.place(x=5,y=5)

        def choisir_photo(event=None):
            filename = tk.filedialog.askopenfilename(initialdir="/", title="Choisir une photo", filetypes=(("jpg files", "*.jpg"), ("PNG files", "*.png"), ("all files", "*.*")))
            self.entryPhoto = filename

        can.create_text(150, 80, text="Photo", font=("Montserrat", 12, "bold"), fill="white")

        buttonPhoto = tk.Button(can, text="Choisir une photo", padx=23, font=("Montserrat", 11), pady=0, bg="#AC1E44", fg="white", command=choisir_photo)
        buttonPhoto.place(x=230, y=66)

        can.create_text(150, 125, text="Nom", font=("Montserrat", 12, "bold"), fill="white")
        entryNom = tk.Entry(can, font=("Montserrat", 12, "bold"), bg="white", fg="black", justify="center")
        entryNom.place(x=230, y=115)

        can.create_text(150, 175, text="Année", font=("Montserrat", 12, "bold"), fill="white")
        entryAnnee = tk.Entry(can, font=("Montserrat", 12, "bold"), bg="white", fg="black", show="*", justify="center")
        entryAnnee.place(x=230, y=165)

        can.create_text(150, 225, text="Type", font=("Montserrat", 12, "bold"), fill="white")
        entryType = tk.Entry(can, font=("Montserrat", 12, "bold"), bg="white", fg="black", show="*", justify="center")
        entryType.place(x=230, y=215)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("93.7.175.167", 1111))

        m = {"fonction": "get_caves", "paramètres": [2]}
        data = json.dumps(m)

        s.sendall(bytes(data, encoding="utf-8"))

        r = s.recv(9999999)
        r = r.decode("utf-8")
        data = json.loads(r)
        if (data["status"] == 200 and data["valeurs"]):
            OptionList = data["valeurs"]
        variable = tk.StringVar(self)
        variable.set(OptionList[0])

        can.create_text(150, 275, text="Cave", font=("Montserrat", 12, "bold"), fill="white")
        entryCave = tk.OptionMenu(self, variable, *OptionList)
        entryCave.pack(side="top")
        entryCave.place(x=230, y=265)

        def callback(*args):
            print("The selected item is {}".format(variable.get()))

        variable.trace("w", callback)

        can.create_text(150, 325, text="Commentaire", font=("Montserrat", 12, "bold"), fill="white")
        entryCommentaire = tk.Entry(can, font=("Montserrat", 12, "bold"), bg="white", fg="black", show="*", justify="center")
        entryCommentaire.place(x=230, y=315)


        def ajouter_vin():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))
            with open("img/cave.jpg", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())

            my_string = my_string.decode('utf-8')

            print(entryNom)
            print(entryAnnee)
            print(entryType)
            print(variable.get())
            print(entryCommentaire)

            m = {"fonction": "ajouter_vin", "paramètres": [entryNom.get(),entryAnnee.get(),entryType.get(),variable.get(),entryCommentaire.get(),my_string]}
            data = json.dumps(m)
            print(data)
            #data = json.loads(my_string)

            s.sendall(bytes(data, encoding="utf-8"))
            # envoi de l'image

            r = s.recv(9999999)
            r = r.decode("utf-8")
            data = json.loads(r)

            if (data["status"] == 200 and data["valeurs"]):
                controller.show_frame(PageAccueil.PageAccueil)
                print("ici")          

        buttonRecherche = tk.Button(can, text="Ajouter", padx=23, font=("Montserrat", 12, "bold"), pady=0, bg="#AC1E44", fg="white", command=ajouter_vin)
        buttonRecherche.place(x=250, y=350)