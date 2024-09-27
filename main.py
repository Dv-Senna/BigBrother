import pygame as pg
from eventHandler import EventHandler
from event_manager import EventManager

def main():
    pg.init()  # Initialisation de Pygame
    fpsClock = pg.time.Clock()
    window = pg.display.set_mode((16*70, 9*70))
    pg.display.set_caption("BigBrother")

    # Charger les images de fond et les flèches
    backgrounds = [pg.image.load(f"img/scenes/background{i}.jpg") for i in range(1, 4)]  # 3 images de fond
    arrow_left = pg.image.load("img/utils/arrow_left.png")
    arrow_right = pg.image.load("img/utils/arrow_right.png")

    # Créer le gestionnaire d'événements
    event_manager = EventManager()

    # Fonction de callback pour changer le fond d'écran
    def on_arrow_left_click():
        event_handler.change_background(-1)

    def on_arrow_right_click():
        event_handler.change_background(1)

    # Enregistrer les événements et les callbacks
    event_manager.register_event("arrow_left_clicked")
    event_manager.register_event("arrow_right_clicked")
    event_manager.register_callback("arrow_left_clicked", on_arrow_left_click)
    event_manager.register_callback("arrow_right_clicked", on_arrow_right_click)

    # Initialiser l'event handler
    event_handler = EventHandler(window, backgrounds, arrow_left, arrow_right, event_manager)

    while True:
        # Gestion des événements par le fichier eventHandler.py
        event_handler.handle_events()

        # Mise à jour de l'affichage
        window.fill((255, 255, 255))  # Fond blanc
        event_handler.display_current_screen()  # Afficher l'écran actuel (fond et flèches)

        pg.display.update()
        fpsClock.tick(60)

if __name__ == "__main__":
    main()
