import random
from . import window
from . import draws
from . import tools

def find_hex_id_by_position(gui, row, col):
    """Trouver l'ID d'un hexagone à partir de sa position dans la matrice.

    :param gui: L'instance de l'interface graphique.
    :param row: La ligne de la matrice.
    :param col: La colonne de la matrice.
    :return: L'ID de l'hexagone ou None s'il n'est pas trouvé.
    """
    for i in gui.canvas.find_all():
        tags = gui.canvas.gettags(i)
        if tags and len(tags) > 0 and tags[0] == str(row) and tags[1] == str(col):
            return i
    return None

def get_hex_color(value):
    """Obtenir la couleur d'un hexagone en fonction de sa valeur.

    :param value: La valeur de l'hexagone.
    :return: La couleur correspondante.
    """
    colors = {
        0: "white",  # Vide
        1: "black",  # Mur
        2: "#5084c1",   # Eau
        3: "#78a75a",  # Forêt
        4: "#eac452", # Désert
        5: "#ea3323",    # Départ
        6: "#ea33f7"  # Fin
    }
    return colors.get(value, "white")  # Valeur par défaut 'white'

def random_map(gui):
    """Générer une carte aléatoire en attribuant des valeurs aléatoires aux hexagones.

    :param gui: L'instance de l'interface graphique.
    """
    draws.reset_path(gui)  # Réinitialise les flèches et chemins tracés

    # Parcourir la matrice pour attribuer des valeurs aléatoires
    for row in range(len(gui.grid_matrix)):
        for col in range(len(gui.grid_matrix[row])):
            # Ignorer les cellules correspondant au départ (5) et à la fin (6)
            if gui.grid_matrix[row][col] not in [5, 6]:
                if gui.grid_matrix[row][col] is not None:
                    # Générer une valeur aléatoire entre 0 et 4 (inclus)
                    random_value = random.randint(0, 4)
                    gui.grid_matrix[row][col] = random_value

                    # Rechercher l'ID de l'hexagone correspondant
                    hex_id = None
                    for item in gui.canvas.find_withtag("hex"):
                        tags = gui.canvas.gettags(item)
                        if tags and len(tags) > 0 and tags[0] == str(row) and tags[1] == str(col):
                            hex_id = item
                            break

                    # Mettre à jour la texture ou la couleur de l'hexagone
                    if hex_id:
                        texture = tools.get_hex_texture(gui, random_value)  # Récupérer la texture aléatoire
                        texture_id = None

                        # Vérifier si une texture existe déjà
                        for item in gui.canvas.find_withtag("texture"):
                            tags = gui.canvas.gettags(item)
                            if tags[0] == str(row) and tags[1] == str(col):
                                texture_id = item
                                break

                        if texture_id:
                            # Mettre à jour la texture existante
                            gui.canvas.itemconfig(texture_id, image=texture)
                        else:
                            # Ajouter une nouvelle texture
                            x, y = gui.canvas.coords(hex_id)[:2]
                            gui.canvas.create_image(x, y, image=texture, tags=(str(row), str(col), "texture"))

def update_cursor(gui):
    """Met à jour le curseur en fonction de l'action sélectionnée.

    :param gui: L'instance de l'interface graphique.
    """
    if gui.selected_action == 5:  # Début
        gui.config(cursor="@res/cursors/home_icon.cur")
    elif gui.selected_action == 6:  # Fin
        gui.config(cursor="@res/cursors/end_icon.cur")
    elif gui.selected_action == 1:  # Mur
        gui.config(cursor="@res/cursors/wall_icon.cur")
    elif gui.selected_action == 2:  # Eau
        gui.config(cursor="@res/cursors/water_icon.cur")
    elif gui.selected_action == 3:  # Forêt
        gui.config(cursor="@res/cursors/forest_icon.cur")
    elif gui.selected_action == 4:  # Désert
        gui.config(cursor="@res/cursors/desert_icon.cur")
    elif gui.selected_action == 0:  # Vide
        gui.config(cursor="@res/cursors/eraser_icon.cur")
    else:
        gui.config(cursor="arrow")


def get_hex_texture(gui, hex_type):
    """Obtenir la texture d'un hexagone en fonction de son type.

    :param gui: L'instance de l'interface graphique.
    :param hex_type: Le type de l'hexagone.
    :return: La texture correspondante.
    """
    hex_type += 1

    texture_variants = {
        1: [101, 102, 103],  # Empty textures
        2: [201, 201, 201, 202],  # Wall textures
        3: [301, 302, 301, 302, 301, 302, 301, 302, 301, 302, 301, 302, 303],  # Water textures
        4: [401, 402, 403, 401, 402, 403, 401, 402, 403, 401, 402, 403, 401, 402, 403, 404],  # Forest textures
        5: [501, 502, 501, 502, 501, 502, 501, 502, 501, 502, 503, 501, 502, 501, 502, 501, 502, 501, 502, 501, 502, 501, 502, 503, 501, 502, 504],  # Desert textures
    }

    # Si hex_type a plusieurs variantes, choisir aléatoirement
    if hex_type in texture_variants:
        return gui.textures[random.choice(texture_variants[hex_type])]
    else:
        return gui.textures[hex_type]  # Si pas de variantes, retourner directement le type