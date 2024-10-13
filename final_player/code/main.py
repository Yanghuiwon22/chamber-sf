import pygame, sys
from settings import *
from level import Level
from player import *
from pygame import joystick

import subprocess
import os


# script_path = os.path.join(os.path.dirname(__file__),  'main.py')
# subprocess.run(['python', script_path])

# if getattr(sys, 'frozen', False):
#     base_path = sys._MEIPASS
# else:
#     base_path = os.path.dirname(__file__)




subprocess.run(['python', ALL_PATH])


# subprocess.run(['python', ALL_PATH])
class Game:
	def __init__(self):
		pygame.init()
		try:
			self.joystick = pygame.joystick.Joystick(0)
			self.joystick.init()

		except pygame.error:
			self.joystick = None


		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('CHAMBER_SF')
		self.clock = pygame.time.Clock()
		self.level = Level(self)
		self.font_name = pygame.font.match_font(FONT_NAME)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.JOYBUTTONDOWN:
					# print(f"!{event.type}/ {event.button}")
					if event.button == 9:
						pygame.quit()
						sys.exit()


			dt = self.clock.tick() / 1000
			self.level.run(dt)
			pygame.display.update()


	def show_start_screen(self):
		# game splash/start screen

		self.screen.fill(GREEN)
		self.draw_text('Greenhouse', 60, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
		self.draw_text("Press a key to play",
					   22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
		pygame.display.flip()
		self.wait_for_key()

	def wait_for_key(self):
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pygame.event.get():

				if event.type== pygame.QUIT:
					waiting = False
					self.running = False
				if event.type == pygame.KEYUP:
					waiting = False
					self.run()
				elif event.type0  == pygame.JOYBUTTONDOWN:
					waiting = False
					self.run()

	def draw_text(self, text, size, color, x, y):
		font = pygame.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)


if __name__ == '__main__':
	game = Game()
	# game.show_start_screen()
	game.run()