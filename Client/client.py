import tkinter.filedialog
import tkinter as tk

import PageAjouterCave
import PageAjouterVin
import PageRecherche
import PageAccueil
import PageConnexion
import PageInscription
import MesCaves
LARGE_FONT= ("Verdana", 12)


class main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)



        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (PageAccueil.PageAccueil, PageRecherche.PageRecherche,PageAjouterVin.PageAjouterVin, PageAjouterCave.PageAjouterCave, PageInscription.PageInscription, PageConnexion.PageConnexion, MesCaves.MesCaves):
            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageConnexion.PageConnexion, "Connexion")


    def show_frame(self, cont, name=None):
        if(name == "Connexion"):
            print("ttttttttttt")
            frame = PageConnexion.PageConnexion(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew")
        elif (name == "MesCaves"):
            print("ooooooooooooooooooooooh")
            frame = MesCaves.MesCaves(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew")
        else:
            frame = self.frames[cont]

        frame.tkraise()




app = main()
app.geometry("1200x800")
app.iconbitmap("img/logo.ico")
app.resizable(width=False, height=False)
app.title("MyWine")
app.mainloop()

if __name__ == '__main__':
    main()

