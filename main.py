import pygame as pg
from eventManager import *
from sceneManager import *
from scenes.doorScene import *
from scenes.logScene import LogScene
from scenes.mainMenuScene import *
from log_manager import Typewriter
from scenes.openDoorScene import OpenDoorScene
from sounds_manager import SoundManager
import random
import config

from log_manager import Typewriter

class SceneNames:
	DOOR = "doorScene"
	OPEN_DOOR = "openDoorScene"
	LOG_SCENE = "logScene"
	MAIN_MENU = "mainMenuScene"


# to check if a scene is a doorScene, just use `if SceneManager.getCurrentSceneName()[:-1] == SceneNames.DOOR`4
# you can also check for currentScene == -1

currentDoor = 0
DOOR_COUNT = 0

SOUND_FREQ = 20 * 1000 # random sound approx each X sec.
random_sound_wait = 0


def load_sprite(path):
	return pg.image.load(path)

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
	global typewriters_screamer

	texts_103 = []
	with open('assets/logs/logs_103.txt') as f:
		texts_103 = f.read().split('\n')

	texts_104 = []
	with open('assets/logs/logs_104.txt') as f:
		texts_104 = f.read().split('\n')

	texts_105_1 = []
	with open('assets/logs/logs_105.txt') as f:
		texts_105_1 = f.read().split('\n')

	texts_106 = []
	with open('assets/logs/logs_106.txt') as f:
		texts_106 = f.read().split('\n')
	
	# Fonts
	pg.font.init()
	font = pg.font.Font("assets/fonts/CourierPrime-Regular.ttf", 24)
	
	doorScenes = [
		DoorScene([load_sprite("assets/images/scenes/Scene01-Background_.png")], changeCurrentDoor, False, True),
		DoorScene([load_sprite("assets/images/scenes/Scene01-Background_.png")], changeCurrentDoor, True, True),
		DoorScene([load_sprite("assets/images/scenes/Scene01-Background_.png")], changeCurrentDoor, True, True),
		DoorScene([load_sprite("assets/images/scenes/Scene01-Background_.png")], changeCurrentDoor, True, False),
	]

	openDoorScenes = [
		OpenDoorScene(pg.image.load("assets/images/scenes/screamer.jpg")),
		OpenDoorScene(pg.image.load("assets/images/scenes/screamer.jpg")),
		OpenDoorScene(pg.image.load("assets/images/scenes/screamer.jpg")),
		OpenDoorScene(pg.image.load("assets/images/scenes/screamer.jpg")),
	]

	logScenes = [
		LogScene(pg.image.load("assets/images/scenes/log.png"), texts_103, font, 1),
		LogScene(pg.image.load("assets/images/scenes/log.png"), texts_104, font, 1),
		LogScene(pg.image.load("assets/images/scenes/log.png"), texts_105_1, font, 1),
		LogScene(pg.image.load("assets/images/scenes/log.png"), texts_106, font, 1),
	]

	DOOR_COUNT = len(doorScenes)
	for i in range(0, len(doorScenes)):
		SceneManager.addScene(f"{SceneNames.DOOR}{i}", doorScenes[i])

	for i in range(0, len(doorScenes)):
		SceneManager.addScene(f"{SceneNames.OPEN_DOOR}{i}", openDoorScenes[i])

	for i in range(0, len(doorScenes)):
		SceneManager.addScene(f"{SceneNames.LOG_SCENE}{i}", logScenes[i])



	SceneManager.addScene(SceneNames.MAIN_MENU, MainMenuScene())

	SceneManager.setCurrentScene(f"{SceneNames.DOOR}{currentDoor}")


	fpsClock = pg.time.Clock()
	window = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
	pg.display.set_caption("BigBrother")


	# Sound
	SoundManager.load_all()
	SoundManager.play_ambient('outdoor_suburb_birds', 4)

	last_update_sound = pg.time.get_ticks()
	random_sound_wait = SOUND_FREQ * (1 + random.random())

	typewriters = []

	with open('text_mysterious.txt') as f:
		texts_myst = f.read().split('\n')

	EventManager.addEventType("key_h", lambda event: event.type == pg.KEYDOWN and event.key == pg.K_h)
	callbackHandlerH = EventManager.registerCallback("key_h", 
												 lambda: displayAllLogs(typewriters, texts, font, 100))
	
	# displaySpecialLog(typewriters_screamer, texts_myst, font=font, delay_between_each_line=100, speed=1, scene='openDoorScene1')


	while True:
		if not EventManager.update():
			return

		# update section
		SceneManager.update(fpsClock.get_time())

		# draw section
		window.fill((0, 0, 0))

		SceneManager.render(window)

		# render text
		for typewriter_screamer in typewriters_screamer:
			typewriter_screamer.update()
			typewriter_screamer.draw(window)

		now = pg.time.get_ticks()

		if now - last_update_sound > random_sound_wait:
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
