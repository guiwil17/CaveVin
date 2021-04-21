import tkinter.filedialog
import tkinter as tk

import PageAjouterCave
import PageAjouterVin
import PageRecherche
import PageAccueil
import PageConnexion
import PageInscription

LARGE_FONT= ("Verdana", 12)

class main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)


        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (PageAccueil.PageAccueil, PageRecherche.PageRecherche,PageAjouterVin.PageAjouterVin, PageAjouterCave.PageAjouterCave, PageInscription.PageInscription, PageConnexion.PageConnexion):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageConnexion.PageConnexion)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

app = main()
app.geometry("600x400")
app.iconbitmap("img/logo.ico")
app.resizable(width=False, height=False)
app.title("MyWine")
app.mainloop()

if __name__ == '__main__':
    main()

