from typing import Callable
import pygame as pg
from sceneManager import *
from eventManager import *
from storyManager import StoryManager
import config
from DialogManager import DialogManager

def init_dialog(initial_text, background_img, fontUsed, Location=(-1,-1)):
    return DialogManager(background_img, 20, initial_text, fontUsed, Location)

	

def esc_key():
	SceneManager.setCurrentScene(f'doorScene{SceneManager.getCurrentSceneName()[-1]}')


class OpenDoorScene(Scene):
	def __init__(self, image: pg.Surface, person: str):
		self.NPCDialogBackground_img = pg.image.load(
						'assets/images/utils/backgroundDialogBottom.png') 
		self.fontForNPC = pg.font.Font("assets/fonts/CourierPrime-Regular.ttf", 20)
		self.image = image
		self.imageRect = self.image.get_rect()
		self.person = person
		self.dialogManager = {}
		self.currentDialogText = ""

	def mount(self):
		StoryManager.selectPerson(self.person)
		EventManager.addEventType("back to door", lambda event: event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
		EventManager.registerCallback("back to door", esc_key)
	
	def update(self, dt: int, dialogText: str):
		if not isinstance(self.dialogManager, dict):
			self.dialogManager
		if self.currentDialogText == dialogText:
			return
		self.currentDialogText = dialogText
		self.dialogManager = init_dialog(dialogText, self.NPCDialogBackground_img, self.fontForNPC)
		self.dialogManager.toggle_visibility()



	def unmount(self):

		EventManager.removeEventType('back to door')



	def render(self, window: pg.Surface):
		window.fill((255, 0, 255))
		window.blit(self.image, self.imageRect)
		if not isinstance(self.dialogManager, dict):
			self.dialogManager.display(window)
