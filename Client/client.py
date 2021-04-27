import tkinter.filedialog
import tkinter as tk

import PageAjouterCave
import PageAjouterVin
import PageRecherche
import PageAccueil
import PageConnexion
import PageInscription
import MesCaves
import VisiterCaves
import DemanderEchange
import ModifierVin
import PageMesDemandes
import PageMesDemandesEnvoyes
import PageAdmin
import VisiterCavesAdmin

LARGE_FONT= ("Verdana", 12)


class main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)



        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}


        self.show_frame("PageConnexion")


    def show_frame(self, name=None, param=None):
        if(name == "PageConnexion"):
            frame = PageConnexion.PageConnexion(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew")
        elif (name == "MesCaves"):
            frame = MesCaves.MesCaves(self.container, self, param[0])
            frame.grid(row=0, column=0, sticky="nsew")
        elif(name == "PageAccueil" and param == None):
            frame = PageAccueil.PageAccueil(self.container, self, param[0])
            frame.grid(row=0, column=0, sticky="nsew")
        elif (name == "PageRecherche"):
            frame = PageRecherche.PageRecherche(self.container, self, param[0])
            frame.grid(row=0, column=0, sticky="nsew")
        elif (name == "PageAjouterVin"):
            frame = PageAjouterVin.PageAjouterVin(self.container, self, param[0])
            frame.grid(row=0, column=0, sticky="nsew")
        elif (name == "PageAjouterCave"):
            frame = PageAjouterCave.PageAjouterCave(self.container, self, param[0])
            frame.grid(row=0, column=0, sticky="nsew")
        elif (name == "PageInscription"):
            frame = PageInscription.PageInscription(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew")
        elif (name == "VisiterCaves"):
            frame = VisiterCaves.VisiterCaves(self.container, self, param[0], param[1])
            frame.grid(row=0, column=0, sticky="nsew")
        elif(name == "DemanderEchange"):
            frame = DemanderEchange.DemanderEchange(self.container, self, param[0], param[1], param[2])
            frame.grid(row=0, column=0, sticky="nsew")
        elif (name == "ModifierVin"):
            frame = ModifierVin.ModifierVin(self.container, self, param[0], param[1])
            frame.grid(row=0, column=0, sticky="nsew")
        elif(name ==  "PageMesDemandes"):
            frame = PageMesDemandes.PageMesDemandes(self.container, self, param[0])
            frame.grid(row=0, column=0, sticky="nsew")
        elif(name == "PageMesDemandesEnvoyes"):
            frame = PageMesDemandesEnvoyes.PageMesDemandesEnvoyes(self.container, self, param[0])
            frame.grid(row=0, column=0, sticky="nsew")
        elif (name == "PageAccueil" and param[0]==1):
            frame = PageAdmin.PageAdmin(self.container, self, param[0])
            frame.grid(row=0, column=0, sticky="nsew")
        elif (name == "VisiterCavesAdmin"):
            frame = VisiterCavesAdmin.VisiterCavesAdmin(self.container, self, param[0], param[1])
            frame.grid(row=0, column=0, sticky="nsew")


        frame.tkraise()




app = main()
app.geometry("1200x800")
app.iconbitmap("img/logo.ico")
app.resizable(width=False, height=False)
app.title("MyWine")
app.mainloop()

if __name__ == '__main__':
    main()

