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
bg_image = pg.image.load("assets/images/background/background.jpg")
warrior_sheet = pg.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pg.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# set animation steps to make animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 2, 8, 8, 3, 7]

WARRIOR_SIZE = 162
WIZARD_SIZE = 250
WARRIOR_OFFSET = (-280, -225)
WIZARD_OFFSET = (-330, -322)
WARRIOR_SCALE = 4
WIZARD_SCALE = 3

#init player
fighter_1 = Fighter(1, 200, 310, WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET, warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter_2 = Fighter(2, 700, 310, WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET, wizard_sheet, WIZARD_ANIMATION_STEPS)


def draw_bg():
	scaled_bg = pg.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
	screen.blit(scaled_bg, (0, 0))

# draw fighter health bars
def draw_health_bars(health, x, y):
	ratio = health / 100
	pg.draw.rect(screen, 'red',(x, y, 400, 30))
	pg.draw.rect(screen, 'yellow',(x, y, ratio * 400, 30))

running = True
while running:
	clock.tick(FPS)
	draw_bg()

	#show player stats
	draw_health_bars(fighter_1.health, 20, 20)
	draw_health_bars(fighter_2.health,SCREEN_WIDTH - 20 - 400, 20)
	fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
	fighter_1.draw(screen)
	fighter_2.draw(screen) 
	fighter_1.update()
	fighter_2.update()
	fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
	for event in pg.event.get():
		if event.type == pg.QUIT: running = False
	pg.display.update()

pg.quit()

