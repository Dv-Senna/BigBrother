import pygame as pg
from eventHandler import EventHandler


def main():
    pg.init()  # Initialisation de Pygame
    fpsClock = pg.time.Clock()
    window = pg.display.set_mode((16*70, 9*70))  # Taille de la fenêtre
    pg.display.set_caption("BigBrother")

    # Charger les images de fond et les flèches
    backgrounds = [pg.image.load(f"img/scenes/background{i}.jpg") for i in range(1, 4)]  # 3 images de fond
    arrow_left = pg.image.load("img/utils/arrow_left.png")
    arrow_right = pg.image.load("img/utils/arrow_right.png")

    # Initialisation du gestionnaire d'événements
    event_handler = EventHandler(window, backgrounds, arrow_left, arrow_right)

    while True:
        # Gestion des événements par le fichier eventHandler.py
        event_handler.handle_events()

        # Mise à jour de l'affichage dans la fenêtre
        window.fill((255, 255, 255))  # Fond blanc
        event_handler.display_current_screen()  # Afficher l'écran actuel (fond et flèches)

        pg.display.update()
        fpsClock.tick(60)

if __name__ == "__main__":
    main()
