import tkinter as tk

class ToolTip:
    def __init__(self, widget, text):
        """Initialise l'info-bulle pour un widget spécifique avec le texte donné.

        :param widget: Le widget auquel l'info-bulle est associée.
        :param text: Le texte à afficher dans l'info-bulle.
        """
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.id = None  # Identifiant du délai
        self.widget.bind("<Enter>", self.schedule_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def schedule_tooltip(self, event=None):
        """Planifie l'affichage de l'info-bulle après un délai spécifié.

        :param event: L'événement déclencheur (facultatif).
        """
        # Planifie l'affichage du tooltip après 1 seconde
        self.id = self.widget.after(250, self.show_tooltip)

    def show_tooltip(self, event=None):
        """Affiche l'info-bulle à côté du widget associé.

        :param event: L'événement déclencheur (facultatif).
        """
        # Affiche l'info-bulle
        if self.tooltip is not None:  # Ne pas recréer si déjà affiché
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)  # Supprime la bordure de la fenêtre
        self.tooltip.geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="white", fg="black", relief="solid", borderwidth=1)
        label.pack(ipadx=5, ipady=2)

    def hide_tooltip(self, event=None):
        """Cache l'info-bulle et annule l'affichage planifié si nécessaire.

        :param event: L'événement déclencheur (facultatif).
        """
        # Cache l'info-bulle
        if self.id:
            self.widget.after_cancel(self.id)  # Annule l'affichage planifié
            self.id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
