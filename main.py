import pygame as pg
from eventManager import *
from sceneManager import *
from scenes.doorScene import *
from scenes.mainMenuScene import *
from log_manager import Typewriter

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
	pg.font.init()
	window = pg.display.set_mode((16*70, 9*70))
	pg.display.set_caption("BigBrother")
	background_img = pg.image.load("test.png")

	testText = """"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi archonsectetur,re magnam aliqutationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur"
	"""
	_dialogManagertest.DisplayText(testText)


	typewriters = []

	dialog_manager = DialogManager(window, background_img, 20,  testText)
	dialog_manager.display()
	dialog_manager.hide()
	print(dialog_manager.getVisiblity())
	# dialog_manager.set_text(testText)
	# dialog_manager.toggle_visibility()

	while True:
		if not EventManager.update():
			return

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
