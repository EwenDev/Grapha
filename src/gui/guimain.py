from . import window as gui

def guimain():
    """Initialise et lance la fenêtre principale de l'application.

    Crée une fenêtre avec le titre "Grapha" et les dimensions "1500x800", puis lance la boucle principale de l'interface graphique.
    """
    fenetre = gui.window("Grapha", "1500x800")
    fenetre.mainloop()