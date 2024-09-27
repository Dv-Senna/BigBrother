import pygame as pg
from sceneManager import *


class DoorScene(Scene):
	def __init__(self):
		self.image = pg.image.load("res/spritesheet.png")
		self.imageRect = self.image.get_rect()
		self.imageRect.x = 100
		self.imageRect.y = 200

	def update(self):
		pass
	
	def render(self, window: pg.Surface):
		window.blit(self.image, self.imageRect)
