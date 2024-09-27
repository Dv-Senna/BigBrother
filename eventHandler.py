import pygame as pg

class EventHandler:
    def __init__(self, window, backgrounds, arrow_left, arrow_right):
        self.window = window
        self.backgrounds = backgrounds
        self.current_background_index = 0  # Index de l'image de fond actuelle

        # Taille et position des boutons (flèches)
        self.arrow_left_rect = pg.Rect(20, (self.window.get_height() // 2) - 50, 50, 100)  # Taille 50x100
        self.arrow_right_rect = pg.Rect(self.window.get_width() - 70, (self.window.get_height() // 2) - 50, 50, 100)  # Taille 50x100

        # Redimensionner les images pour qu'elles correspondent à la taille des hitboxes
        self.arrow_left = pg.transform.scale(arrow_left, (self.arrow_left_rect.width, self.arrow_left_rect.height))
        self.arrow_right = pg.transform.scale(arrow_right, (self.arrow_right_rect.width, self.arrow_right_rect.height))

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Quitter le jeu
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:  # Clic de souris
                if self.arrow_left_rect.collidepoint(event.pos):  # Clic sur la flèche gauche
                    self.change_background(-1)
                elif self.arrow_right_rect.collidepoint(event.pos):  # Clic sur la flèche droite
                    self.change_background(1)

    def change_background(self, direction):
        """Change le fond en fonction de la direction (-1 pour gauche, 1 pour droite)."""
        self.current_background_index += direction

        # Gérer les débordements pour les indices des images de fond
        if self.current_background_index < 0:
            self.current_background_index = len(self.backgrounds) - 1
        elif self.current_background_index >= len(self.backgrounds):
            self.current_background_index = 0

    def display_current_screen(self):
        """Affiche le fond actuel, les flèches, et les hitboxes sur la fenêtre."""
        # Afficher le fond actuel
        current_background = self.backgrounds[self.current_background_index]
        self.window.blit(current_background, (0, 0))

        # Afficher les flèches redimensionnées
        self.window.blit(self.arrow_left, self.arrow_left_rect.topleft)
        self.window.blit(self.arrow_right, self.arrow_right_rect.topleft)

        # Dessiner les bordures (hitboxes) autour des flèches
        pg.draw.rect(self.window, (0, 0, 0), self.arrow_left_rect, 2)  # Dessiner une bordure noire de 2 pixels
        pg.draw.rect(self.window, (0, 0, 0), self.arrow_right_rect, 2)  # Dessiner une bordure noire de 2 pixels
