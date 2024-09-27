import pygame as pg

class EventManager:
    def __init__(self):
        self.events = {}  # Dictionnaire pour stocker les événements et leurs callbacks

    def register_event(self, event_type):
        """Enregistre un nouveau type d'événement."""
        if event_type not in self.events:
            self.events[event_type] = []

    def register_callback(self, event_type, callback):
        """Enregistre un callback pour un événement spécifique."""
        if event_type in self.events:
            self.events[event_type].append(callback)

    def trigger_event(self, event_type, *args, **kwargs):
        """Déclenche l'événement et exécute tous les callbacks associés."""
        if event_type in self.events:
            for callback in self.events[event_type]:
                callback(*args, **kwargs)  # Appelle le callback


class EventHandler:
    def __init__(self, window, backgrounds, arrow_left, arrow_right, event_manager):
        self.window = window
        self.backgrounds = backgrounds
        self.current_background_index = 0

        # Rectangles des flèches (position et taille)
        self.arrow_left_rect = pg.Rect(20, (self.window.get_height() // 2) - 50, 50, 100)
        self.arrow_right_rect = pg.Rect(self.window.get_width() - 70, (self.window.get_height() // 2) - 50, 50, 100)

        # Redimensionner les images des flèches pour correspondre aux rectangles
        self.arrow_left = pg.transform.scale(arrow_left, (self.arrow_left_rect.width, self.arrow_left_rect.height))
        self.arrow_right = pg.transform.scale(arrow_right, (self.arrow_right_rect.width, self.arrow_right_rect.height))

        # Gestionnaire d'événements
        self.event_manager = event_manager

    @staticmethod
    def on_arrow_left_click(event_handler):
        """Callback statique pour changer le fond vers la gauche."""
        event_handler.change_background(-1)

    @staticmethod
    def on_arrow_right_click(event_handler):
        """Callback statique pour changer le fond vers la droite."""
        event_handler.change_background(1)

    def change_background(self, direction):
        """Change le fond d'écran en fonction de la direction (-1 pour gauche, 1 pour droite)."""
        self.current_background_index += direction

        # Boucler les fonds d'écran en cas de dépassement des index
        if self.current_background_index < 0:
            self.current_background_index = len(self.backgrounds) - 1
        elif self.current_background_index >= len(self.backgrounds):
            self.current_background_index = 0

    def display_current_screen(self):
        """Affiche l'image de fond actuelle et les flèches sur la fenêtre."""
        current_background = self.backgrounds[self.current_background_index]
        self.window.blit(current_background, (0, 0))

        # Afficher les flèches redimensionnées
        self.window.blit(self.arrow_left, self.arrow_left_rect.topleft)
        self.window.blit(self.arrow_right, self.arrow_right_rect.topleft)

        # Dessiner les bordures autour des flèches pour voir la hitbox
        pg.draw.rect(self.window, (0, 0, 0), self.arrow_left_rect, 2)
        pg.draw.rect(self.window, (0, 0, 0), self.arrow_right_rect, 2)

    def update(self):
        """Gère les événements de Pygame, notamment les clics de souris, et appelle les callbacks."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:  # Filtre uniquement les événements de clic de souris
                if self.arrow_left_rect.collidepoint(event.pos):
                    self.event_manager.trigger_event("arrow_left_clicked", self)  # Passer `self` comme argument
                elif self.arrow_right_rect.collidepoint(event.pos):
                    self.event_manager.trigger_event("arrow_right_clicked", self)  # Passer `self` comme argument
