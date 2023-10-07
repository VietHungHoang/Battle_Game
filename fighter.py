import pygame as pg

class Fighter():
	def __init__(self, x, y, size, scale, offset, sprite_sheet, animation_list):
		self.x = x
		self.y = y
		self.size = size
		self.scale = scale
		self.offset = offset
		self.sprite_sheet = sprite_sheet
		# 1 nomral, 2 run, 3 jump, 4 attack1, 5 attack2, 6 hit, 7 death
		self.animation_list = self.load_animation_list(animation_list)
		self.action = 0
		self.frame = 0
		self.rect = pg.Rect((x, y, 80, 180))
		self.vel_y = 0
		self.jumping = False
		self.attack_type = 0
		self.attacking = False
		self.health = 100
		self.flip = False
	def draw(self, surface):
		pg.draw.rect(surface, 'red', self.rect)
		img = pg.transform.flip(self.animation_list[self.action][self.frame], self.flip, False)
		surface.blit(img,(self.rect.x + self.offset[0], self.rect.y + self.offset[1]))

	def load_animation_list(self, animation_list):
		img_list = []
		for i in range(len(animation_list)):
			tmp_list = []
			for j in range(animation_list[i]):
				tmp_list.append(pg.transform.scale(self.sprite_sheet.subsurface((j * self.size, i * self.size, self.size, self.size)), (self.size * self.scale, self.size * self.scale)))
			img_list.append(tmp_list)
		return img_list

	def attack(self, surface, target): 
		self.attacking = True
		attacking_rect = pg.Rect((self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, self.rect.width * 2, self.rect.height))
		if attacking_rect.colliderect(target.rect):
			target.health -= 10

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
				# determine which attack type was used
				if key[pg.K_r]: self.attack_type = 1
				if key[pg.K_t]: self.attack_type = 2

		# apply garvity
		self.vel_y += GRAVITY
		dy += self.vel_y

		#esure player 
		self.flip = True if self.rect.centerx > target.rect.centerx else False

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

		


