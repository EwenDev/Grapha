from . import draws
from . import tools

def on_mouse_drag(event, gui):
    """Gérer le déplacement de la souris pour dessiner les hexagones.

    :param event: L'événement de déplacement de la souris.
    :param gui: L'instance de l'interface graphique.
    """
    hex_id = gui.canvas.find_closest(event.x, event.y)[0]
    if hex_id:
        draws.update_hex_texture(gui, hex_id)

def on_action_button_click(gui, action_value):
    """Définir l'action sélectionnée.

    :param gui: L'instance de l'interface graphique.
    :param action_value: La valeur de l'action sélectionnée.
    """
    gui.selected_action = action_value
    tools.update_cursor(gui)

def on_drag(event, gui):
    """Gérer le déplacement de la souris pour dessiner les hexagones.

    :param event: L'événement de déplacement de la souris.
    :param gui: L'instance de l'interface graphique.
    """
    hex_id = gui.canvas.find_closest(event.x, event.y)[0]
    if hex_id:
        draws.update_hex_texture(gui, hex_id)

def on_click(event, gui):
    """Gérer le clic.

    :param event: L'événement de clic de la souris.
    :param gui: L'instance de l'interface graphique.
    """
    hex_id = gui.canvas.find_closest(event.x, event.y)[0]
    draws.reset_path(gui)
    draws.update_hex_texture(gui, hex_id)

def stop_draw(gui):
    """Arrêter le dessin si l'exécution est en cours.

    :param gui: L'instance de l'interface graphique.
    """
    if gui.exec == False:
        return True
