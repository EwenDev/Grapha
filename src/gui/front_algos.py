import algos

from . import draws
from . import tools

def BFS(gui):
    """Exécute l'algorithme de BFS pour trouver le chemin le plus court.

    :param gui: L'instance de l'interface graphique.
    """
    # Réinitialiser le chemin actuel
    draws.reset_path(gui)
    checkStartEnd(gui)
    # Exécuter l'algorithme de BFS
    path = algos.BFS_algo(gui.grid_matrix, gui.start_position, gui.end_position)

    # Dessiner le chemin
    draws.draw_path(gui, path[0], path[1], gui.hex_size)

def dijkstra(gui):
    """Exécute l'algorithme de Dijkstra pour trouver le chemin le plus court.

    :param gui: L'instance de l'interface graphique.
    """
    # Réinitialiser le chemin actuel
    draws.reset_path(gui)
    checkStartEnd(gui)

    # Exécuter l'algorithme de Dijkstra
    path = algos.parcours_dijkstra(gui.grid_matrix, gui.start_position, gui.end_position)

    # Dessiner le chemin
    draws.draw_path(gui, path[0], path[1], gui.hex_size)

    # Afficher la distance
    draws.afficher_distance(gui, path[2])

def DFS(gui):
    """Exécute l'algorithme de DFS pour trouver le chemin le plus court.

    :param gui: L'instance de l'interface graphique.
    """
    # Réinitialiser le chemin actuel
    draws.reset_path(gui)
    checkStartEnd(gui)

    # Exécuter l'algorithme de DFS
    path = algos.DFS_algo(gui.grid_matrix, gui.start_position, gui.end_position)

    # Dessiner le chemin
    draws.draw_path(gui, path[0], path[1], gui.hex_size)

def checkStartEnd(gui):
    """Vérifie si les positions de départ et de fin sont définies.
    Si ce n'est pas le cas, elles sont initialisées avec des textures appropriées.

    :param gui: L'instance de l'interface graphique.
    """
    if not gui.start_position or not gui.end_position:
        if not gui.start_position:
            gui.grid_matrix[0][0] = 5  # Début
            gui.start_position = (0, 0)
            debut_hex_id = tools.find_hex_id_by_position(gui, 0, 0)
            if debut_hex_id:
                # Mettre à jour la texture pour la position de départ
                texture = tools.get_hex_texture(gui, 5)
                update_hex_texture(gui, debut_hex_id, texture)

        if not gui.end_position:
            gui.grid_matrix[33][25] = 6  # Fin
            gui.end_position = (33, 25)
            end_hex_id = tools.find_hex_id_by_position(gui, 33, 25)
            if end_hex_id:
                # Mettre à jour la texture pour la position de fin
                texture = tools.get_hex_texture(gui, 6)
                update_hex_texture(gui, end_hex_id, texture)

def update_hex_texture(gui, hex_id, texture):
    """Met à jour la texture d'un hexagone spécifique.

    :param gui: L'instance de l'interface graphique.
    :param hex_id: L'identifiant de l'hexagone à mettre à jour.
    :param texture: La texture à appliquer à l'hexagone.
    """
    matrix_row, matrix_col = int(gui.canvas.gettags(hex_id)[0]), int(gui.canvas.gettags(hex_id)[1])
    # Supprimer l'ancienne texture si elle existe
    texture_id = None
    for item in gui.canvas.find_withtag("texture"):
        tags = gui.canvas.gettags(item)
        if tags[0] == str(matrix_row) and tags[1] == str(matrix_col):
            texture_id = item
            break

    if texture_id:
        # Mettre à jour l'image existante
        gui.canvas.itemconfig(texture_id, image=texture)
    else:
        # Ajouter une nouvelle texture si aucune n'existe
        x, y = gui.canvas.coords(hex_id)[:2]
        gui.canvas.create_image(x, y, image=texture, tags=(str(matrix_row), str(matrix_col), "texture"))

def Prim(gui):
    """Exécute l'algorithme de Prim pour trouver le chemin le plus court.

    :param gui: L'instance de l'interface graphique.
    """
    draws.reset_path(gui)
    #Clear le chemin actuel
    checkStartEnd(gui)
    
    # Exécuter l'algorithme de DFS
    path = algos.Prim_algo(gui.grid_matrix, gui.start_position, gui.end_position)

    # Dessiner le chemin
    draws.draw_path(gui, path[0], path[1], gui.hex_size)

def A_etoile(gui):
    """Exécute l'algorithme de A* pour trouver le chemin le plus court.

    :param gui: L'instance de l'interface graphique.
    """
    draws.reset_path(gui)
    draws.effacer_distances(gui)
    #Clear le chemin actuel
    checkStartEnd(gui)
    
    # Exécuter l'algorithme de A*
    path = algos.a_etoile(gui.grid_matrix, gui.start_position, gui.end_position)

    # Dessiner le chemin
    draws.draw_path(gui, path[0], path[1], gui.hex_size)

    # Afficher la distance
    draws.afficher_distance(gui, path[2])

def bellman_ford(gui):
    """Exécute l'algorithme de Bellman-Ford pour trouver le chemin le plus court.

    :param gui: L'instance de l'interface graphique.
    """
    #Clear le chemin actuel
    draws.reset_path(gui)
    draws.effacer_distances(gui)
    checkStartEnd(gui)

    # Exécuter l'algorithme de Bellman-Ford
    path = algos.bellman_ford(gui.grid_matrix, gui.start_position, gui.end_position)

    # Dessiner le chemin
    draws.draw_path(gui, path[0], path[1], gui.hex_size)

    # Afficher la distance
    draws.afficher_distance(gui, path[2])


def Kruksal(gui):
    """Exécute l'algorithme de Kruksal pour trouver le chemin le plus court.

    :param gui: L'instance de l'interface graphique.
    """
    #Clear le chemin actuel
    draws.reset_path(gui)
    checkStartEnd(gui)
    
    # Exécuter l'algorithme de Kruksal
    path = algos.kruskal(gui.grid_matrix)

    # Dessiner le chemin
    draws.draw_path(gui, path, [], gui.hex_size)
