import pygame as pg
from eventManager import *
from sceneManager import *
from scenes.doorScene import *
from scenes.mainMenuScene import *
from log_manager import Typewriter
from sounds_manager import SoundManager
import random
import config


class SceneNames:
	DOOR = "doorScene"
	MAIN_MENU = "mainMenuScene"

# to check if a scene is a doorScene, just use `if SceneManager.getCurrentSceneName()[:-1] == SceneNames.DOOR`4
# you can also check for currentScene == -1

currentDoor = 0
DOOR_COUNT = 0

SOUND_FREQ = 20 * 1000 # random sound approx each X sec.
random_sound_wait = 0

def changeCurrentDoor(goLeft: bool) -> int:
	global currentDoor
	global DOOR_COUNT

	if goLeft and currentDoor > 0:
		currentDoor -= 1
	elif not goLeft and currentDoor < DOOR_COUNT - 1:
		currentDoor += 1
	SceneManager.setCurrentScene(f"{SceneNames.DOOR}{currentDoor}")


def main():
	global currentDoor
	global DOOR_COUNT

	doorScenes = [
		DoorScene(pg.image.load("assets/images/scenes/background1.jpg"), changeCurrentDoor, False, True),
		DoorScene(pg.image.load("assets/images/scenes/background2.jpg"), changeCurrentDoor, True, True),
		DoorScene(pg.image.load("assets/images/scenes/background3.jpg"), changeCurrentDoor, True, False),
	]
	DOOR_COUNT = len(doorScenes)
	for i in range(0, len(doorScenes)):
		SceneManager.addScene(f"{SceneNames.DOOR}{i}", doorScenes[i])

	SceneManager.addScene(SceneNames.MAIN_MENU, MainMenuScene())

	SceneManager.setCurrentScene(f"{SceneNames.DOOR}{currentDoor}")


	fpsClock = pg.time.Clock()
	window = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
	pg.display.set_caption("BigBrother")

	# Fonts
	pg.font.init()
	font = pg.font.Font("assets/fonts/CourierPrime-Regular.ttf", 12)

	# Sound
	SoundManager.load_all()
	SoundManager.play_ambient('outdoor_subsurb_birds', 4)

	last_update_sound = pg.time.get_ticks()
	random_sound_wait = SOUND_FREQ * (1 + random.random())

	typewriters = []
	texts = []
	with open('example_text.txt') as f:
		texts = f.read().split('\n')

	texts += 10 * ['']

	EventManager.addEventType("key_h", lambda event: event.type == pg.KEYDOWN and event.key == pg.K_h)
	callbackHandlerH = EventManager.registerCallback("key_h", 
												 lambda: displayAllLogs(typewriters, texts, font, 100))

	while True:
		if not EventManager.update():
			return

		# update section
		SceneManager.update(fpsClock.get_time())

		# draw section
		window.fill((0, 0, 0))

		SceneManager.render(window)

		# render text
		for typewriter in typewriters:
			typewriter.update()
			typewriter.draw(window)

		now = pg.time.get_ticks()

		if now - last_update_sound > random_sound_wait:
			print('test')
			SoundManager.play_ambient_small(0.1)
			random_sound_wait = SOUND_FREQ * (1 + random.random())
			last_update_sound = now

		# darken for transition
		blackScreenSurface = pg.Surface((window.get_rect().w, window.get_rect().h))
		blackScreenSurface.fill((0, 0, 0))
		blackScreenSurface.set_alpha(SceneManager.blackScreenOpacity)
		window.blit(blackScreenSurface, blackScreenSurface.get_rect())

		#render text
		for typewriter in typewriters:
			typewriter.update()
			typewriter.draw(window)

		pg.display.update()
		fpsClock.tick(60)



if __name__ == "__main__":
    main()
