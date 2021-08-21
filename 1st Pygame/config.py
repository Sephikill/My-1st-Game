#Pygame windows settings

#Pygame window size
WIN_WIDTH = 640
WIN_HEIGHT = 470
#Game Fps
FPS = 60

#loading and drawing stuff
#Which stuff to draw and load from
PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1



#Terrain and stuff 
#Size of each tile
TILESIZE = 32

tilemap = [
	'BBBBBBBBBBBBBBBBBBBB',
	'B.................EB',
	'B..................B',
	'B......BB..........B',
	'B......BB..........B',
	'B..................B',
	'B.BB...............B',
	'B................E.B',
	'B......BBBBBBB.....B',
	'B..................B',
	'B...........BB.....B',
	'B..................B',
	'B..................B',
	'BP.................B',
	'BBBBBBBBBBBBBBBBBBBB',
]


#Sprite Stuff
#main player
PLAYER_SPEED = 3


#Enemy
ENEMY_SPEED = 2	

#Color and sound 
#Color
BLACK = (0,0,0)
WHITE = (255,255,255)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
