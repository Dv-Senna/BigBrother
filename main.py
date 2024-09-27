import pygame as pg
from sceneManager import *
from scenes.doorScene import *


def main():
	doorScenes = [
		DoorScene(pg.image.load("res/spritesheet.png"))
	]

	for i in range(0, len(doorScenes)):
		SceneManager.addScene(f"doorScene{i}", doorScenes[i])
	SceneManager.setCurrentScene("doorScene0")

	fpsClock = pg.time.Clock()
	window = pg.display.set_mode((16*70, 9*70))
	pg.display.set_caption("BigBrother")

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return
		
		# update section
		SceneManager.getCurrentScene().update()

		# draw section
		window.fill((0, 0, 0))

		SceneManager.getCurrentScene().render(window)

		pg.display.update()
		fpsClock.tick(60)



if __name__ == "__main__":
	main()