from sceneManager import *
import pygame as pg
from DialogManager import DialogManager
from scenes.doorScene import *
from scenes.mainMenuScene import *
from log_manager import Typewriter
import config


class SceneNames:
	DOOR = "doorScene"
	MAIN_MENU = "mainMenuScene"


# to check if a scene is a doorScene, just use `if SceneManager.getCurrentSceneName()[:-1] == SceneNames.DOOR`4
# you can also check for currentScene == -1

currentDoor = 0
DOOR_COUNT = 0
from DialogManager import DialogManager

def init_dialog(window, initial_text, background_img, fontUsed):
    return DialogManager(window, background_img, 20, initial_text, fontUsed)

def mainSceneUpdate():
	return
def mainSceneRender():
	return

def main():
	mainScene = Scene(mainSceneUpdate, mainSceneRender)
	SceneManager.addScene("main", mainScene)

	fpsClock = pg.time.Clock()
	pg.font.init()
	window = pg.display.set_mode((16*70, 9*70))
	pg.display.set_caption("BigBrother")

	background_img = pg.image.load(
		'assets\\images\\utils\\test.png').convert()  # Remplacez par le chemin de votre image
	testText = """"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi archonsectetur,re magnam aliqutationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur"""

	# load font
	font = pg.font.init()
	font = pg.font.Font(None, 36)

	typewriters = []

	bottomDialogBox = init_dialog(window, testText, background_img, font)

	IMG = pg.image.load("test.png")
	_dialogManagertest = DialogManager(window, IMG, 25)
	testText = """"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi archonsectetur,re magnam aliqutationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur"
	"""
	_dialogManagertest.DisplayText(testText)
	# _dialogManagertest.UpdateText("TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST")
	# _dialogManagertest.ShowDialog()
	_dialogManagertest.HideDialog()
	_dialogManagertest.ShowDialog()
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

				if event.key == pg.K_l:
					bottomDialogBox.toggle_visibility()
				if event.key == pg.K_k:
					bottomDialogBox.changeText("Test Test Test Test Test Test Test Test Test Test Test Test ")

		for event in pg.event.get():
			if event.type == pg.QUIT:
				return

		# update section
		SceneManager.getCurrentScene().updateCallback()

		# draw section
		window.fill((0, 0, 0))

		SceneManager.getCurrentScene().renderCallback()

		pg.display.update()
		fpsClock.tick(60)



if __name__ == "__main__":
	main()