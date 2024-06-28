import pygame, sys
from settings import *
from level import Level
from player import *
from pygame import joystick
import sqlite3


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

		conn = sqlite3.connect('game_data.db')
		self.cur = conn.cursor()

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


	# def show_start_screen(self):
	# 	# game splash/start screen
	#
	# 	self.screen.fill(GREEN)
	# 	self.draw_text('Greenhouse', 60, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
	# 	self.draw_text("log in to start",
	# 				   22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
	#
	# 	pygame.display.flip()
	# 	self.wait_for_key()

	def login_site(self):
		index = 0
		input_list = [[], []]

		error_message = 'log  in to start game'
		error_color = BLACK
		while True:
			self.screen.fill(GREEN)

			self.draw_text('Chamber-sf', 60, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)


			self.draw_text(error_message, 30, error_color, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 60 + 10)
			pygame.draw.rect(self.screen, (255,255,255), [SCREEN_WIDTH / 2 - 180*3/2, SCREEN_HEIGHT / 4 + 110 + 10, 180*3, (60+10)*4])
			self.draw_text('LOGIN', 30, (255, 127, 0), SCREEN_WIDTH / 2 - 180*3/2 + 50, SCREEN_HEIGHT / 4 + 110 + 10+10)

			rect_id = pygame.Rect(SCREEN_WIDTH / 2 - 180*3/2 +20, SCREEN_HEIGHT / 4 + 170 +10, 180*3 -40, 60)
			rect_pw = pygame.Rect(SCREEN_WIDTH / 2 - 180*3/2 +20, SCREEN_HEIGHT / 4 + 170 + 60 + 20 + 10, 180*3 - 40, 60)


			if index % 2 == 0:
				pygame.draw.rect(self.screen, (0,136,85), rect_id, 2)
				pygame.draw.rect(self.screen, (200, 200, 200), rect_pw, 2)

			else:
				pygame.draw.rect(self.screen, (200, 200, 200), rect_id, 2)
				pygame.draw.rect(self.screen, (0,136,85), rect_pw, 2)

			self.draw_text('ID', 30, (176, 176, 176), SCREEN_WIDTH / 2 - 180*3/2 + 50, SCREEN_HEIGHT / 4 + 170+20)
			self.draw_text('PW', 30, (176, 176, 176), SCREEN_WIDTH / 2 - 180*3/2 + 50, SCREEN_HEIGHT / 4 + 170 + 60 + 20 +20)

			rect_signin = pygame.Rect(SCREEN_WIDTH / 2 - 30 - 60,SCREEN_HEIGHT / 4 + 170 + 60 + 20 + 10+ 60+10, 180, 60)
			pygame.draw.rect(self.screen, (0,136,85), rect_signin)
			self.draw_text('SIGN IN', 30, (255,255,255), SCREEN_WIDTH / 2 - 30 - 60 + 90, SCREEN_HEIGHT / 4 + 170 + 60 + 20 + 90)

			id = ''.join(input_list[0])
			password = ''.join(input_list[1])

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					pygame.quit()

				# 아이디 비번 입력받기
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_TAB:
						index += 1
					elif event.key == pygame.K_BACKSPACE:
						if len(input_list[index % 2]) != 0:
							input_list[index % 2].pop()
					elif event.key == pygame.K_RETURN:
						result = self.cur.execute("SELECT * FROM User;")
						for row in result:
							print(row)
							if row[1] == id and row[2] == password:
								self.run()
							else:
								error_message = 'check your id & pw'
								error_color = RED
								index = 0
						input_list = [[], []]
					else:
						input_list[index % 2].append(event.unicode)

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					print('mouse')
					if rect_signin.collidepoint(pygame.mouse.get_pos()):
						result = self.cur.execute("SELECT * FROM User;")
						for row in result:
							print(row)
							if row[1] == id and row[2] == password:
								self.run()
							else:
								error_message = 'check your id & pw'
								error_color = RED
								index = 0
						input_list = [[], []]
					elif rect_id.collidepoint(pygame.mouse.get_pos()):
						index = 0

					elif rect_pw.collidepoint(pygame.mouse.get_pos()):
						index = 1

			self.draw_text(''.join(input_list[0]), 60, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 170)
			self.draw_text(''.join(input_list[1]), 60, BLACK, SCREEN_WIDTH / 2,  SCREEN_HEIGHT / 4 + 170+ 60 +20)



			pygame.display.flip()
			# self.wait_for_key()

	#
		# while try_login:
		# 	for event in pygame.event.get():
		# 		if event.type == pygame.QUIT:
		# 			pygame.quit()
		#
		# 		if event.type == pygame.KEYDOWN:
		# 			print(event.unicode)




	#
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
				elif event.type == pygame.JOYBUTTONDOWN:
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
	game.login_site()