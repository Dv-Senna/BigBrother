import pygame as pg

class DialogManager:
    def __init__(self, window, backgroundImg, margin):
        self._window = window
        self._backgroundImg = backgroundImg
        self._margin = margin

    def wrap_text(self, text, font, max_width):
        """Divise le texte en plusieurs lignes si nécessaire."""
        words = text.split(' ')
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

    def DisplayText(self, Text):
        # Blitter l'image de fond centrée en bas avec une marge
        img_rect = self._backgroundImg.get_rect(center=(self._window.get_width() // 2, self._window.get_height() - self._margin))
        img_rect.bottom = self._window.get_height() - self._margin  # Ajuste pour que l'image soit en bas avec la marge
        self._window.blit(self._backgroundImg, img_rect.topleft)

        # Blitter le texte centré dans l'image
        font = pg.font.Font(None, 36)  # Police par défaut, taille 36
        text_lines = self.wrap_text(Text, font, img_rect.width - 20)  # 20 pixels de marge

        # Calculer la position de départ pour centrer verticalement le texte
        total_height = sum(font.get_height() for _ in text_lines)
        start_y = img_rect.centery - total_height // 2

        for line in text_lines:
            text_surface = font.render(line, True, (255, 255, 255))  # Texte en blanc
            text_rect = text_surface.get_rect(center=(img_rect.centerx, start_y))
            self._window.blit(text_surface, text_rect)
            start_y += font.get_height()  # Déplacer vers la ligne suivante

    def ShowDialog(self):
        self._visible = True  # Rendre visible l'image et le texte

    def HideDialog(self):
        self._visible = False  # Cacher l'image et le texte
        # Optionnel : Effacer la zone de dialogue
        self._window.fill((0, 0, 0), rect=(0, self._window.get_height() - self._backgroundImg.get_height() - self._margin, self._window.get_width(), self._backgroundImg.get_height() + self._margin))
