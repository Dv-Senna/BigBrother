from typing import Callable
import pygame as pg
from sceneManager import *
from eventManager import *
import config

def esc_key():
	print('esc')

class LogScene(Scene):
	def __init__(self, image: pg.Surface):
		self.image = image
		self.imageRect = self.image.get_rect()

		self.typewriters = []

	def set_typewriters(self, typewriters):
		self.typewriters = typewriters

	def mount(self):

		EventManager.addEventType("back to door", lambda event: event.type==pg.KEYDOWN and )
		EventManager.registerCallback("back to door", )

	def unmount(self):

		EventManager.removeEventType('back to door')
	
	def update(self, dt: int):
		pass

	def render(self, window: pg.Surface):
		window.blit(self.image, self.imageRect)

		for typewriter in self.typewriters:
			typewriter.update()
			typewriter.draw(window)