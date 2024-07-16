import pygame 

class Timer:
	def __init__(self,duration,func = None):
		self.duration = duration
		self.func = func
		self.start_time = 0
		self.active = False
		self.start_time = 0

	def activate(self):
		print(f'2-1. timer activate')
		self.active = True
		self.start_time = pygame.time.get_ticks()
		# print(self.current_time, self.start_time)   # -> 문제없음

	def deactivate(self):
		# print(f'2-2. timer deactivate')
		self.active = False
		self.start_time = 0

	def update(self):
		self.current_time = pygame.time.get_ticks()
		# print(self.current_time) # -> 문제 없음
		if self.start_time != 0:
			print(f'{self.current_time} - {self.start_time}')
		# if self.current_time - self.start_time >= self.duration and self.start_time != 0:
			# print(f'{self.current_time} - {self.start_time}')
		if self.current_time - self.start_time >= self.duration:
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()

