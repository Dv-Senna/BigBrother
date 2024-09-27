import pygame as pg
from sceneManager import *
from scenes.doorScene import *


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
	SceneManager.setCurrentScene(f"{SceneNames.DOOR}{currentDoorScene}")

	fpsClock = pg.time.Clock()
	window = pg.display.set_mode((16*70, 9*70))
	pg.display.set_caption("BigBrother")

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_a:
					currentDoorScene = 1
					SceneManager.setCurrentScene(f"{SceneNames.DOOR}{currentDoorScene}")
				if event.key == pg.K_s:
					currentDoorScene = 0
					SceneManager.setCurrentScene(f"{SceneNames.DOOR}{currentDoorScene}")
		
		# update section
		SceneManager.getCurrentScene().update(fpsClock.get_time())

		# draw section
		window.fill((0, 0, 0))

		SceneManager.getCurrentScene().render(window)

		pg.display.update()
		fpsClock.tick(60)



if __name__ == "__main__":
	main()