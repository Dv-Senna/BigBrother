import pygame as pg
from sceneManager import *
from scenes.doorScene import *
from scenes.mainMenuScene import *
from log_manager import Typewriter

class SceneNames:
	DOOR = "doorScene"
	MAIN_MENU = "mainMenuScene"

# to check if a scene is a doorScene, just use `if SceneManager.getCurrentSceneName()[:-1] == SceneNames.DOOR`4
# you can also check for currentScene == -1

def main():
	currentDoorScene = 0
	doorScenes = [
		DoorScene(pg.image.load("res/spritesheet.png")),
		DoorScene(pg.image.load("res/alian_spaceship_heavy1.png"))
	]
	for i in range(0, len(doorScenes)):
		SceneManager.addScene(f"{SceneNames.DOOR}{i}", doorScenes[i])

	SceneManager.addScene(SceneNames.MAIN_MENU, MainMenuScene())

	SceneManager.setCurrentScene(f"{SceneNames.DOOR}{currentDoorScene}")

	SceneManager.setCurrentScene("ajdjsd")

	fpsClock = pg.time.Clock()
	window = pg.display.set_mode((16*70, 9*70))
	pg.display.set_caption("BigBrother")

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