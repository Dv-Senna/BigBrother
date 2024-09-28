import pygame

from sceneManager import SceneManager
from sceneManager import SceneManager
from sounds_manager import SoundManager

# Display text function
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clear screen function
def clear_screen(window):
    window.fill(BLACK)
    pygame.display.flip()


# Typewriter effect using time tracking (non-blocking)
class Typewriter:
    def __init__(self, text, font, pos, speed=50, wait_before_start=0, silent=False, on_finish=lambda: None):
        self.text = text
        self.pos = pos
        self.font = font
        self.speed = speed  # Speed in milliseconds per character
        self.wait = wait_before_start  # Wait in milliseconds before it starts
        self.current_index = 0
        self.last_update_time = pygame.time.get_ticks()
        self.done = False
        self.silent = silent

        self.on_finish = on_finish

    def update(self):
        now = pygame.time.get_ticks()
        delay = now - self.last_update_time        
        if self.drawable() and delay > self.speed:
            self.last_update_time = now
            if self.current_index < len(self.text):
                if self.current_index == 0:
                    SoundManager.play_sound('GUI Sound Effects_038', 0.01)
                self.current_index += min(2, len(self.text) - self.current_index)
                print("test")
                if not self.silent and self.text[self.current_index - 1] != ' ':
                    SoundManager.play_sound('TF_GUI-Sound-7', 0.01)
        if not self.done and self.current_index >= len(self.text): # If we want it to disappear
            self.on_finish()
            self.done = True
    
    def drawable(self):
        now = pygame.time.get_ticks()

        delay = now - self.last_update_time
        if delay < self.wait:
            return False
        else:
            self.wait = 0
            return True


    def draw(self, surface):
        #if self.drawable():
        text_surface = self.font.render(self.text[:self.current_index], True, WHITE)
        surface.blit(text_surface, self.pos)
