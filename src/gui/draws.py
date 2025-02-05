import math
import customtkinter as tk
from PIL import Image

from . import tools

def reset_path(gui):
    """Réinitialise les flèches du chemin.

    :param gui: L'instance de l'interface graphique.
    """
    effacer_distances(gui)
    gui.stop_drawing = True  # Activer le drapeau d'arrêt
    gui.canvas.delete("path")
    gui.stop_drawing = True
    effacer_distances(gui)

def update_hex_color(gui, hex_id):
    """Changer la couleur d'un hexagone en fonction de l'action sélectionnée.

    :param gui: L'instance de l'interface graphique.
    :param hex_id: L'identifiant de l'hexagone à mettre à jour.
    """
    if not hasattr(gui, 'selected_action') or gui.selected_action is None:
        return
    matrix_row, matrix_col = int(gui.canvas.gettags(hex_id)[0]), int(gui.canvas.gettags(hex_id)[1])

    # Si la case cliquée est actuellement le point de départ ou d'arrivée, et qu'on change son action :
    if gui.start_position == (matrix_row, matrix_col) and gui.selected_action != 5:
        # Réinitialiser start_position si elle est remplacée par une autre action
        gui.start_position = None

    if gui.end_position == (matrix_row, matrix_col) and gui.selected_action != 6:
        # Réinitialiser end_position si elle est remplacée par une autre action
        gui.end_position = None

    # Gérer le début (5) ou la fin (6)
    if gui.selected_action == 5:  # Début
        # Si un début existe déjà, le réinitialiser
        if gui.start_position:
            old_row, old_col = gui.start_position
            gui.grid_matrix[old_row][old_col] = 0  # Réinitialiser la matrice
            old_hex_id = tools.find_hex_id_by_position(gui, old_row, old_col)
            if old_hex_id:
                gui.canvas.itemconfig(old_hex_id, fill=tools.get_hex_color(0))  # Réinitialiser la couleur

        # Mettre à jour la position actuelle du début
        gui.start_position = (matrix_row, matrix_col)

    elif gui.selected_action == 6:  # Fin
        # Si une fin existe déjà, la réinitialiser
        if gui.end_position:
            old_row, old_col = gui.end_position
            gui.grid_matrix[old_row][old_col] = 0  # Réinitialiser la matrice
            old_hex_id = tools.find_hex_id_by_position(gui, old_row, old_col)
            if old_hex_id:
                gui.canvas.itemconfig(old_hex_id, fill=tools.get_hex_color(0))  # Réinitialiser la couleur

        # Mettre à jour la position actuelle de la fin
        gui.end_position = (matrix_row, matrix_col)

    # Mise à jour de la matrice et de la couleur de l'hexagone sélectionné
    gui.grid_matrix[matrix_row][matrix_col] = gui.selected_action
    gui.canvas.itemconfig(hex_id, fill=tools.get_hex_color(gui.selected_action))

def update_hex_texture(gui, hex_id):
    """Changer la texture d'un hexagone en fonction de l'action sélectionnée.

    :param gui: L'instance de l'interface graphique.
    :param hex_id: L'identifiant de l'hexagone à mettre à jour.
    """
    if not hasattr(gui, 'selected_action') or gui.selected_action is None:
        return

    matrix_row, matrix_col = int(gui.canvas.gettags(hex_id)[0]), int(gui.canvas.gettags(hex_id)[1])

    # Si la case cliquée est actuellement le point de départ ou d'arrivée, et qu'on change son action :
    if gui.start_position == (matrix_row, matrix_col) and gui.selected_action != 5:
        # Réinitialiser start_position si elle est remplacée par une autre action
        gui.start_position = None

    if gui.end_position == (matrix_row, matrix_col) and gui.selected_action != 6:
        # Réinitialiser end_position si elle est remplacée par une autre action
        gui.end_position = None

    # Gérer le début (5) ou la fin (6)
    if gui.selected_action == 5:  # Début
        # Si un début existe déjà, le réinitialiser
        if gui.start_position:
            old_row, old_col = gui.start_position
            gui.grid_matrix[old_row][old_col] = 0  # Réinitialiser la matrice
            old_hex_id = tools.find_hex_id_by_position(gui, old_row, old_col)
            if old_hex_id:
                reset_texture(gui, old_hex_id)  # Réinitialiser la texture

        # Mettre à jour la position actuelle du début
        gui.start_position = (matrix_row, matrix_col)

    elif gui.selected_action == 6:  # Fin
        # Si une fin existe déjà, la réinitialiser
        if gui.end_position:
            old_row, old_col = gui.end_position
            gui.grid_matrix[old_row][old_col] = 0  # Réinitialiser la matrice
            old_hex_id = tools.find_hex_id_by_position(gui, old_row, old_col)
            if old_hex_id:
                reset_texture(gui, old_hex_id)  # Réinitialiser la texture

        # Mettre à jour la position actuelle de la fin
        gui.end_position = (matrix_row, matrix_col)

    # Mise à jour de la matrice
    gui.grid_matrix[matrix_row][matrix_col] = gui.selected_action

    # Identifier l'image associée à cet hexagone
    texture = tools.get_hex_texture(gui, gui.selected_action)

    # Mettre à jour l'image de la texture en recherchant le tag
    texture_id = None
    for item in gui.canvas.find_withtag("texture"):
        tags = gui.canvas.gettags(item)
        if tags[0] == str(matrix_row) and tags[1] == str(matrix_col):
            texture_id = item
            break

    if texture_id:
        gui.canvas.itemconfig(texture_id, image=texture)
    else:
        # Ajouter la nouvelle texture si elle n'existe pas encore
        x, y = gui.canvas.coords(hex_id)[:2]
        gui.canvas.create_image(x, y, image=texture, tags=(str(matrix_row), str(matrix_col), "texture"))

def reset_texture(gui, hex_id):
    """Réinitialise la texture d'un hexagone à l'état vide.

    :param gui: L'instance de l'interface graphique.
    :param hex_id: L'identifiant de l'hexagone à réinitialiser.
    """
    matrix_row, matrix_col = int(gui.canvas.gettags(hex_id)[0]), int(gui.canvas.gettags(hex_id)[1])
    gui.grid_matrix[matrix_row][matrix_col] = 0
    texture = tools.get_hex_texture(gui, 0)  # Texture par défaut
    texture_id = None

    for item in gui.canvas.find_withtag("texture"):
        tags = gui.canvas.gettags(item)
        if tags[0] == str(matrix_row) and tags[1] == str(matrix_col):
            texture_id = item
            break

    if texture_id:
        gui.canvas.itemconfig(texture_id, image=texture)


def draw_hexagonal_grid(gui, hex_size):
    """Dessine une grille hexagonale.

    :param gui: L'instance de l'interface graphique.
    :param hex_size: La taille d'un hexagone.
    """
    dx = hex_size * 3 / 2
    dy = math.sqrt(3) * hex_size

    for row, row_data in enumerate(gui.grid_matrix):
        for col, cell in enumerate(row_data):
            if row % 2 == col % 2:
                x = col * dx + 27
                y = row * (dy / 2) + 23
                draw_hexagon(gui, x, y, row, col, hex_size)


def draw_hexagon(gui, x, y, matrix_row, matrix_col, size):
    """Dessine un hexagone à une position spécifique.

    :param gui: L'instance de l'interface graphique.
    :param x: La coordonnée x du centre de l'hexagone.
    :param y: La coordonnée y du centre de l'hexagone.
    :param matrix_row: La ligne de la matrice de l'hexagone.
    :param matrix_col: La colonne de la matrice de l'hexagone.
    :param size: La taille de l'hexagone.
    """
    # Identifier la texture correspondant à la valeur de la matrice
    texture = tools.get_hex_texture(gui,gui.grid_matrix[matrix_row][matrix_col])
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        px = x + size * math.cos(angle)
        py = y + size * math.sin(angle)
        points.extend((px, py))

    # Créer l'hexagone pour les interactions (invisible mais cliquable)
    hex_id = gui.canvas.create_polygon(
        points, outline="", fill="", width=1, tags=(matrix_row, matrix_col, "hex")
    )
    # Ajouter l'image de texture au centre de l'hexagone
    img_id = gui.canvas.create_image(x, y, image=texture, tags=(matrix_row, matrix_col, "texture"))
    return hex_id, img_id

def delete_map(gui):
    """Supprime tous les éléments de la carte.

    :param gui: L'instance de l'interface graphique.
    """
    reset_path(gui)
    gui.stop_drawing = True
    effacer_distances(gui)

    for row in range(len(gui.grid_matrix)):
        for col in range(len(gui.grid_matrix[row])):
            if gui.grid_matrix[row][col] not in [5, 6] and gui.grid_matrix[row][col] is not None:  # Ignorer le début et la fin
                gui.grid_matrix[row][col] = 0  # Réinitialiser la cellule

    # Réinitialiser les textures et couleurs des hexagones
    for hex_id in gui.canvas.find_withtag("hex"):
        matrix_row, matrix_col = int(gui.canvas.gettags(hex_id)[0]), int(gui.canvas.gettags(hex_id)[1])

        # Si c'est un hexagone de début ou de fin, ne pas le modifier
        if gui.grid_matrix[matrix_row][matrix_col] in [5, 6]:
            continue

        # Réinitialiser la texture à l'état par défaut (vide)
        texture = tools.get_hex_texture(gui, 0)  # Obtenir la texture par défaut
        texture_id = None

        # Trouver l'image de texture associée à cet hexagone
        for item in gui.canvas.find_withtag("texture"):
            tags = gui.canvas.gettags(item)
            if tags[0] == str(matrix_row) and tags[1] == str(matrix_col):
                texture_id = item
                break

        if texture_id:
            # Mettre à jour la texture à vide
            gui.canvas.itemconfig(texture_id, image=texture)
        else:
            # Si aucune texture n'existe, mettre à jour la couleur par défaut
            gui.canvas.itemconfig(hex_id, fill=tools.get_hex_color(0))

def draw_arrow(gui, x, y, color, hex_size, shorten_factor=0.9, start_offset=0.1):
    """Dessine une flèche entre deux points, avec des ajustements pour ne pas commencer au centre.

    :param gui: L'instance de l'interface graphique.
    :param x: Coordonnées de départ (ligne, colonne).
    :param y: Coordonnées d'arrivée (ligne, colonne).
    :param color: Couleur de la flèche.
    :param hex_size: Taille d'un hexagone.
    :param shorten_factor: Facteur pour raccourcir la longueur de la flèche (entre 0 et 1).
    :param start_offset: Facteur pour décaler le début de la flèche (entre 0 et 1).
    """
    # Calculs pour la position des points de départ et d'arrivée
    dx = hex_size * 3 / 2
    dy = math.sqrt(3) * hex_size

    row1, col1 = x
    row2, col2 = y
            
    start_x = col1 * dx + 27
    start_y = row1 * (dy / 2) + 23
    end_x = col2 * dx + 27
    end_y = row2 * (dy / 2) + 23   
    
    # Calculer les nouveaux points de départ et d'arrivée
    adjusted_start_x = start_x + (end_x - start_x) * start_offset
    adjusted_start_y = start_y + (end_y - start_y) * start_offset
    adjusted_end_x = start_x + (end_x - start_x) * shorten_factor
    adjusted_end_y = start_y + (end_y - start_y) * shorten_factor
    
    # Déterminer la direction de la flèche
    if adjusted_end_y < adjusted_start_y:
        if adjusted_end_x < adjusted_start_x:
            arrow_texture = gui.arrow_upleft_red if color == "red" else gui.arrow_upleft_white
        elif adjusted_end_x > adjusted_start_x:
            arrow_texture = gui.arrow_upright_red if color == "red" else gui.arrow_upright_white
        else:
            arrow_texture = gui.arrow_up_red if color == "red" else gui.arrow_up_white
    elif adjusted_end_y > adjusted_start_y:
        if adjusted_end_x < adjusted_start_x:
            arrow_texture = gui.arrow_botleft_red if color == "red" else gui.arrow_botleft_white
        elif adjusted_end_x > adjusted_start_x:
            arrow_texture = gui.arrow_botright_red if color == "red" else gui.arrow_botright_white
        else:
            arrow_texture = gui.arrow_down_red if color == "red" else gui.arrow_down_white
    else:
        if adjusted_end_x > adjusted_start_x:
            arrow_texture = gui.arrow_upright_red if color == "red" else gui.arrow_upright_white
        else:
            arrow_texture = gui.arrow_downright_red if color == "red" else gui.arrow_downright_white

    # Dessiner la flèche
    gui.canvas.create_image(
        (adjusted_start_x + adjusted_end_x) / 2, (adjusted_start_y + adjusted_end_y) / 2,
        image=arrow_texture, tags="path"
    )
    # Conserver une référence à l'image pour éviter qu'elle ne soit garbage collected
    if not hasattr(gui, 'arrow_images'):
        gui.arrow_images = []
    gui.arrow_images.append(arrow_texture)

def draw_path(gui, dicChemins, plusCourtChemin, hex_size, intervalle=100, batch_size=10):
    """Dessine les flèches grises par lots, puis les flèches rouges une par une, de manière progressive.

    :param gui: L'instance de l'interface graphique.
    :param dicChemins: Dictionnaire des chemins et voisins.
    :param plusCourtChemin: Liste représentant le chemin optimal.
    :param hex_size: Taille d'un hexagone.
    :param intervalle: Délai en millisecondes entre chaque apparition.
    :param batch_size: Nombre de flèches grises dessinées simultanément.
    """
    if gui.exec:
        return
    gui.exec = True
    gui.stop_drawing = False  # Initialiser le drapeau d'arrêt

    # Séparer les flèches grises et rouges
    gray_arrows = [(i, j) for i in dicChemins for j in dicChemins[i]]
    red_arrows = []

    
    if plusCourtChemin == None:
        gui.exec = False
        return


    if len(plusCourtChemin) >= 2:
        for i in range(len(plusCourtChemin) - 1):
            red_arrows.append((plusCourtChemin[i], plusCourtChemin[i + 1]))

    def dessiner_fleches_grises(index=0):
        """Dessine les flèches grises au fur et à mesure.
        :param index: Index de départ pour dessiner les flèches grises.
        """
        if gui.stop_drawing:
            gui.exec = False
            return
        if index < len(gray_arrows):
            batch = gray_arrows[index:index + batch_size]
            for x, y in batch:
                draw_arrow(gui, x, y, "gray", hex_size)
            gui.canvas.after(intervalle, dessiner_fleches_grises, index + batch_size)
        else:
            dessiner_fleches_rouges()

    def dessiner_fleches_rouges(index=0):
        """Dessine les flèches rouges une par une.
        :param index: Index de départ pour dessiner les flèches rouges.
        """
        if gui.stop_drawing:
            gui.exec = False
            return
        if index < len(red_arrows):
            x, y = red_arrows[index]
            draw_arrow(gui, x, y, "red", hex_size)
            gui.canvas.after(intervalle, dessiner_fleches_rouges, index + 1)
        else:
            gui.exec = False

    try:
        if gray_arrows:
            dessiner_fleches_grises()
        elif red_arrows:
            dessiner_fleches_rouges()
        else:
            print("Aucune flèche à dessiner.")
            gui.exec = False
    except:
        gui.exec = False




def afficher_distance(gui, matricedistance):
    """Affiche les distances calculées sur les hexagones.

    :param gui: L'instance de l'interface graphique.
    :param matricedistance: Matrice des distances calculées.
    """
    for i, row in enumerate(matricedistance):
        for j, distance in enumerate(row):
            if distance != float('inf'):
                hex_id = tools.find_hex_id_by_position(gui, i, j)
                gui.canvas.create_text(
                gui.canvas.coords(hex_id)[0] - 25, gui.canvas.coords(hex_id)[1],
                text=str(int(distance)), fill="black", font=("Arial", 15), tags="text"
                )
    
    gui.canvas.tag_raise("text")  # Mettre le texte au premier plan 
        
def effacer_distances(gui):
    """Efface les distances affichées sur les hexagones.

    :param gui: L'instance de l'interface graphique.
    """
    for text_id in gui.canvas.find_withtag("text"):
        gui.canvas.delete(text_id)