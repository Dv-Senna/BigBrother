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
	background_img = pg.image.load("test.png")

	testText = """"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi archonsectetur,re magnam aliqutationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur"
	"""
	dialog_manager = DialogManager(window, background_img, 20,  testText)
	dialog_manager.display()
	dialog_manager.hide()
	print(dialog_manager.getVisiblity())
	# dialog_manager.set_text(testText)
	# dialog_manager.toggle_visibility()

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return
		pg.display.update()
		fpsClock.tick(60)



if __name__ == "__main__":
	main()