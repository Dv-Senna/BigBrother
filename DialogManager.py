from time import sleep

import config

from log_manager import Typewriter

class DialogManager:
    def __init__(self, backgroundImg, margin, text, font, Location=(-1, -1)):
        self._backgroundImg = backgroundImg
        self._margin = margin
        self._location = Location
        self._font = font  # Stocker la police
        self._typewriters = []
        self._imageLocation = (0, 0)
        self.text = self.wrap_text(config.WINDOW_WIDTH, text)  # Stocker le texte
        self._isIMGAdded = False
        self._img_rect = None
        self._visible = False  # Initialiser la visibilité à False

    def wrap_text(self, max_width, textToClear):
        """Divise le texte en plusieurs lignes si nécessaire."""
        words = textToClear.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + ' '
            if self._font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())  # Ajoute la ligne sans espace supplémentaire
                current_line = word + ' '
        lines.append(current_line.strip())  # Ajouter la dernière ligne sans espace
        return lines

    def set_text(self):
        # Blitter l'image de fond centrée en bas sans marge
        if self._location == (-1, -1):
            self._img_rect = self._backgroundImg.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT))
            self._img_rect.bottom = config.WINDOW_HEIGHT  # Ajuste pour que l'image soit en bas
        else:
            self._img_rect = self._backgroundImg.get_rect(center=self._location)

    def toggle_visibility(self):
        """Basculer la visibilité de la boîte de dialogue."""
        self._visible = not self._visible

    def hide(self):
        """Cacher la boîte de dialogue."""
        self._visible = False

    def display(self, window):
        """Affiche la fenêtre si la boîte de dialogue est visible."""
        if not self._isIMGAdded:
            self.set_text()
            self._isIMGAdded = True

            idLine = 0  # Pour le positionnement vertical
            for line in self.text:
                line_width = self._font.size(line)[0]
                # Calculer la position x pour centrer le texte
                x_position = self._margin
                y_position = self._img_rect.top + self._margin + (self._font.get_height() + self._margin) * idLine
                self._typewriters.append(Typewriter(line, self._font, (x_position, y_position)))
                idLine += 1

        if self._visible:
            window.blit(self._backgroundImg, self._img_rect.topleft)  # Blitter l'image
            for typewriter in self._typewriters:
                if not typewriter.done:
                    typewriter.update()
                    typewriter.draw(window)
                    break
                else:
                    typewriter.draw(window)

    def changeText(self, newText):
        self.text = self.wrap_text(self._backgroundImg.get_width() - (self._margin * 4), newText)  # Stocker le texte
        self._isIMGAdded = False
        self._typewriters = []
