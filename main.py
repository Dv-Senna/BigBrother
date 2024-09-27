import pygame as pg
from eventManager import *
from sceneManager import *
from DialogManager import DialogManager
from scenes.doorScene import *
from scenes.mainMenuScene import *
from log_manager import Typewriter
import config


class SceneNames:
	DOOR = "doorScene"
	MAIN_MENU = "mainMenuScene"
from sceneManager import *
from DialogManager import DialogManager

# to check if a scene is a doorScene, just use `if SceneManager.getCurrentSceneName()[:-1] == SceneNames.DOOR`4
# you can also check for currentScene == -1

currentDoor = 0
DOOR_COUNT = 0


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
		DoorScene(pg.image.load("assets/images/spritesheet.png"), changeCurrentDoor),
		DoorScene(pg.image.load("assets/images/alian_spaceship_heavy1.png"), changeCurrentDoor)
	]
	DOOR_COUNT = len(doorScenes)
	for i in range(0, len(doorScenes)):
		SceneManager.addScene(f"{SceneNames.DOOR}{i}", doorScenes[i])

	SceneManager.addScene(SceneNames.MAIN_MENU, MainMenuScene())

	SceneManager.setCurrentScene(f"{SceneNames.DOOR}{currentDoor}")


	mainScene = Scene(mainSceneUpdate, mainSceneRender)
	SceneManager.addScene("main", mainScene)
	DialogManager.DisplayText("Test")
	fpsClock = pg.time.Clock()
	window = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
	pg.display.set_caption("BigBrother")
	IMG = pg.image.load("test.png")
	_dialogManagertest = DialogManager(window, IMG, 25)
	testText = """"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi archonsectetur,re magnam aliqutationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur"
	"""
	_dialogManagertest.DisplayText(testText)
	# _dialogManagertest.UpdateText("TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST")
	# _dialogManagertest.ShowDialog()
	_dialogManagertest.HideDialog()
	_dialogManagertest.ShowDialog()

	# load font
	font = pg.font.init()
	font = pg.font.Font(None, 36)

	typewriters = []

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				return
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_a:
					currentDoorScene = 1
					SceneManager.setCurrentScene(f"{SceneNames.DOOR}{currentDoorScene}")
				if event.key == pg.K_s:
					currentDoorScene = 0
					SceneManager.setCurrentScene(f"{SceneNames.DOOR}{currentDoorScene}")

				if event.key == pg.K_g:
					typewriters.append(Typewriter('7 am: User 403 brushes his teeths', font, (300, 300)))
					typewriters.append(Typewriter('7:04 am: User 403 eats breakfast', font, (300, 325), wait_before_start=5000))

		# update section
		SceneManager.update()
		SceneManager.getCurrentScene().update(fpsClock.get_time())

		# draw section
		window.fill((0, 0, 0))

		SceneManager.getCurrentScene().render(window)

		#render text
		for typewriter in typewriters:
			typewriter.update()
			typewriter.draw(window)

		pg.display.update()
		fpsClock.tick(60)



if __name__ == "__main__":
	main()