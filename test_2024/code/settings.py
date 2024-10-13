from pygame.math import Vector2
# screen
SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 720
TILE_SIZE = 32

# overlay positions 
OVERLAY_POSITIONS = {
	'tool' : (40, SCREEN_HEIGHT - 15), 
	'seed': (70, SCREEN_HEIGHT - 5)}

PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'fruit': 9,
	'rain drops': 10,
	'greehouse': 11
}

APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

SALE_PRICES = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}


#########################################################
#define colors
FPS = 60
FONT_NAME = 'arial'

# Player properties
PLAYER_ACC = 1.5
PLAYER_FRICTION = -0.2
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = 20

# Starting platforms
PLATFORM_LIST = [(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
                 (SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT*3/4, 100, 20),
                 (125, SCREEN_HEIGHT - 350, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (137, 198, 72)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# pos
GH1_START = (4800, 3904)
GH2_START = (1600, 1344)
GH3_START = (4800, 1344)

# GH1_OUT = (4736, 3904)
# GH2_OUT = (1536, 1344)
# GH3_OUT = (4736, 1344)

START = (1630, 4457)