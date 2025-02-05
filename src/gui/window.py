import sys

import customtkinter as tk
import tkinter as otk
from PIL import Image, ImageTk

import tooltip
from . import tools
from . import components
from . import front_algos
from . import events
from . import draws

class window(tk.CTk):
    def __init__(self, title, resolution):
        """Initialise la fenêtre principale de l'application avec un titre et une résolution spécifiés.

        :param title: Le titre de la fenêtre.
        :param resolution: La résolution de la fenêtre.
        """
        super().__init__()
        self.selected_action = None
        self.start_position = None  # Position actuelle du début (row, col)
        self.end_position = None
        tk.set_appearance_mode("Dark")
        tk.set_default_color_theme("res/themes/metal.json")
        tk.deactivate_automatic_dpi_awareness()
        self.exec = False
        self.tk.call("tk", "scaling", 1.0)

        self.title(title)
        self.geometry(resolution)
        self.resizable(False, False)

        if sys.platform.startswith("win"):  # Windows
            self.iconbitmap("res/GraphaLogo.ico")
        else:  # Linux & macOS
            icon = tk.PhotoImage(file="res/GraphaLogo.png")
            self.wm_iconphoto(True, icon)

        button_width = 300

        # Toolbar
        self.toolbox = tk.CTkFrame(self)
        self.toolbox.pack(side=tk.TOP, fill=tk.X)

        self.button1 = tk.CTkButton(self.toolbox, text="Parcours en profondeur", command=lambda : front_algos.DFS(self))
        self.button1.pack(side=tk.LEFT, padx=1, pady=2)

        self.button2 = tk.CTkButton(self.toolbox, text="Parcours en largeur", command=lambda : front_algos.BFS(self))
        self.button2.pack(side=tk.LEFT, padx=1, pady=2)

        self.button3 = tk.CTkButton(self.toolbox, text="Bellman-Ford", command=lambda : front_algos.bellman_ford(self))
        self.button3.pack(side=tk.LEFT, padx=1, pady=2)

        self.button3 = tk.CTkButton(self.toolbox, text="Dijsktra", command=lambda : front_algos.dijkstra(self))
        self.button3.pack(side=tk.LEFT, padx=1, pady=2)

        self.button3 = tk.CTkButton(self.toolbox, text="A*", command=lambda : front_algos.A_etoile(self))
        self.button3.pack(side=tk.LEFT, padx=1, pady=2)

        self.button3 = tk.CTkButton(self.toolbox, text="Kruskal", command=lambda : front_algos.Kruksal(self))
        self.button3.pack(side=tk.LEFT, padx=1, pady=2)

        self.button3 = tk.CTkButton(self.toolbox, text="Prim", command=lambda : front_algos.Prim(self))
        self.button3.pack(side=tk.LEFT, padx=1, pady=2)

        # Menu gauche
        self.menu = tk.CTkFrame(self)
        self.menu.pack(side=tk.LEFT, fill=tk.BOTH)

        # Toolbar gauche
        self.toolbar = tk.CTkFrame(self.menu)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Chargement des icônes
        self.delete_icon = tk.CTkImage(light_image=Image.open("res/delete_icon.png"),
                                  dark_image=Image.open("res/delete_icon.png"),
                                  size=(30, 30))
        self.reset_icon = tk.CTkImage(light_image=Image.open("res/reset_icon.png"),
                                  dark_image=Image.open("res/reset_icon.png"),
                                  size=(30, 30))
        self.random_icon = tk.CTkImage(light_image=Image.open("res/random_icon.png"),
                                       dark_image=Image.open("res/random_icon.png"),
                                       size=(30, 30))
        self.home_icon = tk.CTkImage(light_image=Image.open("res/home_icon.png"),
                                     dark_image=Image.open("res/home_icon.png"),
                                     size=(30, 30))
        self.water_icon = tk.CTkImage(light_image=Image.open("res/water_icon.png"),
                                      dark_image=Image.open("res/water_icon.png"),
                                      size=(30, 30))
        self.forest_icon = tk.CTkImage(light_image=Image.open("res/forest_icon.png"),
                                       dark_image=Image.open("res/forest_icon.png"),
                                       size=(30, 30))
        self.end_icon = tk.CTkImage(light_image=Image.open("res/end_icon.png"),
                                    dark_image=Image.open("res/end_icon.png"),
                                    size=(30, 30))
        self.wall_icon = tk.CTkImage(light_image=Image.open("res/wall_icon.png"),
                                     dark_image=Image.open("res/wall_icon.png"),
                                     size=(30, 30))
        self.desert_icon = tk.CTkImage(light_image=Image.open("res/desert_icon.png"),
                                       dark_image=Image.open("res/desert_icon.png"),
                                       size=(30, 30))
        self.eraser_icon = tk.CTkImage(light_image=Image.open("res/eraser_icon.png"),
                                       dark_image=Image.open("res/eraser_icon.png"),
                                       size=(30, 30))
        
        # Chargement des flèches
        self.arrow_up_white = ImageTk.PhotoImage(Image.open("res/arrows/arrow_up_white.png"))
        self.arrow_down_white = ImageTk.PhotoImage(Image.open("res/arrows/arrow_down_white.png"))
        self.arrow_upleft_white = ImageTk.PhotoImage(Image.open("res/arrows/arrow_upleft_white.png"))
        self.arrow_upright_white = ImageTk.PhotoImage(Image.open("res/arrows/arrow_upright_white.png"))
        self.arrow_botleft_white = ImageTk.PhotoImage(Image.open("res/arrows/arrow_botleft_white.png"))
        self.arrow_botright_white = ImageTk.PhotoImage(Image.open("res/arrows/arrow_botright_white.png"))

        self.arrow_up_red = ImageTk.PhotoImage(Image.open("res/arrows/arrow_up_red.png"))
        self.arrow_down_red = ImageTk.PhotoImage(Image.open("res/arrows/arrow_down_red.png"))
        self.arrow_upleft_red = ImageTk.PhotoImage(Image.open("res/arrows/arrow_upleft_red.png"))
        self.arrow_upright_red = ImageTk.PhotoImage(Image.open("res/arrows/arrow_upright_red.png"))
        self.arrow_botleft_red = ImageTk.PhotoImage(Image.open("res/arrows/arrow_botleft_red.png"))
        self.arrow_botright_red = ImageTk.PhotoImage(Image.open("res/arrows/arrow_botright_red.png"))

        # Boutons avec icônes
        components.create_action_button(self, "Ajouter Début", self.home_icon, button_width, 5)
        components.create_action_button(self, "Ajouter Fin", self.end_icon, button_width, 6)
        components.create_action_button(self, "Ajouter Mur", self.wall_icon, button_width, 1)
        components.create_action_button(self, "Ajouter eau (+5)", self.water_icon , button_width,2)
        components.create_action_button(self, "Ajouter forêt (+2)", self.forest_icon, button_width, 3)
        components.create_action_button(self, "Ajouer désert (+1)", self.desert_icon, button_width,4)
        components.create_action_button(self, "Ajouter case vide", self.eraser_icon, button_width, 0)


        # Boutons avec icônes
        self.button3 = tk.CTkButton(self.toolbar, text="", image=self.random_icon, command=lambda : tools.random_map(self))
        self.button3.pack(side=tk.RIGHT, padx=1, pady=2)
        tooltip.ToolTip(self.button3, "Génère une carte aléatoire")

        self.button2 = tk.CTkButton(self.toolbar, text="", image=self.reset_icon, command=lambda : draws.reset_path(self))
        self.button2.pack(side=tk.RIGHT, padx=1, pady=2)
        tooltip.ToolTip(self.button2, "Réinitialise les résultats")

        self.button1 = tk.CTkButton(self.toolbar, text="", image=self.delete_icon, command=lambda : draws.delete_map(self))
        self.button1.pack(side=tk.RIGHT, padx=1, pady=2)
        tooltip.ToolTip(self.button1, "Efface la carte")

        self.button = tk.CTkButton(self.menu, text="Quitter", command=self.quit)
        self.button.pack(side=tk.BOTTOM, anchor=tk.CENTER, pady=10)
        tooltip.ToolTip(self.button, "Ferme l'application")

        # Right part configuration
        self.graph = tk.CTkFrame(self)
        self.graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Ajout d'un Canvas pour dessiner la grille d'hexagone
        self.canvas = otk.Canvas(self.graph, bg="#173526", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<B1-Motion>", lambda event: events.on_mouse_drag(event, self))
        self.canvas.bind("<Button-1>", lambda event: events.on_click(event, self))

        self.grid_matrix = []
        for i in range(34):
            row = [0 if (i + j) % 2 == 0 else None for j in range(28)]
            self.grid_matrix.append(row)

        self.hex_size = 25

        # Chargement des textures avec conservation des proportions
        def load_texture(file_path, hex_size):
            """Charge une texture à partir d'un fichier et la redimensionne en fonction de la taille de l'hexagone.

            :param file_path: Le chemin du fichier de la texture.
            :param hex_size: La taille de l'hexagone.
            :return: Une image redimensionnée de la texture.
            """
            texture_size = int(hex_size * 2)-5
            with Image.open(file_path) as img:
                # Calcul du ratio
                ratio = min(texture_size / img.width, texture_size / img.height)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                # Redimensionnement avec conservation des proportions
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(resized_img)

        self.textures = {
            101: load_texture("res/textures/empty_texture1.png", self.hex_size),
            102: load_texture("res/textures/empty_texture2.png", self.hex_size),
            103: load_texture("res/textures/empty_texture3.png", self.hex_size),
            201: load_texture("res/textures/wall_texture1.png", self.hex_size),
            202: load_texture("res/textures/wall_texture2.png", self.hex_size),
            301: load_texture("res/textures/water_texture1.png", self.hex_size),
            302: load_texture("res/textures/water_texture2.png", self.hex_size),
            303: load_texture("res/textures/water_texture3.png", self.hex_size),
            401: load_texture("res/textures/forest_texture1.png", self.hex_size),
            402: load_texture("res/textures/forest_texture2.png", self.hex_size),
            403: load_texture("res/textures/forest_texture3.png", self.hex_size),
            404: load_texture("res/textures/forest_texture4.png", self.hex_size),
            501: load_texture("res/textures/desert_texture1.png", self.hex_size),
            502: load_texture("res/textures/desert_texture2.png", self.hex_size),
            503: load_texture("res/textures/desert_texture3.png", self.hex_size),
            504: load_texture("res/textures/desert_texture4.png", self.hex_size),
            6: load_texture("res/textures/start_texture.png", self.hex_size),
            7: load_texture("res/textures/end_texture.png", self.hex_size),
        }

        # Appel de la fonction pour dessiner la grille
        draws.draw_hexagonal_grid(self, self.hex_size)
