import pygame
from pygame import display
from pygame.constants import QUIT
from sprites import *
from config import *
import sys

class Game:
	def __init__(self):
		#start pygame and stuff
		pygame.init()
		
		#Create Screen
		self.screen = pygame.display.set_mode( ( WIN_WIDTH , WIN_HEIGHT ) )

		#Change Pygame window name
		self.screen_name = pygame.display.set_caption('RPG thing')

		#Clock thing needed for fps
		self.clock = pygame.time.Clock()

		#Font thing
		self.font = pygame.font.Font( 'Text/ariblk.ttf' , 32 )

		#Running vairbale for game loop
		self.running = True


		#set up sprite sheets
		self.enemy_spritesheet = Spritesheet('img/Enemy_Piskel.png')
		self.player_spritesheet = Spritesheet('img/spritesheet.png')
		self.terrain_spritesheet = Spritesheet('img/TerrainSpriteSheet.png')
		self.attack_spritesheet = Spritesheet('img/Player_Atk.png')
		self.intro_background = pygame.image.load('img/Background.png')
		self.gameover_background = pygame.image.load('img/GameOver.png')		
	
	def createTilemap(self):
		for i, row in enumerate(tilemap):
			for j, column in enumerate(row):
				Grass(self, j, i)
				if column == "B":
					Block(self, j, i)
				if column == "P":
					self.player = player = Player(self, j, i)
				if column == "E":
					Enemy(self, j , i)
					
	def new(self):
		#A new game starts
		self.playing = True

		#Controll all the sprites 
		self.all_sprites = pygame.sprite.LayeredUpdates()
		#Controll all the obstacles
		self.blocks = pygame.sprite.LayeredUpdates()
		#Controll all the eneimes
		self.enemies = pygame.sprite.LayeredUpdates()
		#Controll all the attaks
		self.attacks = pygame.sprite.LayeredUpdates()

		#Create where player spawns and the terrain
		self.createTilemap()
	
	def events(self):
		#Game loop events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					#spawn attack
					if self.player.facing == 'up':
						Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)

					if self.player.facing == 'down':			
						Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)

					if self.player.facing == 'left':
						Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)

					if self.player.facing == 'right':			
						Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)



	def update(self):
		#game loop update
		self.all_sprites.update()

	def draw(self):
		#game loop draw
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		self.clock.tick(FPS)
		pygame.display.update()

	def main(self):
		#Game loop
		while self.playing == True:
			#do all the stuff in loop 
			self.events()
			self.update()
			self.draw()
	
	def game_over(self):
		text = self.font.render('U ARE DED', True, WHITE)
		text_rect = text.get_rect(center = (WIN_WIDTH / 2, WIN_HEIGHT / 2))

		restart_button =  Button(WIN_HEIGHT / 2, WIN_WIDTH / 2, 120, 50, WHITE, BLACK, 'Restart?',26)
		
		for sprite in self.all_sprites:
			sprite.kill()
		
		while self.running:
			for event in pygame.event.get():
				if event == pygame.QUIT:
					self.running = False

				mouse_pos = pygame.mouse.get_pos()
				mouse_pressed = pygame.mouse.get_pressed()

				if restart_button.is_pressed(mouse_pos, mouse_pressed):
					#Start new game
					self.new()
					self.main()
				#Display da button and text
				self.screen.blit(self.gameover_background, (0,0))
				self.screen.blit(text, text_rect)
				self.screen.blit(restart_button.image, restart_button.rect)
				self.clock.tick(FPS)
				pygame.display.update()

	def intro_screen(self):
		intro = True

		title = self.font.render('Bad Game', True, BLACK)
		title_rect = title.get_rect(x = 10, y = 10)

		play_button = Button(10,50,100,50,RED,BLACK,'GAME!',32)
		
		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					intro = False
					self.running = False
			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if play_button.is_pressed(mouse_pos, mouse_pressed):
				intro = False
		
			self.screen.blit(self.intro_background, (0,0))
			self.screen.blit(title, title_rect)
			self.screen.blit(play_button.image, play_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()




g = Game()
g.new()
g.intro_screen()
while g.running:
	g.main()
	g.game_over()

pygame.quit() 
sys.exit()