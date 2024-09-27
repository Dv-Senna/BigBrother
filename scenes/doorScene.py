from typing import Callable
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


class DoorScene(Scene):
	def __init__(self, image: pg.Surface, doorSwitchCallback: Callable[[bool], None], hasLeftArrow: bool, hasRightArrow: bool):
		self.image = image
		self.imageRect = self.image.get_rect()
		self.doorSwitchCallback = doorSwitchCallback
		self.hasLeftArrow = hasLeftArrow
		self.hasRightArrow = hasRightArrow

		if hasLeftArrow:
			self.leftArrowImage = pg.image.load("assets/images/utils/arrow_left.png")
			self.leftArrowCollidebox = self.leftArrowImage.get_rect()
			self.leftArrowCollidebox.x = 50
			self.leftArrowCollidebox.y = config.WINDOW_HEIGHT / 2 - self.leftArrowCollidebox.h / 2

		if hasRightArrow:
			self.rightArrowImage = pg.image.load("assets/images/utils/arrow_right.png")
			self.rightArrowCollidebox = self.rightArrowImage.get_rect()
			self.rightArrowCollidebox.x = config.WINDOW_WIDTH - self.rightArrowCollidebox.w - 50
			self.rightArrowCollidebox.y = config.WINDOW_HEIGHT / 2 - self.rightArrowCollidebox.h / 2


	def mount(self):
		if self.hasLeftArrow:
			EventManager.addEventType("left_arrow", lambda event: doorLeftArrowFilter(event, self.leftArrowCollidebox))
			EventManager.registerCallback("left_arrow", lambda: self.doorSwitchCallback(True))
		if self.hasRightArrow:
			EventManager.addEventType("right_arrow", lambda event: doorRightArrowFilter(event, self.rightArrowCollidebox))
			EventManager.registerCallback("right_arrow", lambda: self.doorSwitchCallback(False))

	def unmount(self):
		EventManager.removeEventType("left_arrow")
		EventManager.removeEventType("right_arrow")

	def update(self, dt: int):
		pass

	def render(self, window: pg.Surface):
		window.blit(self.image, self.imageRect)
		if self.hasLeftArrow:
			window.blit(self.leftArrowImage, self.leftArrowCollidebox)
		if self.hasRightArrow:
			window.blit(self.rightArrowImage, self.rightArrowCollidebox)
