import pygame as pg
pg.init()
from fighter import Fighter

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Battle Game")

# set framerate
clock = pg.time.Clock()
FPS = 60

#load background image
bg_image = pg.image.load("assets/images/background/background.jpg").convert_alpha()
#init player
fighter_1 = Fighter(200, 310)
fighter_2 = Fighter(700, 310)


def draw_bg():
	scaled_bg = pg.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
	screen.blit(scaled_bg, (0, 0))

running = True
while running:
	clock.tick(FPS)
	draw_bg()
	fighter_1.draw(screen)
	fighter_2.draw(screen) 
	

	figu = 5
	fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
	# fighter_2.move()
	for event in pg.event.get():
		if event.type == pg.QUIT: running = False
	pg.display.update()

pg.quit()

