import pygame
from timer import Timer
from settings import *
from pytmx.util_pygame import load_pygame
from sprites import Generic

class Edit:
    def __init__(self, toggle_edit):
        self.timer = Timer(350)
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.display_surface = pygame.display.get_surface()

        self.toggle_edit = toggle_edit
        self.click_timer = Timer(200)

        self.selected = None

    def setup_dafault(self):
        tmx_data = load_pygame('data/chamber-sf-map.tmx')

        for x,y,surf in tmx_data.get_layer_by_name('Dafault Greenhouse').tiles():
            Generic(
                pos=(x * TILE_SIZE, y * TILE_SIZE - 366 + 64),
                surf=pygame.image.load('../graphics/environment/Greenhouse.png'),
                groups=self.all_sprites_map
            )
    def input(self):
        mouse = pygame.mouse.get_pressed()
        self.timer.update()
        self.click_timer.update()


        if not self.timer.active:
            if mouse[0]:
                if self.save_rect.collidepoint(pygame.mouse.get_pos()):
                    self.toggle_edit()
                    self.timer.activate()

        if not self.click_timer.active:
            if mouse[0]:
                if self.edit_gh_rect.collidepoint(pygame.mouse.get_pos()):
                    self.selected = 'gh'
                    self.click_timer.activate()


                if self.edit_field_rect.collidepoint(pygame.mouse.get_pos()):
                    self.selected = 'field'
                    self.click_timer.activate()

            elif mouse[2]:
                self.selected = 'delete'
                self.click_timer.activate()

    def display(self):
        # edit mode text 세팅
        save_surf = self.font.render('Save', False, 'Black')
        self.save_rect = save_surf.get_rect()
        self.save_rect.topleft = SCREEN_WIDTH-10-self.save_rect.width, SCREEN_HEIGHT-10-self.save_rect.height

        editmode_surf = self.font.render('Edit Mode', False, 'Black')
        editmode_rect = editmode_surf.get_rect()
        editmode_rect.topleft = 10, 10

        self.display_surface.blit(save_surf, self.save_rect)
        self.display_surface.blit(editmode_surf, editmode_rect)

        # 노지, 온실 선택창
        edit_box_width = 150
        edit_box_height = 300
        edit_box = pygame.Rect(SCREEN_WIDTH - 10 - edit_box_width, SCREEN_HEIGHT - 20 - self.save_rect.height - edit_box_height, edit_box_width, edit_box_height)
        pygame.draw.rect(self.display_surface, GREEN, edit_box, border_radius=10)

        # 노지, 온실 선택창 내부
        edit_gh = pygame.image.load('../graphics/environment/Greenhouse.png')
        edit_gh = pygame.transform.scale(edit_gh, (edit_gh.get_size()[0]/edit_gh.get_size()[1]*120, 120))
        get_middle = edit_box.width/2 - edit_gh.get_size()[0]/2
        self.edit_gh_rect = edit_gh.get_rect()
        self.edit_gh_rect.topleft = get_middle + edit_box.x, edit_box.y + 10
        self.display_surface.blit(edit_gh, self.edit_gh_rect.topleft)

        edit_field = pygame.image.load('../graphics/environment/field.png')
        edit_field = pygame.transform.scale(edit_field, (edit_field.get_size()[0]/edit_field.get_size()[1]*120, 120))
        get_middle = edit_box.width/2 - edit_field.get_size()[0]/2
        self.edit_field_rect = edit_field.get_rect()
        self.edit_field_rect.topleft = get_middle + edit_box.x, edit_box.y + 10 + edit_box.height/2
        self.display_surface.blit(edit_field, self.edit_field_rect.topleft)


    def update(self):
        self.display()
        self.input()

