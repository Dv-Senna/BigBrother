import pygame as pg
from sceneManager import *


class DoorScene(Scene):
	def __init__(self, image: pg.Surface):
		self.image = image
		self.imageRect = self.image.get_rect()
		self.imageRect.x = 100
		self.imageRect.y = 200
		self.position = 0.0

	def mount(self):
		print("Scene did mount")
		self.position = 100.0

	def unmount(self):
		print("Scene did unmount")

	def update(self, dt: int):
		self.position += 0.1 * dt
		self.imageRect.x = int(self.position)
	
	def render(self, window: pg.Surface):
		window.blit(self.image, self.imageRect)
