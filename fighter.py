import pygame as pg

class Fighter():
	def __init__(self,player, x, y, size, scale, offset, sprite_sheet, animation_list, attack_sound):
		self.player = player
		self.x = x
		self.y = y
		self.size = size
		self.scale = scale
		self.offset = offset
		# 1 nomral, 2 run, 3 jump, 4 attack1, 5 attack2, 6 hit, 7 death
		self.animation_list = self.load_animation_list(sprite_sheet, animation_list)
		self.action = 0
		self.frame = 0
		self.rect = pg.Rect((x, y, 80, 180))
		self.vel_y = 0
		self.update_time = pg.time.get_ticks() # save start time to change animation
		self.running = False
		self.jumping = False
		self.attack_type = 0
		self.attacking = False
		self.attack_cooldown = 20 #cooldown time between 2 attacks
		self.attack_sound = attack_sound
		self.health = 100
		self.hit = False
		self.flip = False if self.player == 1 else True
		self.death = False
	def draw(self, surface):
		# pg.draw.rect(surface, 'red', self.rect)
		img = pg.transform.flip(self.animation_list[self.action][self.frame], self.flip, False)
		surface.blit(img,(self.rect.x + self.offset[0], self.rect.y + self.offset[1]))

	def update_action(self, new_action):
		if new_action != self.action:
			self.action = new_action
			self.update_time = pg.time.get_ticks()
			self.frame = 0

	def update(self):
		if self.health <= 0: self.death = True
		if self.death: self.update_action(6)
		elif self.hit: self.update_action(5)
		elif self.jumping: self.update_action(2)
		elif self.running: self.update_action(1)
		elif self.attacking:
			if self.attack_type == 1: self.update_action(3)
			elif self.attack_type == 2: self.update_action(4)
		else: self.action = 0
		
		animation_cooldown = 50
		if pg.time.get_ticks() - self.update_time > animation_cooldown:
			self.frame += 1
			self.update_time = pg.time.get_ticks()
		if self.frame >= len(self.animation_list[self.action]): # animation out of range animation list
			if not self.death:
				self.frame = 0 # reset frame to loop animation
				if self.action == 3 or self.action == 4: # attacked
					self.attacking = False
					self.attack_cooldown = 20 # cooldown after attack
				if self.action == 5: self.hit = False
			else: self.frame = len(self.animation_list[self.action]) - 1 #stop loop animation because fighter was death

	def load_animation_list(self, sprite_sheet, animation_list):
		img_list = []
		for i in range(len(animation_list)):
			tmp_list = []
			for j in range(animation_list[i]):
				tmp_list.append(pg.transform.scale(sprite_sheet.subsurface((j * self.size, i * self.size, self.size, self.size)), (self.size * self.scale, self.size * self.scale)))
			img_list.append(tmp_list)
		return img_list

	def attack(self, surface, target):
		if self.attack_cooldown == 0:
			self.attacking = True
			self.attack_sound.play()
			attacking_rect = pg.Rect((self.rect.centerx - 1.5 * self.rect.width, self.rect.y, self.rect.width * 3, self.rect.height))
			if attacking_rect.colliderect(target.rect):
				target.health -= 10
				target.hit = True
				if (self.flip and target.rect.x >= self.rect.x) or (not self.flip and target.rect.x <= self.rect.x):
					self.flip = False if self.flip else True
			# pg.draw.rect(surface,'green', attacking_rect)

	def move(self, screen_width, screen_height, surface, target):
		SPEED = 10
		GRAVITY = 2
		dx, dy = 0, 0
		# get key pressed
		key = pg.key.get_pressed()
		self.running = False

		# can only perform other actions if not currently attacking
		if not self.attacking and not self.death:
			if self.player == 1:
				if key[pg.K_a]:
					dx = -SPEED
					self.running = True
					self.flip = True
				if key[pg.K_d]:
					dx = SPEED
					self.running = True
					self.flip = False
				if key[pg.K_w] and self.jumping == False:
					self.vel_y = -30
					self.jumping = True

				if key[pg.K_r] or key[pg.K_t]:
					self.attack(surface, target)
					# determine which attack type was used
					if key[pg.K_r]: self.attack_type = 1
					if key[pg.K_t]: self.attack_type = 2

			if self.player == 2:
				if key[pg.K_LEFT]:
					dx = -SPEED
					self.running = True
					self.flip = True
				if key[pg.K_RIGHT]:
					dx = SPEED
					self.running = True
					self.flip = False

				if key[pg.K_UP] and self.jumping == False:
					self.vel_y = -30
					self.jumping = True

				if key[pg.K_DELETE] or key[pg.K_END]:
					self.attack(surface, target)
					# determine which attack type was used
					if key[pg.K_DELETE]: self.attack_type = 1
					if key[pg.K_END]: self.attack_type = 2


		# apply attack cooldown
		if self.attack_cooldown > 0: self.attack_cooldown -= 1
		# apply garvity
		self.vel_y += GRAVITY
		dy += self.vel_y

		# esure player 
		# self.flip = True if not self.death and not target.death and self.rect.centerx > target.rect.centerx else False

		# ensure player stays on screen
		if self.rect.left + dx < 0: dx = -self.rect.left
		if self.rect.right + dx > screen_width: dx = screen_width - self.rect.right
		if self.rect.bottom + dy > screen_height - 110: # at floor
			self.vel_y = 0
			self.jumping = False
			dy = screen_height - 110 - self.rect.bottom
		# update coords
		self.rect.x += dx
		self.rect.y += dy

		


