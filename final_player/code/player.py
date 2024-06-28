import pygame
from settings import *
from support import *
from timer import Timer
from realtime_data import Get_data
from transition import Transition


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop, toggle_dashboard):
		super().__init__(group)

		self.import_assets()
		self.status = 'down_idle'
		self.frame_index = 0

		# general setup
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.z = LAYERS['main']

		# movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 500

		# collision
		self.hitbox = self.rect.copy().inflate((-126,-70))
		self.collision_sprites = collision_sprites

		# timers 
		self.timers = {
			'tool use': Timer(350,self.use_tool),
			'tool switch': Timer(200),

			'seed use': Timer(350,self.use_seed),
			'seed switch': Timer(200),

			# 'data on' : Timer(500, self.on_data),
			# 'data off' : Timer(200)
		}

		# tools 
		self.tools = ['hoe','axe','water']
		self.tool_index = 0
		self.selected_tool = self.tools[self.tool_index]

		# seeds 
		self.seeds = ['corn', 'tomato']
		self.seed_index = 0
		self.selected_seed = self.seeds[self.seed_index]

		# inventory
		self.item_inventory = {
			'wood':   20,
			'apple':  20,
			'corn':   20,
			'tomato': 20
		}
		self.seed_inventory = {
		'corn': 5,
		'tomato': 5
		}
		self.money = 200

		# interaction
		self.tree_sprites = tree_sprites
		self.interaction = interaction
		self.sleep = False
		self.soil_layer = soil_layer
		self.toggle_shop = toggle_shop
		self.toggle_dashboard = toggle_dashboard

		# sound
		# self.watering = pygame.mixer.Sound('audio/water.mp3')
		# self.watering.set_volume(0.2)

		# greenhouse
		self.K_return_pressed = False

		self.game = None
		self.joystick_xmoving = None
		self.joystick_ymoving = None

		# real-time data
		self.realtime_data_status = False


		# position
		# self.tran_dark = False --> sleep
		# self.trans_bright = False

		# self.pos_map = True
		# self.pos_gh1 = False
		# self.pos_gh2 = False
		# self.pos_gh3 = False
		self.to_go = None
		self.before_go = None
		self.pos_layer = None

	def use_tool(self):
		if self.selected_tool == 'hoe':
			self.soil_layer.get_hit(self.target_pos)
		
		if self.selected_tool == 'axe':
			for tree in self.tree_sprites.sprites():
				if tree.rect.collidepoint(self.target_pos):
					tree.damage()
		
		if self.selected_tool == 'water':
			self.soil_layer.water(self.target_pos)
			self.watering.play()

	def get_target_pos(self):

		self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

	def use_seed(self):
		if self.seed_inventory[self.selected_seed] > 0:
			self.soil_layer.plant_seed(self.target_pos, self.selected_seed)
			self.seed_inventory[self.selected_seed] -= 1

	# def on_data(self):
	# 	print(f'on data \n {self.realtime_data}')
	# 	# pass


	def import_assets(self):
		self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

		for animation in self.animations.keys():
			full_path = 'graphics/character/' + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self,dt):
		self.frame_index += 4 * dt
		if self.frame_index >= len(self.animations[self.status]):
			self.frame_index = 0

		self.image = self.animations[self.status][int(self.frame_index)]

	def input(self):
		keys = pygame.key.get_pressed()

		try:
			key_up = self.game.joystick.get_axis(1)
			key_down = self.game.joystick.get_axis(1)
			key_left = self.game.joystick.get_axis(0)
			key_right = self.game.joystick.get_axis(0)
			key_tool = self.game.joystick.get_button(1)
			key_enter = self.game.joystick.get_button(0)
			key_data = self.game.joystick.get_button(5)

			joy_btn_b = self.game.joystick.get_button(2)
			joy_btn_y = self.game.joystick.get_button(3)
			joy_btn_start = self.game.joystick.get_button(9)
			joy_btn_select = self.game.joystick.get_button(8)
			joy_btn_lt = self.game.joystick.get_button(4)
			joy_btn_rt = self.game.joystick.get_button(5)

		except AttributeError:
			key_up = keys[pygame.K_UP]
			key_down = keys[pygame.K_DOWN]
			key_left = keys[pygame.K_RIGHT]
			key_right = keys[pygame.K_LEFT]
			key_tool = keys[pygame.K_SPACE]
			key_enter = keys[pygame.K_a]
			key_data = keys[pygame.K_s]

		if not self.timers['tool use'].active and not self.sleep:

			if key_up < -0.5 or key_up==True:
				self.direction.y = -1
				self.status = 'up'
			elif key_down > 0.5:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if key_left > 0.5 :
				self.direction.x = 1
				self.status = 'right'
			elif key_right == True or key_left < -0.5 :
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			# tool use
			if key_tool:
				self.timers['tool use'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0

			#  print realtime_data
			# if key_data:
			# 	self.timers['data on'].activate()
			#
			# if key_data and not self.timers['data on'].active:
			# 	self.timers['data off'].activate()


			# change tool
			if keys[pygame.K_q] and not self.timers['tool switch'].active:
				self.timers['tool switch'].activate()
				self.tool_index += 1
				self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
				self.selected_tool = self.tools[self.tool_index]

			# seed use
			if keys[pygame.K_LCTRL]:
				self.timers['seed use'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0

			# change seed 
			if keys[pygame.K_e] and not self.timers['seed switch'].active:
				self.timers['seed switch'].activate()
				self.seed_index += 1
				self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
				self.selected_seed = self.seeds[self.seed_index]

			if key_enter:
				# self.toggle_dashboard()
				collided_interaction_sprite = pygame.sprite.spritecollide(self,self.interaction,False)
				if collided_interaction_sprite:
					if collided_interaction_sprite[0].name == 'Trader':
						self.toggle_shop()

					if collided_interaction_sprite[0].name == "Enter_gh1":
						self.sleep = True
						self.pos_layer = 'mini_chamber'
						self.to_go = GH1_START[0], GH1_START[1]
						self.before_go = self.pos.x, self.pos.y

					if collided_interaction_sprite[0].name == "Enter_gh2":
						self.sleep = True
						self.pos_layer = 'greenhouse'
						self.to_go = GH2_START[0], GH2_START[1]
						self.before_go = self.pos.x, self.pos.y


					if collided_interaction_sprite[0].name == "Enter_gh3":
						self.sleep = True
						self.pos_layer = 'lab_208'
						self.to_go = GH3_START[0], GH3_START[1]
						self.before_go = self.pos.x, self.pos.y

					if collided_interaction_sprite[0].name == "dashboard1" \
							or collided_interaction_sprite[0].name == "dashboard2" \
							or collided_interaction_sprite[0].name == "dashboard3":
						self.toggle_dashboard()


					if collided_interaction_sprite[0].name == "gh1_out":
						self.sleep = True
						self.to_go = self.before_go


					if collided_interaction_sprite[0].name == "gh2_out":
						self.sleep = True
						self.to_go = self.before_go


					if collided_interaction_sprite[0].name == "gh3_out":
						self.sleep = True
						self.to_go = self.before_go
	def get_status(self):
		# idle
		if self.direction.magnitude() == 0:
			self.status = self.status.split('_')[0] + '_idle'

		# tool use
		if self.timers['tool use'].active:
			self.status = self.status.split('_')[0] + '_' + self.selected_tool

	def update_timers(self):
		for timer in self.timers.values():
			timer.update()

	def collision(self, direction):
		for sprite in self.collision_sprites.sprites():
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					if direction == 'horizontal':
						if self.direction.x > 0: # moving right
							self.hitbox.right = sprite.hitbox.left
						if self.direction.x < 0: # moving left
							self.hitbox.left = sprite.hitbox.right
						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx

					if direction == 'vertical':
						if self.direction.y > 0: # moving down
							self.hitbox.bottom = sprite.hitbox.top
						if self.direction.y < 0: # moving up
							self.hitbox.top = sprite.hitbox.bottom
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery

	def move(self,dt):

		# normalizing a vector 
		if self.direction.magnitude() > 0:
			self.direction = self.direction.normalize()

		# horizontal movement
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		# vertical movement
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')

	def update(self, dt):
		self.input()
		self.get_status()
		self.update_timers()
		self.get_target_pos()

		self.move(dt)
		self.animate(dt)
