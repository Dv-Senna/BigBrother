from typing import Callable
import pygame as pg
from sceneManager import *
from eventManager import *
import config

def esc_key():
	SceneManager.setCurrentScene(f'doorScene{SceneManager.getCurrentSceneName()[-1]}')


class OpenDoorScene(Scene):
	def __init__(self, image: pg.Surface):
		self.image = image
		self.imageRect = self.image.get_rect()

	def mount(self):

		EventManager.addEventType("back to door", lambda event: event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
		EventManager.registerCallback("back to door", esc_key)


	def unmount(self):

		EventManager.removeEventType('back to door')


	def update(self, dt: int):
		
		pass

	def render(self, window: pg.Surface):
		window.blit(self.image, self.imageRect)
