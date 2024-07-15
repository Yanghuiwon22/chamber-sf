import pygame
from timer import Timer
from settings import *
class Edit:
    def __init__(self, toggle_edit):
        self.timer = Timer(200)
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.display_surface = pygame.display.get_surface()

        self.toggle_edit = toggle_edit
    def input(self):
        # print('1. def input')
        mouse = pygame.mouse.get_pressed()
        self.timer.update()

        # print(f'2. timer {self.timer.active}')
        if not self.timer.active:
            if mouse[0]:
                # print('3. mouse clicked')
                if self.save_rect.collidepoint(pygame.mouse.get_pos()):
                    # print('4. save clicked')
                    self.toggle_edit()

                    self.timer.activate()
                    print('save')


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

