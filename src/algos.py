from collections import deque
import random
from utils import get_voisins, dict_etat_case
import heapq

def BFS_algo(matrice : list, coordDepart : tuple, coordArrivee : tuple) :
    """Trouve le chemin le plus court entre deux cases dans une grille hexagonale en double-height.

    :param matrice: La grille hexagonale représentée comme une matrice.
    :param coordDepart: Tuple (x, y) représentant la case de départ.
    :param coordArrivee: Tuple (x, y) représentant la case cible.
    :return voisins: un dictionnaire représentant toutes les relations entre cases.
    :return chemin: Liste de tuple représentant le chemin le plus court ou "Aucun chemin" si la cible est inaccessible.
    """

    # Initialiser la file pour BFS
    file = deque([coordDepart])
    
    # Suivre les cases visitées
    visite = set()
    visite.add(coordDepart)
    
    # Stocker les prédécesseurs pour reconstruire le chemin
    predecesseur = {coordDepart: None}

    # Stocker les voisins pour l'affichage
    voisins = {}
    
    # BFS
    while file:
        courant = file.popleft()
        voisins[courant] = []
        
        # Si on atteint la cible, reconstruire le chemin
        if courant == coordArrivee:
            chemin = []
            while courant is not None:
                chemin.append(courant)
                courant = predecesseur[courant]
            return voisins, chemin[::-1]  # Inverser pour avoir l'ordre correct
        
        # Explorer les voisins
        for voisin in get_voisins(matrice, courant):
            if voisin not in visite:
                visite.add(voisin)
                voisins[courant].append(voisin)
                predecesseur[voisin] = courant
                file.append(voisin)
    
    # Si aucun chemin n'est trouvé
    return "Aucun chemin"

def DFS_algo(matrice: list, coordDepart: tuple, coordArrivee: tuple):
    """Trouve un chemin entre deux cases dans une grille hexagonale en double-height en utilisant
    la recherche en profondeur.

    :param matrice: La grille hexagonale représentée comme une matrice.
    :param coordDepart: Tuple (x, y) représentant la case de départ.
    :param coordArrivee: Tuple (x, y) représentant la case cible.
    :return voisins: un dictionnaire représentant toutes les relations entre cases.
    :return chemin: Liste de tuple représentant un chemin ou "Aucun chemin" si la cible est inaccessible.
    """
    # Initialiser la pile pour DFS
    pile = [coordDepart]
    
    # Suivre les cases visitées
    visite = set()
    visite.add(coordDepart)
    
    # Stocker les prédécesseurs pour reconstruire le chemin
    predecesseur = {coordDepart: None}
    
    # Stocker les voisins pour l'affichage
    voisins = {}

    # DFS
    while pile:
        courant = pile.pop()  # On prend l'élément le plus récent ajouté
        
        voisins[courant] = []

        # Toujours continuer d'explorer même après avoir trouvé la cible
        if courant == coordArrivee:
            # On a trouvé la cible, mais on continue l'exploration.
            # Ajout du prédécesseur à la liste du chemin.
            chemin = []
            temp = courant
            while temp is not None:
                chemin.append(temp)
                temp = predecesseur[temp]
            chemin = chemin[::-1]  # Inverser pour avoir l'ordre correct
        
        # Explorer les voisins
        voisins_courant = get_voisins(matrice, courant)
        random.shuffle(voisins_courant)  # Mélanger les voisins pour les explorer aléatoirement
        
        for voisin in voisins_courant:
            # Vérifier si le voisin n'a pas encore été visité et si c'est un voisin valide
            if voisin not in visite:
                visite.add(voisin)
                voisins[courant].append(voisin)
                predecesseur[voisin] = courant
                pile.append(voisin)

    # Si aucun chemin n'est trouvé
    # Vérification qu'il y a un chemin (même après l'exploration continue)
    if coordArrivee in predecesseur:
        chemin = []
        courant = coordArrivee
        while courant is not None:
            chemin.append(courant)
            courant = predecesseur[courant]
        chemin = chemin[::-1]  # Inverser pour avoir l'ordre correct
        return voisins, chemin

    # Si aucun chemin n'est trouvé
    return "Aucun chemin"

def parcours_dijkstra(matrice, depart, arrivee):
    """Calcule le chemin le plus court dans une matrice à l'aide de l'algorithme de
    Dijkstra et enregistre les relations entre chaque point et ses voisins explorés.

    :param matrice: Matrice 2D des coûts de déplacement.
    :param depart: Tuple (x, y) des coordonnées de départ.
    :param arrivee: Tuple (x, y) des coordonnées d'arrivée.
    :return chemin_critique: Liste des tuples représentant le chemin optimal.
    :return distances: Matrice des distances calculées.
    :return voisins_explores: Dictionnaire des voisins explorés depuis chaque point.
    """
    n_lignes, n_colonnes = len(matrice), len(matrice[0])

    # Matrice des distances initialisées à infini
    dist = [[float('inf')] * n_colonnes for _ in range(n_lignes)]
    dist[depart[0]][depart[1]] = 0  # Distance du point de départ à lui-même est 0

    # File de priorité pour Dijkstra
    a_visiter = []
    heapq.heappush(a_visiter, (0, depart))

    # Ensemble des cases déjà visitées
    deja_visite = set()

    # Dictionnaire des voisins explorés
    voisins_explores = {}

    while a_visiter:
        # Récupère la case avec la plus petite distance
        distance_courante, (i, j) = heapq.heappop(a_visiter)

        if (i, j) in deja_visite:
            continue  # Ignore les cases déjà visitées

        deja_visite.add((i, j))  # Marque la case comme visitée

        # Si on atteint l'arrivée, on peut arrêter
        if (i, j) == arrivee:
            break

        # Initialise les voisins pour cette case dans le dictionnaire
        voisins_explores[(i, j)] = []

        # Explore les voisins de la case actuelle
        voisins = get_voisins(matrice, (i, j))
        for v in voisins:
            if v in deja_visite:
                continue  #pas revisiter les cases déjà visitées

            # distance de la case actuelle à la case voisine
            cout_voisin = dict_etat_case[matrice[v[0]][v[1]]][1]
            nouvelle_distance = distance_courante + cout_voisin

            # Si une meilleure distance est trouvée, on met à jour
            if nouvelle_distance < dist[v[0]][v[1]]:
                dist[v[0]][v[1]] = nouvelle_distance
                heapq.heappush(a_visiter, (nouvelle_distance, v))
                if v not in voisins_explores[(i, j)]:
                    voisins_explores[(i, j)].append(v)
            
    chemin_critique = trouver_chemin_le_plus_court(dist, matrice, voisins_explores, depart, arrivee)
    return voisins_explores, chemin_critique, dist

def bellman_ford(matrice, depart, arrivee):
    """Trouve le chemin le plus court entre deux cases dans une grille hexagonale en double-height
    à l'aide de l'algorithme de Bellman-Ford et enregistre les relations entre chaque point et ses voisins explorés.

    :param matrice: Matrice 2D des coûts de déplacement.
    :param depart: Tuple (x, y) des coordonnées de départ.
    :param arrivee: Tuple (x, y) des coordonnées d'arrivée.
    :return voisins_explores: Dictionnaire des voisins explorés depuis chaque point.
    :return chemin_critique: Liste des tuples représentant le chemin optimal ou "Aucun chemin" si inaccessible.
    :return distances: Matrice des distances calculées.
    """
    n_lignes, n_colonnes = len(matrice), len(matrice[0])

    # Matrice des distances initialisées à infini
    dist = [[float('inf')] * n_colonnes for _ in range(n_lignes)]
    dist[depart[0]][depart[1]] = 0  # Distance du point de départ à lui-même est 0

    # Dictionnaire des prédécesseurs pour reconstruire le chemin
    pred = {}

    # Dictionnaire des voisins explorés
    voisins_explores = {}

    # Bellman-Ford : relaxation des arêtes
    for _ in range(n_lignes * n_colonnes - 1):  # Nombre maximum d'itérations
        for x in range(n_lignes):
            for y in range(n_colonnes):
                if dist[x][y] < float('inf'):
                    current = (x, y)
                    if current not in voisins_explores:
                        voisins_explores[current] = []
                    
                    for voisin in get_voisins(matrice, current):
                        cout_voisin = dict_etat_case[matrice[voisin[0]][voisin[1]]][1]
                        if dist[x][y] + cout_voisin < dist[voisin[0]][voisin[1]]:
                            dist[voisin[0]][voisin[1]] = dist[x][y] + cout_voisin
                            pred[voisin] = current
                            if voisin not in voisins_explores[current]:
                                voisins_explores[current].append(voisin)

    # Vérification des cycles de poids négatif
    for x in range(n_lignes):
        for y in range(n_colonnes):
            if dist[x][y] < float('inf'):
                current = (x, y)
                for voisin in get_voisins(matrice, current):
                    cout_voisin = dict_etat_case[matrice[voisin[0]][voisin[1]]][1]
                    if dist[x][y] + cout_voisin < dist[voisin[0]][voisin[1]]:
                        return "Cycle de poids négatif détecté", None, None

    # Reconstruction du chemin critique
    chemin_critique = []
    courant = arrivee
    while courant in pred:
        chemin_critique.append(courant)
        courant = pred[courant]
    
    if courant == depart:
        chemin_critique.append(depart)
        chemin_critique.reverse()
    else:
        chemin_critique = "Aucun chemin"

    return voisins_explores, chemin_critique, dist

def trouver_chemin_le_plus_court(dist:list, matrice:list, voisins_explores:list, origine:tuple, destination:tuple):
    """Retourne le chemin le plus court à partir de la matrice de distances.

    :param dist: Tableau 2D des distances complétées (après BFS).
    :param matrice: La grille hexagonale représentée comme une matrice.
    :param voisins_explores: Liste des voisins explorés.
    :param origine: Tuple (x, y) des coordonnées du point de départ.
    :param destination: Tuple (x, y) des coordonnées du point d'arrivée.
    :return: Une liste de tuples représentant le chemin de l'origine à la destination.
    """
    x_fin, y_fin = destination
    
    if dist[x_fin][y_fin] == float('inf'): #destination atteignable ?
        return None
    
    chemin = []
    courant = destination
    
    while courant != origine:
        chemin.append(courant)
        x, y = courant
        
        # Trouver la case adjacente avec une distance plus petite
        voisins = get_voisins(matrice, (x, y))
        distance_min = float('inf')
        for voisin in voisins:
            if dist[voisin[0]][voisin[1]] < distance_min and voisin in voisins_explores and courant in voisins_explores[voisin]:
                distance_min = dist[voisin[0]][voisin[1]]
                courant = voisin
    
    # Ajouter le point de départ
    chemin.append(origine)
    chemin.reverse()  # Inverser pour avoir le chemin de l'origine à la destination
    return chemin

def Prim_algo(matrice: list, coordDepart: tuple, coordArrivee: tuple):
    """Implémente l'algorithme de Prim pour trouver l'arbre couvrant de poids minimum et renvoyer
    un chemin entre coordDepart et coordArrivee.

    :param matrice: La matrice à partir de laquelle l'algo est effectué.
    :param coordDepart: Tuple des coordonnées de départ de l'algorithme.
    :param coordArrivee: Tuple des coordonnées d'arrivée.
    :return: Un dictionnaire des voisins de l'arbre couvrant minimal et un chemin entre coordDepart et coordArrivee.
    """
    mst = []  # Liste des arêtes de l'arbre couvrant
    visited = set()  # Ensemble des sommets visités
    min_heap = []  # Min-heap pour les arêtes (poids, sommet_source, sommet_dest)
    predecesseurs = {coordDepart: None}  # Dictionnaire pour reconstruire le chemin

    # Ajouter les arêtes du sommet de départ dans le heap
    visited.add(coordDepart)
    for voisinsDepart in get_voisins(matrice, coordDepart):
        heapq.heappush(min_heap, (dict_etat_case[matrice[voisinsDepart[0]][voisinsDepart[1]]][1], coordDepart, voisinsDepart))

    total_weight = 0  # Poids total de l'arbre couvrant

    while min_heap:
        # Récupérer l'arête avec le poids minimum
        weight, u, v = heapq.heappop(min_heap)

        # Ignorer si le sommet de destination est déjà visité
        if v in visited:
            continue

        # Ajouter l'arête au MST
        mst.append((u, v, weight))
        total_weight += weight

        # Marquer le sommet comme visité
        visited.add(v)

        # Enregistrer le prédecesseur pour pouvoir reconstruire un chemin
        predecesseurs[v] = u

        # Ajouter les nouvelles arêtes du sommet "v" au heap
        for neighbor in get_voisins(matrice, v):
            if neighbor not in visited:
                heapq.heappush(min_heap, (dict_etat_case[matrice[v[0]][v[1]]][1], v, neighbor))
    
    # Construire le dictionnaire des voisins
    dic_voisins = {}
    for x, y, w in mst:
        if x not in dic_voisins:
            dic_voisins[x] = []
        dic_voisins[x].append(y)

    # Reconstruire le chemin de coordArrivee à coordDepart
    chemin = []
    sommet = coordArrivee
    while sommet is not None:
        chemin.append(sommet)
        sommet = predecesseurs.get(sommet)

    # Inverser le chemin pour qu'il soit dans l'ordre coordDepart -> coordArrivee
    chemin.reverse()

    return dic_voisins, chemin




def double_height_to_cube(x, y):
    """Convertit les coordonnées double-height (x, y) en coordonnées cube (q, r, s).

    :param x: Coordonnée x en double-height.
    :param y: Coordonnée y en double-height.
    :return: Tuple (q, r, s) représentant les coordonnées cube.
    """
    q = x
    r = y - (x // 2) # coordonnée y ajustée pour double-height
    s = -q - r # somme des coordonnées cube = 0
    return q, r, s

def dist_manhattan(point1:tuple, point2:tuple):
    """Calcule la distance entre deux points dans une grille hexagonale en double-height.

    :param point1: Tuple (x, y) représentant le premier point.
    :param point2: Tuple (x, y) représentant le deuxième point.
    :return: La distance de Manhattan entre les deux points.
    """
    q1, r1, s1 = double_height_to_cube(point1[0], point1[1])
    q2, r2, s2 = double_height_to_cube(point2[0], point2[1])

    return max(abs(q1 - q2), abs(r1 - r2), abs(s1 - s2))

def a_etoile(matrice:list, start:tuple, goal:tuple):
    """Implémente l'algorithme A* pour trouver le chemin le plus court.

    :param matrice: La grille hexagonale (liste imbriquée représentant les types de cases).
    :param start: Point de départ (x, y).
    :param goal: Point d'arrivée (x, y).
    :return: Un tuple contenant :
        - Un dictionnaire {point: [points explorés depuis ce point]}.
        - La liste des points du chemin le plus court.
    """
    # File de priorité (coût total estimé, compteur, point)
    open_set = []
    heapq.heappush(open_set, (0, 0, start))
    compteur = 0

    # Garde les coûts et le chemin parcouru
    score = {start: 0}
    f_score = {start: dist_manhattan(start, goal)}
    case_precedente = {}
    explored = {}

    distances = [[float("inf") for _ in range(len(matrice[0]))] for _ in range(len(matrice))]
    distances[start[1]][start[0]] = 0

    while open_set:
        _, _, current = heapq.heappop(open_set)

        # Si on atteint l'objectif
        if current == goal:
            chemin = []
            while current in case_precedente:
                chemin.append(current)
                current = case_precedente[current]
            chemin.append(start)
            chemin.reverse()
            return explored, chemin, distances

        # Enregistrer les voisins explorés
        if current not in explored:
            explored[current] = []

        # Explorer les voisins
        for neighbor in get_voisins(matrice, current):
            if neighbor in explored and current in explored[neighbor]:
                continue
    
            explored[current].append(neighbor)

            # Calculer le coût pour ce voisin
            tentative_score = score[current] + dict_etat_case[matrice[neighbor[0]][neighbor[1]]][1]

            if neighbor not in score or tentative_score < score[neighbor]:
                # Met à jour les scores
                score[neighbor] = tentative_score
                f_score[neighbor] = tentative_score + dist_manhattan(neighbor, goal)
                case_precedente[neighbor] = current

                distances[neighbor[0]][neighbor[1]] = tentative_score

                # Ajouter à la file si pas déjà exploré
                if all(neighbor != item[2] for item in open_set):
                    compteur += 1
                    heapq.heappush(open_set, (f_score[neighbor], compteur, neighbor))

    # Si aucun chemin trouvé
    return explored, [], distances


def kruskal(grid:list):
    """Algorithme de Kruskal modifié, pour traiter les arêtes par groupes de poids discrets.

    :param grid: La matrice représentant la grille hexagonale (types de cases).
    :return: Dictionnaire où chaque clé est un point et chaque valeur est la liste des points connectés.
    """
    # Stocke les connexions explorées dans le MST
    explored = {}

    # Structures pour gérer les ensembles disjoints
    parent = {}  # Parent de chaque nœud
    rank = {}    # Rang de chaque ensemble

    def find(node):
        # Trouve le représentant de l'ensemble contenant `node` (avec compression de chemin)
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        # Fusionne les ensembles contenant `node1` et `node2` (en utilisant les rangs)
        root1 = find(node1)
        root2 = find(node2)

        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    # Initialiser chaque case dans les dictionnaires
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            parent[(x, y)] = (x, y)
            rank[(x, y)] = 0
            explored[(x, y)] = []  # Initialise une liste vide pour chaque nœud

    # Rassembler les arêtes par groupes de poids dans une liste
    edges_by_weight = [[] for _ in range(7)]  # Poids possibles : 0, 1, 2, 3, 4, 5, 6

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            # Ignorer les cases `None` ou invalides
            if cell is None or dict_etat_case[cell][1] == 0:  # Exclure les murs
                continue
            current = (x, y)
            for neighbor in get_voisins(grid, current):
                # Vérifie que le voisin est valide et traversable
                nx, ny = neighbor
                if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                    continue  # Hors limites
                if grid[nx][ny] is None or dict_etat_case[grid[nx][ny]][1] == 0:
                    continue  # Ignore les voisins invalides ou "murs"

                weight = dict_etat_case[grid[nx][ny]][1]
                # Ajouter l'arête dans un seul sens pour éviter les doublons
                if current < neighbor:  # Utilise l'ordre des tuples pour éviter les inversions
                    edges_by_weight[weight].append((current, neighbor, weight))

    # Traiter les groupes de poids dans l'ordre croissant
    for weight in range(len(edges_by_weight)):  # Parcours des groupes de poids
        for node1, node2, w in edges_by_weight[weight]:
            # Ajouter l'arête si elle ne crée pas de cycle
            if find(node1) != find(node2):
                union(node1, node2)
                explored[node1].append(node2)

    return explored
