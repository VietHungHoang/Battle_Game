import pygame as pg

class Fighter():
	def __init__(self, x, y):
		self.rect = pg.Rect((x, y, 80, 280))
		self.vel_y = 0
		self.jumping = False
		self.attack_type = 0
		self.attacking = False
	def draw(self, surface):
		pg.draw.rect(surface, 'red', self.rect)

	def attack(self, surface, target): 
		self.attacking = True
		attacking_rect = pg.Rect((self.rect.centerx, self.rect.y, self.rect.width * 2, self.rect.height))
		if attacking_rect.colliderect(target.rect):
			print(1)

		pg.draw.rect(surface,'green', attacking_rect)

	def move(self, screen_width, screen_height, surface, target):
		SPEED = 10
		GRAVITY = 2
		dx, dy = 0, 0


		# get key pressed
		key = pg.key.get_pressed()

		# can only perform other actions if not currently attacking
		if not self.attacking:
			if key[pg.K_a]: dx = -SPEED
			if key[pg.K_d]: dx = SPEED
			if key[pg.K_w] and self.jumping == False:
				self.vel_y = -30
				self.jumping = True

			if key[pg.K_r] or key[pg.K_t]:
				self.attack(surface, target)
				#determine which attack type was used
				if key[pg.K_r]: self.attack_type = 1
				if key[pg.K_t]: self.attack_type = 2

		# apply garvity
		self.vel_y += GRAVITY
		dy += self.vel_y

		# ensure player stays on screen
		if self.rect.left + dx < 0: dx = -self.rect.left
		if self.rect.left + dx > screen_width: dx = screen_width - self.rect.right
		if self.rect.bottom + dy > screen_height - 110: # at floor
			self.vel_y = 0
			self.jumping = False
			dy = screen_height - 110 - self.rect.bottom
		# update coords
		self.rect.x += dx
		self.rect.y += dy
		
		#print(1)
		# viet hung haong


		


