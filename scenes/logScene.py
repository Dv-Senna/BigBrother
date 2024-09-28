from typing import Callable
import pygame as pg
from sceneManager import *
from eventManager import *
from storyManager import StoryManager
import config

def esc_key():
	SceneManager.setCurrentScene(f'doorScene{SceneManager.getCurrentSceneName()[-1]}')

class LogScene(Scene):
	def __init__(self, image: pg.Surface, person: str, font, speed):
		self.image = image
		self.imageRect = self.image.get_rect()

		self.person = person
		self.texts = []
		self.font = font
		self.speed = speed
		self.typewriters = []

	def set_typewriters(self, typewriters):
		self.typewriters = typewriters

	def generateTypewriters(self):
		index_with_noise = 0 # get the longest sentence
		for i, text in enumerate(self.texts):
			if len(text) > len(self.texts[index_with_noise]):
				index_with_noise = i
		print("INDEX_WITH_NOISE", index_with_noise)
		wait_before = 0
		for i, text in enumerate(self.texts):
			if i != 0:
				wait_before += self.speed * len(self.texts[i-1]) * 3 + 200
			self.typewriters.append(Typewriter(
				text, 
				self.font, 
				(580, 180 + 20 * len(self.typewriters)), 
				speed=self.speed,
				#silent=i != index_with_noise,
				wait_before_start = wait_before))

	def mount(self):

		StoryManager.selectPerson(self.person)
		self.typewriters = []

		EventManager.addEventType("back to door", lambda event: event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
		EventManager.registerCallback("back to door", esc_key)


	def unmount(self):

		self.typewriters = []

		EventManager.removeEventType('back to door')
	
	def update(self, dt: int, texts):
		if self.texts == texts:
			return
		self.texts = texts
		self.generateTypewriters()

	def render(self, window: pg.Surface):
		window.blit(self.image, self.imageRect)

		for typewriter in self.typewriters:
			typewriter.update()
			typewriter.draw(window)