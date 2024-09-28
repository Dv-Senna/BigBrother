import pygame

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
    def __init__(self, text, font, pos, speed=50, wait_before_start=0):
        self.text = text
        self.pos = pos
        self.font = font
        self.speed = speed  # Speed in milliseconds per character
        self.wait = wait_before_start  # Wait in milliseconds before it starts
        self.current_index = 0
        self.last_update_time = pygame.time.get_ticks()
        self.done = False

    def update(self):
        now = pygame.time.get_ticks()
        delay = now - self.last_update_time        
        if self.drawable() and delay > self.speed:
            self.last_update_time = now
            if self.current_index < len(self.text):
                self.current_index += 1
            else: # If we want it to disappear
                #self.done = True
                pass
    
    def drawable(self):
        now = pygame.time.get_ticks()

        delay = now - self.last_update_time
        if delay < self.wait:
            self.wait -= delay
            return False
        else:
            delay -= self.wait
            self.wait = 0
            return True


    def draw(self, surface):
        if self.drawable():
            text_surface = self.font.render(self.text[:self.current_index], True, WHITE)
            surface.blit(text_surface, self.pos)
