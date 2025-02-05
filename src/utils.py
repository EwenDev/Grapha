# Dictionnaire de définition des état de la matrice
# id = [couleur, temps de trajet]
# Ne pas modifier les éléments 0, 1 et 2
# Le reste peut être modifié librement, et de nouveaux peuvent être ajoutés

dict_etat_case = {
    0 : ["blanc", 1],
    1 : ["black", 0], 
    2 : ["eau", 6],  
    3 : ["forêt", 3], 
    4 : ["désert", 2],
    5 : ["départ", 1],
    6 : ["arrivée", 1] 
}

# VERIF: RANGE X, RANGE y, NON 0
def get_voisins(matrice: list, coords: tuple):
    """
    Récupère les voisins existants dans la grille hexagonale.

    :param matrice: Matrice 2D représentant la grille.
    :param coords: Tuple (x, y) des coordonnées de l'hexagone cible.
    :return: Une liste de tuples représentant les coordonnées des voisins existants.
    """

    # Définition des variables nécessaires au calcul
    index_col_max = len(matrice[0]) - 1  # Max index for columns
    index_ligne_max = len(matrice) - 1  # Max index for rows

    if coords[0] > index_ligne_max or coords[0] < 0 or coords[1] < 0 or coords[1] > index_col_max:
        raise ValueError(f"Les coordonnées de la case {coords} ne sont pas correctes (hors limites de la grille)")

    # Définir les directions en fonction de la parité de y
    directions = [(-1, -1), (-2, 0), (-1, 1), (1, 1), (2, 0), (1, -1)]
    
    # Calculer les voisins tout en restant dans les limites
    voisins = []
    for dx, dy in directions:
        voisin_x, voisin_y = coords[0] + dx, coords[1] + dy
        # Vérification correcte des limites pour chaque coordonnée
        if 0 <= voisin_x <= index_ligne_max and 0 <= voisin_y <= index_col_max:
            # Vérifie si la case voisine n'est pas bloquée
            case_etat = dict_etat_case.get(matrice[voisin_x][voisin_y], [None, None])[1]
            if case_etat != 0:  # Assurez-vous que la case est accessible
                voisins.append((voisin_x, voisin_y))
    
    return voisins




def create_matrice_vide (nb_lignes : int, nb_colonnes : int) :
    """
    Crée une matrice avec un motif alterné (0 et None) en fonction du nombre de lignes et de colonnes.

    :param nb_lignes: Nombre de lignes de la matrice.
    :param nb_colonnes: Nombre de colonnes de la matrice.
    :return: Matrice générée.
    """
    if nb_lignes <= 0 or nb_colonnes <= 0 :
        raise ValueError("Les données entrées sont inférieures ou égales à 0")
    return [[0 if (i + j) % 2 == 0 else None for j in range(nb_colonnes)] for i in range(nb_lignes)]

def change_hex_state (matrice : list, x : int, y : int, new_state : int) :
    """
    Change l'état d'un hexagone cible.

    :param matrice: Matrice 2D représentant la grille.
    :param x: Coordonnée x de l'hexagone cible.
    :param y: Coordonnée y de l'hexagone cible.
    :param new_state: Nouvel état de l'hexagone cible.
    """

    if not(0 <= x < len(matrice) and 0 <= y < len(matrice[0])) :
        raise ValueError("Les coordonnées de la case ne sont pas correctes")
    
    if(new_state not in dict_etat_case) :
        raise ValueError("Le nouvel état de la case n'existe pas")
    
    matrice[x][y] = new_state