import pygame as pg
from sceneManager import *
from DialogManager import DialogManager


def mainSceneUpdate():
	return
def mainSceneRender():
	return

def main():
	mainScene = Scene(mainSceneUpdate, mainSceneRender)
	# SceneManager.addScene("main", mainScene)
	fpsClock = pg.time.Clock()
	pg.font.init()
	window = pg.display.set_mode((16*70, 9*70))
	pg.display.set_caption("BigBrother")
	IMG = pg.image.load("test.png")
	_dialogManagertest = DialogManager(window, IMG, 25)
	testText = """"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi archonsectetur,re magnam aliqutationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur"
	"""
	_dialogManagertest.DisplayText(testText)


	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return
		# update section
		# SceneManager.getCurrentScene().updateCallback()
		# draw section
		# window.fill((0, 0, 0))

		# SceneManager.getCurrentScene().renderCallback()

		pg.display.update()
		fpsClock.tick(60)



if __name__ == "__main__":
	main()