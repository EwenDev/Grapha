import customtkinter as tk
from . import events

def create_action_button(gui, text, image, button_width, value):
    """Crée un bouton pour définir une action.

    :param gui: L'instance de l'interface graphique.
    :param text: Le texte à afficher sur le bouton.
    :param image: L'image à afficher sur le bouton.
    :param button_width: La largeur du bouton.
    :param value: La valeur associée à l'action du bouton.
    """
    button = tk.CTkButton(
        gui.menu,
        text=text,
        image=image,
        compound=tk.LEFT,
        width=button_width,
        command=lambda: events.on_action_button_click(gui, value)
    )
    button.pack(side=tk.TOP, anchor=tk.CENTER, pady=10)
