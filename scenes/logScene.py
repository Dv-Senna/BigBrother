from typing import Callable
import pygame as pg
from sceneManager import *
from eventManager import *
from storyManager import StoryManager
import config
from math import sin

firstInterupt = True

def check_collide(rects, links, mouse):
	collide = False
	for rect, link in zip(rects, links):
		if rect.collidepoint(mouse.get_pos()):
			collide = True
			print(link)
			currentPerson = int(SceneManager.getCurrentSceneName()[-1])
			SceneManager.setCurrentScene(f"openDoorScene{currentPerson}")
			for log in StoryManager.logs[f"{103 + currentPerson}"]:
				logContent = f'{log["start"]} - {log["end"]} : {log["text"]}'
				if logContent == link:
					StoryManager.selectDialog(log["dialog"])
					print(log)
#			StoryManager.selectDialog()
	return collide


def esc_key():
	SceneManager.setCurrentScene(f'doorScene{SceneManager.getCurrentSceneName()[-1]}')


def special_interupt():
	SceneManager.setCurrentScene("openDoorScene2")
	StoryManager.selectDialog("-1")

class LogScene(Scene):
	def __init__(self, image: pg.Surface, person: str, font, speed):
		self.image = image
		self.imageRect = self.image.get_rect()
		self.wardenImage = pg.image.load("assets/images/scenes/Warden.png")
		self.wardenImage.set_alpha(255 * 0.6)
		self.wardenImageRect = self.wardenImage.get_rect()
		self.wardenImageRect.x = config.WINDOW_WIDTH / 2 - self.wardenImageRect.w / 2
		self.wardenImageRect.y = config.WINDOW_HEIGHT / 2 - self.wardenImageRect.h / 2 + 20
		print(self.wardenImageRect)
		self.wardenOffset = 0
		self.timer = 0

		self.person = person
		self.texts = []
		self.font = font
		self.speed = speed
		self.typewriters = []
		self.logs_rect = []
		self.logs_link = []

	def set_typewriters(self, typewriters):
		self.typewriters = typewriters

	def generateTypewriters(self):
		global firstInterupt
		door_id = int(SceneManager.getCurrentSceneName()[-1])

		if door_id == 2 and firstInterupt:
			print('Loading the scene with auto screamer')
			SoundManager.play_sound('run_door', 2)

		index_with_noise = 0 # get the longest sentence
		for i, text in enumerate(self.texts):
			if len(text) > len(self.texts[index_with_noise]):
				index_with_noise = i
		wait_before = 0
		for i, text in enumerate(self.texts):
			if i != 0:
				wait_before += self.speed * len(self.texts[i-1]) * 3 + 200
			if i == len(self.texts) -1 and door_id == 2 and firstInterupt:
				on_finish = special_interupt
				firstInterupt = False
			else:
				on_finish = lambda: print('abc')
			self.logs_link.append(text)
			self.logs_rect.append(pg.Rect(580, 180 + 25 * len(self.typewriters), 830, 30))
			self.typewriters.append(Typewriter(
				text, 
				self.font, 
				(580, 180 + 25 * len(self.typewriters)), 
				speed=self.speed,
				#silent=i != index_with_noise,
				wait_before_start = wait_before,
				on_finish=on_finish))
			
		EventManager.addEventType(f"logs_0", lambda event: event.type==pg.MOUSEBUTTONDOWN and check_collide(self.logs_rect, self.logs_link, pg.mouse))
		EventManager.registerCallback(f"logs_0", lambda: None)

	def mount(self):

		self.texts = []
		self.generateTypewriters()

		StoryManager.selectPerson(self.person)
		self.typewriters = []

		EventManager.addEventType("back to door", lambda event: event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
		EventManager.registerCallback("back to door", esc_key)


	def unmount(self):

		EventManager.removeEventType(f"logs_0")


		self.typewriters = []

		EventManager.removeEventType('back to door')
	
	def update(self, dt: int, texts):
		mouse_pos = pg.mouse.get_pos()

		self.timer += dt
		self.wardenOffset = 7 * sin(self.timer * 0.001)

		touch_one = False
		for rect in self.logs_rect:
			if rect.collidepoint(mouse_pos):
				pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
				touch_one = True
		if not touch_one:
			pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

		if self.texts == texts:
			return
		self.texts = texts
		self.generateTypewriters()



	def render(self, window: pg.Surface):
		self.wardenImageRect.y += self.wardenOffset
		window.blit(self.wardenImage, self.wardenImageRect)
		self.wardenImageRect.y -= self.wardenOffset
		window.blit(self.image, self.imageRect)

		for rect in self.logs_rect:
			pass
			#pg.draw.rect(window, (255, 255, 255), rect)
		for typewriter in self.typewriters:
			typewriter.update()
			typewriter.draw(window)