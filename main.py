import pygame as pg
from sceneManager import *


def mainSceneUpdate():
	return
def mainSceneRender():
	return

def main():
	mainScene = Scene(mainSceneUpdate, mainSceneRender)
	SceneManager.addScene("main", mainScene)

	fpsClock = pg.time.Clock()
	window = pg.display.set_mode((16*70, 9*70))
	pg.display.set_caption("BigBrother")

	while True:
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