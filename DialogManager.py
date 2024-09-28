import pygame as pg

class DialogManager:
    def __init__(self, window, backgroundImg, margin, text):
        self._window = window
        self._backgroundImg = backgroundImg
        self._margin = margin
        self._text = text  # Stocker le texte
        self._visible = True  # Initialiser la visibilité à False
        self.set_text()

    def wrap_text(self, font, max_width):
        """Divise le texte en plusieurs lignes si nécessaire."""
        words = self._text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '

        lines.append(current_line)  # Ajouter la dernière ligne
        return lines

    def set_text(self):
        if not self._visible:
            return  # Ne rien afficher si la boîte de dialogue n'est pas visible

        # Blitter l'image de fond centrée en bas avec une marge
        img_rect = self._backgroundImg.get_rect(center=(self._window.get_width() // 2, self._window.get_height() - self._margin))
        img_rect.bottom = self._window.get_height() - self._margin  # Ajuste pour que l'image soit en bas avec la marge
        self._window.blit(self._backgroundImg, img_rect.topleft)

        # Blitter le texte centré dans l'image
        font = pg.font.Font(None, 36)  # Police par défaut, taille 36
        text_lines = self.wrap_text(font, img_rect.width - 20)  # 20 pixels de marge

        # Calculer la position de départ pour centrer verticalement le texte
        total_height = sum(font.get_height() for _ in text_lines)
        start_y = img_rect.centery - total_height // 2

        for line in text_lines:
            text_surface = font.render(line, True, (255, 255, 255))  # Texte en blanc
            text_rect = text_surface.get_rect(center=(img_rect.centerx, start_y))
            self._window.blit(text_surface, text_rect)
            start_y += font.get_height()  # Déplacer vers la ligne suivante

    def toggle_visibility(self):
        """Basculer la visibilité de la boîte de dialogue."""
        self.visible = not self._visible

    def display(self):
        """Affiche la fenêtre si la boîte de dialogue est visible."""
        if self._visible:
            pg.display.flip()  # Met à jour l'affichage

    def hide(self):
        self._backgroundImg.fill((0, 0, 0, 0))

    def getVisiblity(self):
        return self._visible