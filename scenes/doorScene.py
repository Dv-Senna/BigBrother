from typing import Callable
import pygame as pg
from sceneManager import *
from eventManager import *
from storyManager import StoryManager
import config
import random
import glob

isLeftArrowButtonPress = False
isRightArrowButtonPress = False


fade_surface = pg.Surface((1920, 1080))
fade_surface.fill((0, 0, 0))  # Fill with black
alpha = 0  # Start with fully transparent
fade_surface.set_alpha(alpha)  # Set the transparency level

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
	room_id = int(SceneManager.getCurrentSceneName()[-1])

	if room_id == 0:
		print('Clicked on room 103, opens')
		SceneManager.setCurrentScene(f'openDoorScene{SceneManager.getCurrentSceneName()[-1]}')
		StoryManager.selectDialog("0")
	elif room_id == 1:
		print('Clicked on room 104, opens')
		SceneManager.setCurrentScene(f'openDoorScene{SceneManager.getCurrentSceneName()[-1]}')
		StoryManager.selectDialog("0")
	elif room_id == 2:
		print('Clicked on room 105, nothing happens')
		pass
	elif room_id == 3:
		print('Clicked on room 106, nothing happens')
		return



def onClickEye():
	room_id = int(SceneManager.getCurrentSceneName()[-1])

	if room_id == 0:
		SoundManager.play_sound('scream_man')
	elif room_id == 1:
		SoundManager.play_sound('scream_man')
	elif room_id == 2:
		SoundManager.play_sound('scream_man')
	elif room_id == 3:
		SoundManager.play_sound('scream_woman', 0.1)
		SoundManager.stop_sound('crying_1')

	SceneManager.getCurrentScene().dead=True

def onClickLogs():
	SceneManager.setCurrentScene(f'logScene{SceneManager.getCurrentSceneName()[-1]}')
	pass




class DoorScene(Scene):
	isSetup = False
	eyes = []
	eyes_rect = []

	@staticmethod
	def setup():
		

		for path in glob.glob("assets/eye/*"):
			DoorScene.eyes.append(pg.image.load(path))
			DoorScene.eyes_rect.append(DoorScene.eyes[-1].get_rect())


	def __init__(self, images: list, doorSwitchCallback: Callable[[bool], None], hasLeftArrow: bool, hasRightArrow: bool):
		if not DoorScene.isSetup:
			DoorScene.setup()
		
		self.images = images
		self.imageRects = [image.get_rect() for image in self.images]
		
		self.doorSwitchCallback = doorSwitchCallback
		self.hasLeftArrow = hasLeftArrow
		self.hasRightArrow = hasRightArrow

		self.dead = False
		self.eye_dead = pg.image.load('assets/images/scenes/SceneX-CloseEye_1k.png')
		self.eye_dead_rect = self.eye_dead.get_rect()

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

		self.index = 0
		self.timer = 0
		

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

		print('mount', SceneManager.getCurrentSceneName())
		if '3' in SceneManager.getCurrentSceneName() and not self.dead:
			print('ouinnnn')
			SoundManager.play_sound('crying_1', 0.1)



	def unmount(self):
		EventManager.removeEventType("left_arrow")
		EventManager.removeEventType("eye")
		EventManager.removeEventType("log")
		EventManager.removeEventType("door")

		EventManager.removeEventType("right_arrow")

		SoundManager.sounds['crying_1'].stop()


	def update(self, dt: int):

		FRAME_DURATION = 150
		self.timer += dt

		mouse_pos = pg.mouse.get_pos()

		if self.eye.collidepoint(mouse_pos):
			pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
		elif self.logs.collidepoint(mouse_pos):
			pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
		elif self.door.collidepoint(mouse_pos):
			pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
		else:
			pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

		if self.timer > FRAME_DURATION:
			self.timer = 0
			self.index += 1
			if self.index == len(DoorScene.eyes):
				self.index = 0
	

	def render(self, window: pg.Surface):
		global alpha
		global running
		global fade_surface

		for image, imageRect in zip(self.images, self.imageRects):
			window.blit(image, imageRect)
		if self.hasLeftArrow:
			window.blit(self.leftArrowImage, self.leftArrowCollidebox)
		if self.hasRightArrow:
			window.blit(self.rightArrowImage, self.rightArrowCollidebox)
		if not self.dead:
			window.blit(DoorScene.eyes[self.index], DoorScene.eyes_rect[self.index])
		else:
			window.blit(self.eye_dead, self.eye_dead_rect)
			alpha += 5  # Increase alpha value for the fade effect
			if alpha >= 255:
				alpha = 255
				running = False  # Stop the loop when fade is complete
			fade_surface.set_alpha(alpha)  # Apply the updated alpha to the surface
			window.blit(fade_surface, (0, 0))  # Draw the fade surface on the screen
