import pygame
from pygame import image
from pygame.sprite import spritecollide
from config import *
import math
import random

class Spritesheet:
	def __init__(self, file):
		self.sheet = pygame.image.load(file).convert()
	
	def get_sprite(self, x, y ,width, height):
		sprite = pygame.Surface([width, height])
		sprite.blit(self.sheet,(0,0), (x, y, width, height))
		sprite.set_colorkey(BLACK)
		return sprite 



class Player(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		
		#Place Sprite in game and configurations for loading and where it is
		self.game = game
		self._layer = PLAYER_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		#Cords and Size of Sprtie and Facing
		self.x = x * TILESIZE
		self.y = y * TILESIZE

		self.width = TILESIZE
		self.height = TILESIZE 

		self.x_change = 0
		self.y_change = 0

		self.facing = 'down'
		self.animation_loop = 1


		#Needed stuff for pygame to show the sprite
		#Png file for looks of Main Char and sprite sheet
		self.image = self.game.player_spritesheet.get_sprite(0,32,self.width,self.height)
		

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y


		

	def update(self):
		#Apply movement
		self.movement()
		self.animate()
		self.camera_move()

		self.collide_enemy()

		self.rect.x += self.x_change
		self.collide_blocks('x')
		self.rect.y += self.y_change
		self.collide_blocks('y')

		#reset x and y change vars to 0 after movement
		self.x_change = 0
		self.y_change = 0
		

	def movement(self):
		#Get key pressed
		keys = pygame.key.get_pressed()

		#wasd keys to move stuff
		if keys[pygame.K_a]:
			self.x_change -= PLAYER_SPEED
			self.facing = 'left'
			
		if keys[pygame.K_d]:
			self.x_change += PLAYER_SPEED
			self.facing = 'right'	

		if keys[pygame.K_w]:
			self.y_change -= PLAYER_SPEED
			self.facing = 'up'

		if keys[pygame.K_s]:
			self.y_change += PLAYER_SPEED
			self.facing = 'down'	
			
	def camera_move(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			#Camera to da left
			for sprite in self.game.all_sprites:
				sprite.rect.x += PLAYER_SPEED

		if keys[pygame.K_RIGHT]:
			#Camera to da right
			for sprite in self.game.all_sprites:
				sprite.rect.x -= PLAYER_SPEED

		if keys[pygame.K_UP]:
			#Camera to da up
			for sprite in self.game.all_sprites:
				sprite.rect.y += PLAYER_SPEED

		if keys[pygame.K_DOWN]:
			#Camera to da down
			for sprite in self.game.all_sprites:
				sprite.rect.y -= PLAYER_SPEED


	def collide_blocks(self, direction):
		#Function when player tries to go over obstacles that u can go over. eg rocks and trees
		if direction == "x":
			hits = pygame.sprite.spritecollide(self, self.game.blocks,False)
			if hits:
				#goes opposite way when hit rock
				if self.x_change > 0:
					self.rect.x = hits[0].rect.left - self.rect.width

				if self.x_change < 0:
					self.rect.x = hits[0].rect.right 

		if direction == "y":
			hits = pygame.sprite.spritecollide(self, self.game.blocks,False)
			if hits:
				#goes opposite way when hit rock
				if self.y_change > 0:
					self.rect.y = hits[0].rect.top - self.rect.height

				if self.y_change < 0:
					self.rect.y = hits[0].rect.bottom
	def animate(self):
		up_animations = [
			#Movement up
			self.game.player_spritesheet.get_sprite(0,0,self.width,self.height),
			self.game.player_spritesheet.get_sprite(32,0,self.width,self.height),
			self.game.player_spritesheet.get_sprite(64,0,self.width,self.height)
		]
		down_animation = [
			#Movement down
			self.game.player_spritesheet.get_sprite(0,32,self.width,self.height),
			self.game.player_spritesheet.get_sprite(64,32,self.width,self.height),
			self.game.player_spritesheet.get_sprite(96,32,self.width,self.height)
		]

		right_animation = [
			#Movement right
			self.game.player_spritesheet.get_sprite(0, 66,self.width,self.height),
			self.game.player_spritesheet.get_sprite(32,66,self.width,self.height),
			self.game.player_spritesheet.get_sprite(64,66,self.width,self.height)
		]
		left_animation = [
			#Movement left
			self.game.player_spritesheet.get_sprite(0,102,self.width,self.height),
			self.game.player_spritesheet.get_sprite(32,102,self.width,self.height),
			self.game.player_spritesheet.get_sprite(64,102,self.width,self.height)
		]
		#Animation bs
		if self.facing == "down":
			if self.y_change == 0:
				self.image == self.game.player_spritesheet.get_sprite(0,32,self.width,self.height)
			else:
				self.image = down_animation[math.floor(self.animation_loop)]
				self.animation_loop += 0.1 
				if self.animation_loop >= 3:
					self.animation_loop = 1

		if self.facing == "up":
			if self.y_change == 0:
				self.image == self.game.player_spritesheet.get_sprite(0,0,self.width,self.height)
			else:
				self.image = up_animations[math.floor(self.animation_loop)]
				self.animation_loop += 0.1 
				if self.animation_loop >= 3:
					self.animation_loop = 1		

		if self.facing == "right":
			if self.x_change == 0:
				self.image == self.game.player_spritesheet.get_sprite(64,32,self.width,self.height)
			else:
				self.image = right_animation[math.floor(self.animation_loop)]
				self.animation_loop += 0.1 
				if self.animation_loop >= 3:
					self.animation_loop = 1	

		if self.facing == "left":
			if self.x_change == 0:
				self.image == self.game.player_spritesheet.get_sprite(96,32,self.width,self.height)
			else:
				self.image = left_animation[math.floor(self.animation_loop)]
				self.animation_loop += 0.1 
				if self.animation_loop >= 3:
					self.animation_loop = 1
	def collide_enemy(self):
		hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
		if hits:
			self.kill()
			self.game.playing = False
			self.game.game_over()

class Enemy(pygame.sprite.Sprite):
	def __init__(self, game, x ,y):
		
		self.game = game
		self._layer = ENEMY_LAYER
		self.groups = self.game.all_sprites, self.game.enemies
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		
		self.x_change = 0
		self.y_change = 0

		#Get image and maske it transperant
		self.image = self.game.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
		self.image.set_colorkey(BLACK)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

		#Picks if facing left or right
		self.facing = random.choice(['left','right',])
		#Setup for if enemy move left or right and distance it does as well animations
		self.animation_loop = 1
		self.movement_loop = 0
		self.max_travel = random.randint(10,50)

	def update(self):
		#Make it move in left or right and animate
		self.movement() 
		self.animation()
		#change da sprite
		self.rect.x += self.x_change
		self.collide_blocks('x')
		self.rect.y += self.y_change
		self.collide_blocks('y')
		
		self.x_change = 0
		self.y_change = 0

	def movement(self):
		if self.facing == 'left':
			self.x_change += ENEMY_SPEED
			self.movement_loop -= 1
			#every frame thing determines if it should turn right cuz its moving left now
			if self.movement_loop <= -self.max_travel:
				self.facing = 'right'

		if self.facing == 'right':
			self.x_change -= ENEMY_SPEED
			self.movement_loop += 1
			#every frame thing determines if it should turn left cuz its moving left now
			if self.movement_loop >= self.max_travel:
				self.facing = 'left'
	def animation(self):
		up_animations = [
			#Movement up
			self.game.enemy_spritesheet.get_sprite(0,0,self.width,self.height),
			self.game.enemy_spritesheet.get_sprite(32,0,self.width,self.height),
			self.game.enemy_spritesheet.get_sprite(64,0,self.width,self.height)
		]
		down_animation = [
			#Movement down
			self.game.enemy_spritesheet.get_sprite(0,32,self.width,self.height),
			self.game.enemy_spritesheet.get_sprite(32,32,self.width,self.height),
			self.game.enemy_spritesheet.get_sprite(64,32,self.width,self.height)
		]

		right_animation = [
			#Movement right
			self.game.enemy_spritesheet.get_sprite(0,64,self.width,self.height),
			self.game.enemy_spritesheet.get_sprite(32,64,self.width,self.height),
			self.game.enemy_spritesheet.get_sprite(64,64,self.width,self.height)
		]
		left_animation = [
			#Movement left
			self.game.enemy_spritesheet.get_sprite(0,96,self.width,self.height),
			self.game.enemy_spritesheet.get_sprite(32,96,self.width,self.height),
			self.game.enemy_spritesheet.get_sprite(64,96,self.width,self.height)
		]
		#Animation bs
		if self.facing == "down":
			if self.y_change == 0:
				self.image == self.game.enemy_spritesheet.get_sprite(0,32,self.width,self.height)
			else:
				self.image = down_animation[math.floor(self.animation_loop)]
				self.animation_loop += 0.1 
				if self.animation_loop >= 3:
					self.animation_loop = 1

		if self.facing == "up":
			if self.y_change == 0:
				self.image == self.game.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
			else:
				self.image = up_animations[math.floor(self.animation_loop)]
				self.animation_loop += 0.1 
				if self.animation_loop >= 3:
					self.animation_loop = 1		

		if self.facing == "right":
			if self.x_change == 0:
				self.image == self.game.enemy_spritesheet.get_sprite(0,64,self.width,self.height)
			else:
				self.image = right_animation[math.floor(self.animation_loop)]
				self.animation_loop += 0.1 
				if self.animation_loop >= 3:
					self.animation_loop = 1	

		if self.facing == "left":
			if self.x_change == 0:
				self.image == self.game.enemy_spritesheet.get_sprite(0,96,self.width,self.height)
			else:
				self.image = left_animation[math.floor(self.animation_loop)]
				self.animation_loop += 0.1 
				if self.animation_loop >= 3:
					self.animation_loop = 1
	def collide_blocks(self, direction):
		#Function when player tries to go over obstacles that u can go over. eg rocks and trees
		if direction == "x":
			hits = pygame.sprite.spritecollide(self, self.game.blocks,False)
			if hits:
				#goes opposite way when hit rock
				if self.x_change > 0:
					self.rect.x = hits[0].rect.left - self.rect.width

				if self.x_change < 0:
					self.rect.x = hits[0].rect.right 

		if direction == "y":
			hits = pygame.sprite.spritecollide(self, self.game.blocks,False)
			if hits:
				#goes opposite way when hit rock
				if self.y_change > 0:
					self.rect.y = hits[0].rect.top - self.rect.height

				if self.y_change < 0:
					self.rect.y = hits[0].rect.bottom

class Block(pygame.sprite.Sprite):
	def __init__(self, game, x,y):
		#Connect it with the game class
		self.game = game
		self._layer = BLOCK_LAYER

		#put it in All sprite in game
		self.groups = self.game.all_sprites, self.game.blocks

		#Actually connect it
		pygame.sprite.Sprite.__init__(self,self.groups)

		#Cords
		self.x = x * TILESIZE
		self.y = y * TILESIZE
		
		#size
		self.width = TILESIZE
		self.height = TILESIZE

		#Image and rect of the Block
		self.image = self.game.terrain_spritesheet.get_sprite(64,0,self.width,self.height)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
	
class Grass(pygame.sprite.Sprite):
	def __init__(self, game, x,y):
		#Connect it with the game class
		self.game = game
		self._layer = GROUND_LAYER

		#put it in All sprite in game
		self.groups = self.game.all_sprites

		#Actually connect it
		pygame.sprite.Sprite.__init__(self,self.groups)

		#Cords
		self.x = x * TILESIZE
		self.y = y * TILESIZE
		
		#size
		self.width = TILESIZE
		self.height = TILESIZE

		#Image and rect of the Block
		self.image = self.game.terrain_spritesheet.get_sprite(0,0,self.width,self.height)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

class Button:
	def __init__(self, x, y, width, height, fg, bg, content, fontsize):
		#Which file to get text from and content on button
		self.font = pygame.font.Font('Text/ariblk.ttf',fontsize)
		self.content = content

		#Cords
		self.x = x
		self.y = y

		#Size
		self.width = width
		self.height = height

		#color of da thing
		self.fg = fg
		self.bg = bg

		#things looks
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(self.bg)
		self.rect = self.image.get_rect()

		self.rect.x = self.x
		self.rect.y = self.y

		#Text
		self.text = self.font.render(self.content, True, self.fg)
		self.text_rect = self.text.get_rect(center = (self.width / 2, self.height / 2) )
		self.image.blit(self.text,self.text_rect)

	#func is pressed. 
	def is_pressed(self,pos,pressed):
		if self.rect.collidepoint(pos):
			#if left clicked sinec python returns a list and one is true or not and right click is on pressed[1]?
			if pressed[0]:
				return True
			return False
		return False

class Attack(pygame.sprite.Sprite):
	
	def __init__(self, game, x ,y):

		self.game = game

		self._layer = PLAYER_LAYER

		#put in group
		self.groups = self.game.all_sprites, self.game.attacks
		#Actually connect it
		pygame.sprite.Sprite.__init__(self,self.groups)

		self.x = x
		self.y = y
		self.width = TILESIZE
		self.height = TILESIZE

		self.animation_loop = 0

		self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
		self.rect = self.image.get_rect()
		
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self):
		self.animate()
		self.collide()
	
	def collide(self):
		hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

	def animate(self):
		direction = self.game.player.facing

		attack_animation = [
			self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
			self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
			self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),

			self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
			self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
			self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),

			self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
			self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
			self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),

			self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height)
		]

		if direction == 'up' or direction == 'down' or direction == 'right' or direction == 'left':
			self.image = attack_animation[math.floor(self.animation_loop)]
			self.animation_loop += .5

			if self.animation_loop >= 10:
				self.kill()