import tkinter.filedialog
import tkinter as tk
from tkinter.ttk import *
import socket
import json
import PageAccueil
from PIL import Image, ImageTk
import PageAjouterVin
import PageAjouterCave
import base64
import io
from io import StringIO


class PageMesDemandes(tk.Frame):
    def __init__(self, parent, controller, id_user):

        tk.Frame.__init__(self, parent)

        def recupDemandes():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("93.7.175.167", 1111))

            m = {"fonction": "get_demandeRecu", "paramètres": [id_user]}
            data = json.dumps(m)

            s.sendall(bytes(data, encoding="utf-8"))

            r = s.recv(9999999)
            r = r.decode("utf-8")
            s.close()
            data = json.loads(r)
            if (data["status"] == 200 and data["valeurs"]):
                return data['valeurs']
            else:
                return []



        self.data = recupDemandes()

        self.config(width=1200, height=800)
        can = tk.Canvas(self, width=1200, height=800)
        self.img = ImageTk.PhotoImage(file="img/echange1.jpg")
        can.create_image(0, 0, anchor=tk.NW, image=self.img)
        can.place(x=0, y=0)
        style = Style(can)
        style.configure('Treeview', rowheight=50)

        self.imgHome = tk.PhotoImage(file="img/home.png")
        self.imgcave = tk.PhotoImage(file="img/MesCaves.png")
        self.imgEmailReceive = tk.PhotoImage(file="img/email_recu.png")
        self.imgEmailSend = tk.PhotoImage(file="img/email_envoye.png")

        buttonHome = tk.Button(can, image=self.imgHome, command=lambda: controller.show_frame("PageAccueil",[id_user]))
        buttonHome.place(x=5,y=5)

        button_Ajouter_cave = tk.Button(can, image=self.imgcave, command=lambda: controller.show_frame("MesCaves", [id_user]))
        button_Ajouter_cave.place(x=60, y=5)

        titre = ("Time New Roman", 30, "bold")

        can.create_text(630, 90, text="Mes demandes reçues", font=titre, fill="white")

        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]

        style = Style()
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))

        class Mbox(object):

            root = None

            def __init__(self, id_echange, pseudo, id_user):
                tki = tkinter
                self.top = tki.Toplevel(Mbox.root)
                self.top.title("Action")
                self.top.geometry("400x200")
                frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
                frm.pack(fill='both', expand=True)

                label = tki.Label(frm, text="Quelle action voulez-vous réaliser ?")
                label.pack(padx=4, pady=4)

                self.valider = ImageTk.PhotoImage(file="img/checked.png")
                self.refuse = ImageTk.PhotoImage(file="img/remove.png")

                b_submit = tki.Button(frm, image=self.valider)
                b_submit['command'] = lambda: self.accepter(id_echange)
                b_submit.place(x=100, y=50)


                b_cancel = tki.Button(frm, image=self.refuse)
                b_cancel['command'] = lambda: self.refuser(id_echange)
                b_cancel.place(x=250, y=50)

                regarderCave = tki.Button(frm, text="Regarder la Cave de l'utilisateur")
                regarderCave['command'] = lambda: self.visiterCave(pseudo, id_user)
                regarderCave.place(x=105, y=120)

            def accepter(self, id_echange):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("93.7.175.167", 1111))

                m = {"fonction": "accept_echange", "paramètres": [id_echange]}
                data = json.dumps(m)

                s.sendall(bytes(data, encoding="utf-8"))

                r = s.recv(9999999)
                r = r.decode("utf-8")
                s.close()
                data = json.loads(r)
                mise_a_jour()
                self.top.destroy()

            def visiterCave(self, pseudo, id_user):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("93.7.175.167", 1111))

                m = {"fonction": "get_id_user", "paramètres": [pseudo]}
                data = json.dumps(m)

                s.sendall(bytes(data, encoding="utf-8"))

                r = s.recv(9999999)
                r = r.decode("utf-8")
                data = json.loads(r)
                s.close()
                if (data["status"] == 200 and data["valeurs"]):
                    controller.show_frame("VisiterCaves", [id_user, int(data["valeurs"][0])])
                self.top.destroy()

            def refuser(self, id_echange):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("93.7.175.167", 1111))

                m = {"fonction": "refuse_echange", "paramètres": [id_echange]}
                data = json.dumps(m)

                s.sendall(bytes(data, encoding="utf-8"))

                r = s.recv(9999999)
                r = r.decode("utf-8")
                data = json.loads(r)
                s.close()
                mise_a_jour()
                self.top.destroy()
        

        def selectItem(a):
            curItem = self.tableau.focus()
            if(self.tableau.item(curItem)["values"][0] == "Pas encore répondu"):
                msg = Mbox(self.tableau.item(curItem)["values"][5], self.tableau.item(curItem)["values"][3], id_user)

        def mise_a_jour():
            self.data = recupDemandes()
            self.tableau.delete(*self.tableau.get_children())
            for d in self.data:
                if (d["Reponse"] == 0):
                    self.tableau.insert('', 'end', values=(
                        "Pas encore répondu", d["Nom_vin_moi"], d["Nom_vin_demandeur"], d["Pseudo"],
                        d["Date_demande"], d["id"]))
                else:
                    if (d["Echange"] == 1):
                        self.check = tk.PhotoImage(file="img/checked.png")
                        self.tableau.insert(parent='', index='end', values=(
                            "accepté", d["Nom_vin_moi"], d["Nom_vin_demandeur"], d["Pseudo"], d["Date_demande"],
                            d["id"]), tags=('accept',))
                    else:
                        self.tableau.insert('', 'end', values=(
                            "refusé", d["Nom_vin_moi"], d["Nom_vin_demandeur"], d["Pseudo"], d["Date_demande"],
                            d["id"]), tags=('refuse',))
            self.tableau.bind('<Double-1>', selectItem)
        #Tableau

        self.tableau = Treeview(can, columns=('','Mon vin', 'Vin proposé', 'Demandeur', 'Date de la demande'))
        self.tableau.pack(padx=147, pady=180)

        vsb = Scrollbar(can, orient="vertical", command=self.tableau.yview)
        vsb.pack(side='right', fill='y')
        self.tableau.configure(yscrollcommand=vsb.set)

        vsb.place(x=1081, y=180, height=527)

        self.tableau.column('',  width=150, stretch=tk.NO, anchor='center')
        self.tableau.column('Mon vin', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Vin proposé', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Demandeur', width=200, stretch=tk.NO, anchor='center')
        self.tableau.column('Date de la demande', width=200, stretch=tk.NO, anchor='center')

        self.tableau.heading('Mon vin', text='Mon vin')

        self.tableau.heading('Vin proposé', text='Vin proposé')

        self.tableau.heading('Demandeur', text='Demandeur')
        self.tableau.heading('Date de la demande', text='Date de la demande')

        self.tableau['show'] = 'headings'

        self.tableau.tag_configure('accept', background="green")
        self.tableau.tag_configure('refuse', background="red")
        for d in self.data:
            if (d["Reponse"] == 0):
                self.tableau.insert('', 'end', values=(
               "Pas encore répondu", d["Nom_vin_moi"], d["Nom_vin_demandeur"], d["Pseudo"], d["Date_demande"], d["id"]))
            else:
                if (d["Echange"] == 1):
                    self.check = tk.PhotoImage(file="img/checked.png")
                    self.tableau.insert(parent='', index='end', values=(
                    "accepté", d["Nom_vin_moi"], d["Nom_vin_demandeur"], d["Pseudo"], d["Date_demande"], d["id"]),tags=('accept',))
                else:
                    self.tableau.insert('', 'end', values=(
                        "refusé", d["Nom_vin_moi"], d["Nom_vin_demandeur"], d["Pseudo"], d["Date_demande"], d["id"]), tags=('refuse',))
        self.tableau.bind('<Double-1>', selectItem)




