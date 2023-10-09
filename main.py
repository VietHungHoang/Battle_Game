import pygame as pg
from random import randint
from fighter import Fighter
pg.init()
pg.mixer.init() # init mixer to insert music and sound

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Battle Game")

# set framerate
clock = pg.time.Clock()
FPS = 60

#load background image
ng_image = pg.image.load("assets/images/icons/newgame1.png").convert_alpha()
bg_image = [pg.image.load(f"assets/images/background/background{i}.jpg") for i in range(1, 8)]
warrior_sheet = pg.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pg.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
bg_index = randint(0, 6)


# set animation steps to make animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 2, 8, 8, 3, 7]

WARRIOR_SIZE = 162
WIZARD_SIZE = 250
WARRIOR_OFFSET = (-280, -225)
WIZARD_OFFSET = (-330, -322)
WARRIOR_SCALE = 4
WIZARD_SCALE = 3

#load background music
pg.mixer.music.load("assets/audio/music.mp3")
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(-1, 0.0, 5000)

sword_fx = pg.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.1)
magic_fx = pg.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.1)

#init player
fighter_1 = Fighter(1, 200, 310, WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

start_countdown = 3
start_time = None
over_time = None
round_over = False
score = [0, 0]
#font
font = pg.font.Font("assets/fonts/turok.ttf", 60)
font_score = pg.font.Font("assets/fonts/turok.ttf", 40)

#victory
victory_image = pg.image.load("assets/images/icons/victory.png").convert_alpha()

	

def draw_bg(index):
	scaled_bg = pg.transform.scale(bg_image[index], (SCREEN_WIDTH, SCREEN_HEIGHT))
	screen.blit(scaled_bg, (0, 0))

# draw fighter health bars
def draw_health_bars(health, x, y, player):
	ratio = health / 100 
	pg.draw.rect(screen, 'white',(x - 2, y - 2,400 + 4, 30 + 4))
	pg.draw.rect(screen, 'red',(x, y, 400, 30))
	pg.draw.rect(screen, 'yellow',(x, y, ratio * 400, 30)) 
	screen.blit(font_score.render(str(score[player]), True, 'red'), (x + 20, y + 40))

def start_screen():
	global start_time
	image = pg.transform.scale(ng_image, (400, 400))
	while True:
		draw_bg(bg_index)
		x, y = (SCREEN_WIDTH - 400) / 2, (SCREEN_HEIGHT - 400) / 2
		image_rect = pg.Rect(x, y, 400, 400)
		screen.blit(image, image_rect)
		for event in pg.event.get():
			if event.type == pg.QUIT: return
			elif event.type == pg.MOUSEBUTTONDOWN:
				if image_rect.collidepoint(event.pos):
					start_time = pg.time.get_ticks()
					return
		pg.display.update()

def playing():
	global start_countdown, start_time, round_over, over_time, fighter_1, fighter_2
	while True:
		clock.tick(FPS)
		draw_bg(bg_index)
		#show player stats
		draw_health_bars(fighter_1.health, 20, 20, 0)
		draw_health_bars(fighter_2.health,SCREEN_WIDTH - 20 - 400, 20,1)
		fighter_1.draw(screen)
		fighter_2.draw(screen)
		fighter_1.update()
		fighter_2.update()
		if start_countdown > 0:
			screen.blit(font.render(str(start_countdown), True, 'red'), (490, 100))
			if pg.time.get_ticks() - start_time >= 1000:
				start_time = pg.time.get_ticks()
				start_countdown -= 1
		else:
			fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
			fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
		if not round_over: # check if figher was die
			if fighter_1.death:
				round_over = True
				score[1] += 1
				over_time = pg.time.get_ticks()
			if fighter_2.death:
				round_over = True
				score[0] += 1
				over_time = pg.time.get_ticks()
				
		else:
			if pg.time.get_ticks() - over_time > 2000: # reset a new game
				start_countdown = 3
				round_over = False
				fighter_1 = Fighter(1, 200, 310, WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
				fighter_2 = Fighter(2, 700, 310, WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
			else: screen.blit(victory_image, (355, 130))


		for event in pg.event.get():
			if event.type == pg.QUIT: return
		pg.display.update()
def main():
	start_screen()
	playing()
if __name__ == '__main__':
	main()
pg.quit()

