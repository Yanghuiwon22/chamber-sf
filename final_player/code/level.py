import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu import Menu
from dashboard import DashBoard
from realtime_data import Get_data

class Level:
	def __init__(self, game):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		self.get_data = Get_data()


		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()
		# sprite groups - greenhouse
		self.all_sprites_greenhouse = CameraGroup()
		self.all_sprites_map = CameraGroup()

		self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

		self.soil_layer = SoilLayer(self.all_sprites_map, self.collision_sprites)
		self.setup()
		self.index_screen = True
		self.overlay = Overlay(self.player)
		self.transition = Transition(self.player, self.move_layer)

		# sky
		self.rain = Rain(self.all_sprites_map)
		self.raining = randint(0,10) > 7
		self.soil_layer.raining = self.raining
		self.sky = Sky()

		# shop
		self.menu = Menu(self.player, self.toggle_shop)
		self.shop_active = False

		# greenhouse
		self.gh_active = False


		# dashboard
		self.dashboard = DashBoard(self.player, self.toggle_dashboard, self.get_data)
		self.dashboard_active = False

		# music
		# self.success = pygame.mixer.Sound('audio/success.wav')
		# self.success.set_volume(0.3)
		# self.music = pygame.mixer.Sound('audio/music.mp3')
		# self.music.play(loops = -1)

		self.player.game = game



	def setup(self):
		tmx_data = load_pygame('data/chamber-sf-map.tmx')

		# greenhouse  -----> 메인 맵에서 온실 사진
		for x, y, surf in tmx_data.get_layer_by_name('greenhouse').tiles():
			Generic(
				pos = (x * TILE_SIZE, y * TILE_SIZE - 366 + 64),
				surf = pygame.image.load('graphics/environment/Greenhouse.png'),
				groups = self.all_sprites_map
			)

		# Fence
		for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites_map, self.collision_sprites])

		# water 
		water_frames = import_folder('graphics/water')
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites_map)

		# trees 
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree(
				pos = (obj.x, obj.y), 
				surf = obj.image, 
				groups = [self.all_sprites_map, self.collision_sprites, self.tree_sprites],
				name = obj.name,
				player_add = self.player_add)

		# wildflowers 
		for obj in tmx_data.get_layer_by_name('Decoration'):
			WildFlower((obj.x, obj.y), obj.image, [self.all_sprites_map, self.collision_sprites])


		# collion tiles
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

		# Player
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					pos=(obj.x, obj.y),
					group=self.all_sprites_map,
					collision_sprites=self.collision_sprites,
					tree_sprites=self.tree_sprites,
					interaction=self.interaction_sprites,
					soil_layer=self.soil_layer,
					toggle_shop=self.toggle_shop,
					toggle_dashboard=self.toggle_dashboard
				)

			if obj.name == 'Trader':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Enter_gh1':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Enter_gh2':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Enter_gh3':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'gh1_start':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'gh2_start':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'gh3_start':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'gh1_out':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'gh2_out':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'gh3_out':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'dashboard1':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'dashboard2':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'dashboard3':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)


		# collion tilese
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        # wall
		for x, y, surf in tmx_data.get_layer_by_name('wall').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites_map, self.collision_sprites])

		Generic(
			pos = (0,0),
			surf = pygame.image.load('graphics/world/chamber-sf-map.png').convert_alpha(),  # ----> 배경 화면 사진
			groups = self.all_sprites_map,
			z = LAYERS['ground'])

	def grh_setup(self):
		tmx_data = load_pygame('data/chamber-sf-map.tmx')

		if self.dashboard.vent_data == 'fan_on':
			for x,y,surf in tmx_data.get_layer_by_name('Greenhouse Status2').tiles():
				self.fan_sprite2 = Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites_map)

			for x,y,surf in tmx_data.get_layer_by_name('Greenhouse Status1').tiles():
				self.fan_sprite1 = Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites_map)

		else:
			print('remove')
			self.all_sprites_map.remove(self.fan_sprite1)
			self.all_sprites_map.remove(self.fan_sprite2)

		self.dashboard.have_to_vent = 'off'

	def grh_water_setup(self):
		tmx_data = load_pygame('data/chamber-sf-map.tmx')

		print(f'grh_water_setup {self.dashboard.water_data}')
		if self.dashboard.water_data == 'water_on':
			for x, y, surf in tmx_data.get_layer_by_name('Greenhouse Water2').tiles():
				self.water_sprite2 = Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites_map)

			for x, y, surf in tmx_data.get_layer_by_name('Greenhouse Water1').tiles():
				self.water_sprite1 = Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites_map)

			for x, y, surf in tmx_data.get_layer_by_name('Greenhouse Water3').tiles():
				self.water_sprite3 = Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites_map)

			for x, y, surf in tmx_data.get_layer_by_name('Greenhouse Water4').tiles():
				self.water_sprite4 = Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites_map)

		else:
			print('remove')
			self.all_sprites_map.remove(self.water_sprite1)
			self.all_sprites_map.remove(self.water_sprite2)
			self.all_sprites_map.remove(self.water_sprite3)
			self.all_sprites_map.remove(self.water_sprite4)

		self.dashboard.have_to_water = 'off'


	def player_add(self,item):

		self.player.item_inventory[item] += 1
		self.success.play()

	def toggle_shop(self):
		self.shop_active = not self.shop_active

	def toggle_dashboard(self):
		self.dashboard_active = not self.dashboard_active
		self.dashboard.index = 0

	def green_house(self):
		self.gh_active = not self.gh_active

	def reset(self):
		# plants
		self.soil_layer.update_plants()

		# soil
		self.soil_layer.remove_water()
		self.raining = randint(0,10) > 7
		self.soil_layer.raining = self.raining
		if self.raining:
			self.soil_layer.water_all()

		# apples on the trees
		for tree in self.tree_sprites.sprites():
			for apple in tree.apple_sprites.sprites():
				apple.kill()
			tree.create_fruit()

		# sky
		self.sky.start_color = [255,255,255]

	def move_layer(self):
		self.green_house()
		self.player.pos.x = self.player.to_go[0]
		self.player.pos.y = self.player.to_go[1]
		# self.player.to_go = None

	def plant_collision(self):
		if self.soil_layer.plant_sprites:
			for plant in self.soil_layer.plant_sprites.sprites():
				if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
					self.player_add(plant.plant_type)
					plant.kill()
					Particle(plant.rect.topleft, plant.image, self.all_sprites_map, z = LAYERS['main'])
					self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

	def first_func(self):
		print('first_func')

	def second_func(self):
		print('second_func')

	def third_func(self):
		print('third_func')

	def run(self,dt):
		self.display_surface.fill('black')  # ---------> 검은 화면 기본세팅
		# updates
		if self.shop_active:
			self.menu.update()

		elif self.dashboard_active:
			self.dashboard.update()

		else:
			self.all_sprites_map.custom_draw(self.player)
			self.all_sprites_map.update(dt)
			self.plant_collision()

		# weather
		self.overlay.display()

		if self.raining and not self.shop_active and not self.gh_active:
			self.rain.update()
		# self.sky.display(dt)

		# transition overlay
		if self.player.sleep:                           # ------> 잠에 들면 화면이 까매지면서 모든 설정 초기화
			self.transition.play()

		if self.gh_active:
			self.my_text = self.font.render(f'{self.player.pos_layer}', True, (255, 255, 255))
			self.display_surface.blit(self.my_text, [30,30])

		if self.dashboard.light_data == 'led_off' and self.gh_active and not self.dashboard_active and self.player.pos_layer == 'mini_chamber':
			self.sky.sky_dark()

		if self.dashboard.vent_data == 'fan_on' and self.dashboard.have_to_vent == 'on':
			self.grh_setup()
		elif self.dashboard.vent_data == 'fan_off' and self.dashboard.have_to_vent == 'on':
			self.grh_setup()

		if self.dashboard.water_data == 'water_on' and self.dashboard.have_to_water == 'on':
			self.grh_water_setup()
		elif self.dashboard.water_data == 'water_off' and self.dashboard.have_to_water == 'on':
			self.grh_water_setup()







class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):

		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)
