import sys
import pygame as pg
from sceneManager import *
from eventManager import *
import config

isLeftArrowButtonPress = False
isRightArrowButtonPress = False

def doorRightArrowFilter(event: pg.event.Event, collidebox: pg.Rect) -> bool:
    global isRightArrowButtonPress
    if event.type != pg.MOUSEBUTTONDOWN:
        isRightArrowButtonPress = False
        return False
    if isRightArrowButtonPress:
        return False
    isRightArrowButtonPress = True
    if collidebox.collidepoint(pg.mouse.get_pos()):
        return True
    return False

def doorLeftArrowFilter(event: pg.event.Event, collidebox: pg.Rect) -> bool:
    global isLeftArrowButtonPress
    if event.type != pg.MOUSEBUTTONDOWN:
        isLeftArrowButtonPress = False
        return False
    if isLeftArrowButtonPress:
        return False
    isLeftArrowButtonPress = True
    if collidebox.collidepoint(pg.mouse.get_pos()):
        return True
    return False

def playButtonFilter(event: pg.event.Event, collidebox: pg.Rect) -> bool:
    if event.type == pg.MOUSEBUTTONDOWN:  # Check if mouse button is pressed
        if collidebox.collidepoint(pg.mouse.get_pos()):  # Check if the click was inside the button's rectangle
            return True
    return False

def playButtonCallback():
    SceneManager.setCurrentScene("doorScene0")  # Set the scene to the first door scene

def quitButtonFilter(event: pg.event.Event, collidebox: pg.Rect) -> bool:
    if event.type == pg.MOUSEBUTTONDOWN:
        if collidebox.collidepoint(pg.mouse.get_pos()):
            return True
    return False

def quitButtonCallback():
    pg.quit()  # Quit pygame
    sys.exit()  # Exit the program

class MainMenuScene(Scene):
    def __init__(self, play_button: pg.surface, quit_button: pg.surface):
        self.background = "assets/images/scenes/background1.jpg"
        
        # Play button setup
        self.play_buttonRect = play_button.get_rect()
        self.play_button = play_button
        self.play_buttonRect.centerx = config.WINDOW_WIDTH // 2  # Center horizontally
        self.play_buttonRect.centery = config.WINDOW_HEIGHT // 2  # Center vertically
        
        # Quit button setup
        self.quit_buttonRect = quit_button.get_rect()
        self.quit_button = quit_button
        self.quit_buttonRect.centerx = config.WINDOW_WIDTH // 2  # Center horizontally
        self.quit_buttonRect.centery = config.WINDOW_HEIGHT // 1.5  # Position below the play button

    def mount(self):
        # Register events for play and quit buttons
        EventManager.addEventType("play_button", lambda event: playButtonFilter(event, self.play_buttonRect))
        EventManager.addEventType("quit_button", lambda event: quitButtonFilter(event, self.quit_buttonRect))

        # Register callbacks for play and quit buttons
        EventManager.registerCallback("play_button", playButtonCallback)
        EventManager.registerCallback("quit_button", quitButtonCallback)

    def unmount(self):
        EventManager.removeEventType("play_button")
        EventManager.removeEventType("quit_button")

    def render(self, window: pg.Surface):
        # Render the background and buttons
        background_image = pg.image.load(self.background)
        window.blit(background_image, (0, 0))
        window.blit(self.play_button, self.play_buttonRect)
        window.blit(self.quit_button, self.quit_buttonRect)
