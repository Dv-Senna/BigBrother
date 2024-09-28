from typing import Callable
import pygame as pg
from sceneManager import *
from eventManager import *
import config
import random

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

def check_collide(rect, mouse):
	return rect.collidepoint(mouse.get_pos())

def onClickDoor():
	SoundManager.play_sound(f'triKnock{random.randint(1, 12):02d}')
	pass

def onClickEye():
	pass

def onClickLogs():
	SceneManager.setCurrentScene(f'logScene{SceneManager.getCurrentSceneName()[-1]}')
	pass



class DoorScene(Scene):
	def __init__(self, images: list, doorSwitchCallback: Callable[[bool], None], hasLeftArrow: bool, hasRightArrow: bool):
		self.images = images
		self.imageRects = [image.get_rect() for image in self.images]
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

		self.eye = pg.Rect(1290, 150, 260, 260)
		self.logs = pg.Rect(1100, 500, 700, 560)
		self.door = pg.Rect(150, 100, 800, 800)


	def mount(self):
		if self.hasLeftArrow:
			EventManager.addEventType("left_arrow", lambda event: doorLeftArrowFilter(event, self.leftArrowCollidebox))
			EventManager.registerCallback("left_arrow", lambda: self.doorSwitchCallback(True))
		if self.hasRightArrow:
			EventManager.addEventType("right_arrow", lambda event: doorRightArrowFilter(event, self.rightArrowCollidebox))
			EventManager.registerCallback("right_arrow", lambda: self.doorSwitchCallback(False))

		EventManager.addEventType("eye", lambda event: event.type==pg.MOUSEBUTTONDOWN and check_collide(self.eye, pg.mouse))
		EventManager.registerCallback("eye", onClickEye)

		EventManager.addEventType("log", lambda event: event.type==pg.MOUSEBUTTONDOWN and check_collide(self.logs, pg.mouse))
		EventManager.registerCallback("log", onClickLogs)

		EventManager.addEventType("door", lambda event: event.type==pg.MOUSEBUTTONDOWN and check_collide(self.door, pg.mouse))
		EventManager.registerCallback("door", onClickDoor)



	def unmount(self):
		EventManager.removeEventType("left_arrow")
		EventManager.removeEventType("eye")
		EventManager.removeEventType("log")
		EventManager.removeEventType("door")

		EventManager.removeEventType("right_arrow")

	def update(self, dt: int):
		mouse_pos = pg.mouse.get_pos()

		if self.eye.collidepoint(mouse_pos):
			pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
		elif self.logs.collidepoint(mouse_pos):
			pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
		elif self.door.collidepoint(mouse_pos):
			pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
		else:
			pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)


	def render(self, window: pg.Surface):
		for image, imageRect in zip(self.images, self.imageRects):
			window.blit(image, imageRect)
		if self.hasLeftArrow:
			window.blit(self.leftArrowImage, self.leftArrowCollidebox)
		if self.hasRightArrow:
			window.blit(self.rightArrowImage, self.rightArrowCollidebox)
