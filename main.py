import pygame as pg



def main():
	fpsClock = pg.time.Clock()
	window = pg.display.set_mode((16*70, 9*70))
	pg.display.set_caption("BigBrother")

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return
			
		window.fill((255, 0, 0))
		pg.display.update()
		fpsClock.tick(60)

if __name__ == "__main__":
	main()