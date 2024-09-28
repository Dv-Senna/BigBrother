from typing import Callable
import pygame as pg
from sceneManager import *
from eventManager import *
import config

class OpenDoorScene(Scene):
	def __init__(self, image: pg.Surface):
		self.image = image
		self.imageRect = self.image.get_rect()

	def mount(self):
		pass
	
	def unmount(self):
		pass
	
	def update(self, dt: int):
		
		pass

	def render(self, window: pg.Surface):
		window.blit(self.image, self.imageRect)
