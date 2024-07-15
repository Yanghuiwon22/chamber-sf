import pygame
from timer import Timer
from settings import *
class Edit:
    def __init__(self):
        self.timer = Timer(200)
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.display_surface = pygame.display.get_surface()

    def input(self):
        mouse = pygame.mouse.get_pressed()

    def display(self):
        save_surf = self.font.render('Save', False, 'Black')
        save_rect = save_surf.get_rect()
        save_rect.topleft = SCREEN_WIDTH-10-save_rect.width, SCREEN_HEIGHT-10-save_rect.height

        editmode_surf = self.font.render('Edit Mode', False, 'Black')
        editmode_rect = editmode_surf.get_rect()
        editmode_rect.topleft = 10, 10

        self.display_surface.blit(save_surf, save_rect)
        self.display_surface.blit(editmode_surf, editmode_rect)
    def update(self):
        self.input()
        self.display()

