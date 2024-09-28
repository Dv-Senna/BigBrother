from log_manager import Typewriter

class DialogManager:
    def __init__(self, window, backgroundImg, margin, text, font):
        self._window = window
        self._backgroundImg = backgroundImg
        self._margin = margin
        self._font = font  # Stocker la police
        self._typewriters = []
        self._imageLocation = (0,0)
        self.text = self.wrap_text(self._backgroundImg.get_width() - (self._margin*2), text)  # Stocker le texte
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
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)  # Ajouter la dernière ligne
        return lines

    def set_text(self):
        # Blitter l'image de fond centrée en bas avec une marge
        img_rect = self._backgroundImg.get_rect(center=(self._window.get_width() // 2, self._window.get_height() - self._margin))
        img_rect.bottom = self._window.get_height() - self._margin  # Ajuste pour que l'image soit en bas avec la marge
        self._window.blit(self._backgroundImg, img_rect.topleft)

        print(self.text)


    def toggle_visibility(self):
        """Basculer la visibilité de la boîte de dialogue."""
        self._visible = not self._visible

    def hide(self):
        """Cacher la boîte de dialogue."""
        self._visible = False

    def display(self):
        """Affiche la fenêtre si la boîte de dialogue est visible."""
        if not self._isIMGAdded:
            self.set_text()
            self._isIMGAdded = True
            # Calculer la position pour centrer l'image en bas avec la marge
            self._img_rect = self._backgroundImg.get_rect(
                center=(self._window.get_width() // 2, self._window.get_height() - self._margin))
            self._img_rect.bottom = self._window.get_height() - self._margin  # Ajuste pour que l'image soit en bas avec la marge
            idLine = 0
            for line in self.text:
                self._typewriters.append(Typewriter(line, self._font, (self._img_rect.topleft[0], self._img_rect.topleft[1] + (self._font.size(line)[1] * idLine)), wait_before_start=(50000*idLine)))
                idLine+=1

        if self._visible:
            self._window.blit(self._backgroundImg, self._img_rect.topleft)  # Blitter l'image
            for typewriter in self._typewriters:
                typewriter.update()
                typewriter.draw(self._window)

    def changeText(self, newText):
        self.text = self.wrap_text(self._backgroundImg.get_width() - (self._margin*2), newText)  # Stocker le texte
        self._typewriters = []

