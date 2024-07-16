import pygame
from timer import Timer
from settings import *
class Edit:
    def __init__(self, toggle_edit):
        self.timer = Timer(350)
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.display_surface = pygame.display.get_surface()

        self.toggle_edit = toggle_edit
    def input(self):
        mouse = pygame.mouse.get_pressed()
        self.timer.update()

        if not self.timer.active:
            if mouse[0]:
                if self.save_rect.collidepoint(pygame.mouse.get_pos()):
                    self.toggle_edit()
                    self.timer.activate()



    def display(self):
        save_surf = self.font.render('Save', False, 'Black')
        self.save_rect = save_surf.get_rect()
        self.save_rect.topleft = SCREEN_WIDTH-10-self.save_rect.width, SCREEN_HEIGHT-10-self.save_rect.height

        editmode_surf = self.font.render('Edit Mode', False, 'Black')
        editmode_rect = editmode_surf.get_rect()
        editmode_rect.topleft = 10, 10

        self.display_surface.blit(save_surf, self.save_rect)
        self.display_surface.blit(editmode_surf, editmode_rect)
    def update(self):
        self.display()
        self.input()

