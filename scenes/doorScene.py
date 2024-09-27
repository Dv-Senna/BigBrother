from typing import Callable
import pygame as pg
from sceneManager import *
from eventManager import *


def doorLeftArrowFilter(event: pg.event.Event) -> bool:
	if event.type == pg.KEYDOWN and event.key == pg.K_a:
		return True
	return False

def doorRightArrowFilter(event: pg.event.Event) -> bool:
	if event.type == pg.KEYDOWN and event.key == pg.K_s:
		return True
	return False

class DoorScene(Scene):
	def __init__(self, image: pg.Surface, doorSwitchCallback: Callable[[bool], None]):
		self.image = image
		self.imageRect = self.image.get_rect()
		self.doorSwitchCallback = doorSwitchCallback

		# example garbage
		self.imageRect.x = 100
		self.imageRect.y = 200
		self.position = 0.0

	def mount(self):
		self.position = 100.0
		EventManager.addEventType("left_arrow", doorLeftArrowFilter)
		EventManager.addEventType("right_arrow", doorRightArrowFilter)
		EventManager.registerCallback("left_arrow", lambda: self.doorSwitchCallback(True))
		EventManager.registerCallback("right_arrow", lambda: self.doorSwitchCallback(False))

	def unmount(self):
		EventManager.removeEventType("left_arrow")
		EventManager.removeEventType("right_arrow")

	def update(self, dt: int):
		self.position += 0.1 * dt
		self.imageRect.x = int(self.position)
	
	def render(self, window: pg.Surface):
		window.blit(self.image, self.imageRect)
