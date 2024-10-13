import pygame
from settings import *
from timer import Timer
from realtime_data import Get_data
from PIL import Image
import requests
import json
from datetime import datetime, timedelta




class DashBoard:

    def __init__(self, player, toggle_dashboard, get_data):

        # general setup
        self.player = player
        self.toggle_dashboard = toggle_dashboard
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        # options
        self.width = 600
        self.space = 10
        self.padding = 0

        self.paragraph_height = 75
        self.title_width = 200

        # data
        self.get_data = get_data.chamber_data()
        self.get_data_graph = get_data
        self.get_lab_data = get_data.get_lab_data()
        self.get_greenhouse_data = get_data.get_gh_data()

        # control
        self.index_light = 0
        self.index_water = 0
        self.index_vent = 0

        self.control_led = ['led_off', 'led_on']
        self.control_water = ['water_off', 'water_on']
        self.control_vent = ['fan_off', 'fan_on']

        self.light_data = 'led_off'
        self.water_data = 'water_off'
        self.vent_data = 'fan_off'
        self.have_to_vent = 'off'
        self.have_to_water = 'off'



        on_button = 'graphics/edit/on_button.png'
        off_button = 'graphics/edit/off_button.png'
        self.control_status = [off_button, on_button]

        # entries
        self.options_title = ('data', 'control')
        self.options_ptitle = ('temp', 'humidity', 'light', 'light', 'water', 'ventilation')
        self.options_control = ('light', 'water', 'ventilation')
        self.options_data = ('temp', 'humidity', 'light')
        self.options_pcontent = ('temp_data', 'humi_data', 'light_data')
        self.options_text = ('Unmanipulated', 'Unmanipulated', 'Unmanipulated')

        start_date = datetime(2024, 5, 18)
        end_date = datetime.now()
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        self.options_dates = [date.strftime("%Y-%m-%d") for date in date_range]
        self.options_dates.pop()


        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

        # movement
        self.index = 0
        self.date_index = -1
        self.timer = Timer(200)


        date = self.options_dates[self.date_index]
        self.get_graph = get_data.get_chamber_graph(date, 't_h')
        self.get_graph_lux = get_data.get_chamber_graph(date, 'lux')
        # self.get_week_data = get_data.get_week_data()
        self.get_graph_week = get_data.draw_week_data()

    def setup(self):
        # create the text surfaces
        self.title_surf = []
        self.title_padding_height = 0

        self.ptitle_surf = []
        self.ptitle_padding_height = 0

        self.tdata_surf = []
        self.tdata_height = 0

        self.tcontrol_surf = []
        self.tcontrol_height = 0

        self.total_height = 0

        self.date_surf = []
        self.date_height = 0

        self.text_surf = []
        self.text_height = 0

        for text in self.options_text:
            text_surf = self.font.render(text, False, 'black')
            self.text_surf.append(text_surf)
            self.text_height += 2*self.padding + text_surf.get_height()

        for item in self.options_dates:
            text_surf = self.font.render(item, False, 'black')
            self.date_surf.append(text_surf)
            self.date_height += 2*self.padding + text_surf.get_height()



        for item in self.options_pcontent:
            text_surf = self.font.render(item, False, 'black')
            self.tdata_surf.append(text_surf)
            self.tdata_height += 2*self.padding + text_surf.get_height()
        self.total_height += self.tdata_height

        for i in range(2):
            title = self.options_title[i]
            title_surf = self.font.render(title, False, 'black')
            self.title_surf.append(title_surf)
            self.title_padding_height += title_surf.get_height() + (self.padding * 2)
            self.total_height += self.title_padding_height

            self.total_height += self.space

            # paragraph
            self.total_height += self.space

            for j in range(3):
                ptitle = self.options_ptitle[j]
                ptitle_surf = self.font.render(ptitle, False, 'black')
                self.ptitle_surf.append(ptitle_surf)
                self.ptitle_padding_height = ptitle_surf.get_height() + (self.padding * 2)

                # pcontent = self.options_pcontent[j]
                # pcontent_surf = self.font.render(pcontent, False, 'black')
                # self.pcontent_surf.append(pcontent_surf)
                # self.pcontent_padding_height = pcontent_surf.get_height() + (self.padding * 2)

                data = self.options_data[j]
                data_surf = self.font.render(data, False, 'black')
                self.tdata_surf.append(data_surf)
                self.data_height = data_surf.get_height() + (self.padding * 2)
                #
                control = self.options_control[j]
                control_surf = self.font.render(control, False, 'black')
                self.tcontrol_surf.append(control_surf)
                self.control_height = control_surf.get_height() + (self.padding * 2)

            self.total_height += self.ptitle_padding_height
            # self.total_height += self.pcontent_padding_height

        self.dashboard_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2, self.dashboard_top, self.width,
                                     self.total_height)


    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        try:
            key_escape = self.player.game.joystick.get_button(10)
            key_left = self.player.game.joystick.get_axis(0)
            key_right = self.player.game.joystick.get_axis(0)
            key_1 = self.player.game.joystick.get_button(3)
            key_2 = self.player.game.joystick.get_button(2)
            key_3 = self.player.game.joystick.get_button(1)

        except AttributeError:
            key_escape = keys[pygame.K_ESCAPE]
            key_left = keys[pygame.K_q]
            key_right = keys[pygame.K_e]
            key_1 = keys[pygame.K_z]
            key_2 = keys[pygame.K_x]
            key_3 = keys[pygame.K_c]

        if key_escape:
            self.toggle_dashboard()

        if not self.timer.active:
            if (key_left < -0.5 or key_left == True) and self.index > 0:
                self.index -= 1
                print(self.index)

                self.timer.activate()

            if key_right > 0.5 and self.index < 4:
                self.index += 1
                print(self.index)
                self.timer.activate()

            if self.index == 0 and self.player.pos_layer == 'lab_chabmer':
                if key_1:
                    if self.index_light > 0:
                        self.index_light = 0
                    else:
                        self.index_light = 1
                    self.light_data = self.control_led[self.index_light]

                    self.control_chamber(self.light_data)
                    self.timer.activate()

                if key_2:
                    if self.index_water > 0:
                        self.index_water = 0
                    else:
                         self.index_water = 1
                    self.water_data = self.control_water[self.index_water]

                    self.control_chamber(self.water_data)
                    self.have_to_water = 'on'
                    self.timer.activate()

                if key_3:
                    if self.index_vent > 0:
                        self.index_vent = 0
                    else:
                        self.index_vent = 1
                    self.vent_data = self.control_vent[self.index_vent]

                    self.control_chamber(self.vent_data)
                    self.have_to_vent = 'on'
                    self.timer.activate()

            if self.index == 1 or self.index == 2:
                if key_1 and self.date_index > -len(self.options_dates):
                    self.date_index += -1
                    self.timer.activate()

                if key_3 and self.date_index < -1:
                    self.date_index += 1
                    self.timer.activate()

                if key_2:
                    print('key2 pressed')
                    self.get__graph()
                    self.timer.activate()

            if self.index == 3 or self.index == 4:
                if key_2:
                    # date = self.options_dates[self.date_index]
                    self.get__graph()
                    self.timer.activate()

    def control_chamber(self, data):
        url = "http://113.198.63.26:14110/run_code"
        data = {'data': data}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json.dumps(data), headers=headers)

    def show_entry(self, text_surf, top):
        # title
        ## background
        title_bg_rect = pygame.Rect(self.main_rect.centerx - 100, top, 200, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', title_bg_rect, 0, 4)

        self.titie_rect = text_surf.get_rect(center=(title_bg_rect.centerx, title_bg_rect.centery))
        # self.display_surface.blit(text_surf, self.titie_rect)

    def show_entry_p(self, text_surf, top):
        for i in range(3):
            data_rect = pygame.Rect(self.main_rect.left + i * self.main_rect.width/3, top,
                                         (self.main_rect.width-self.space*2)/3 , text_surf[i].get_height() + (self.padding * 2))
            # pygame.draw.rect(self.display_surface, 'White', data_rect, 0, 4)

            self.ptitle_rect = text_surf[i].get_rect(center=(data_rect.centerx, data_rect.centery))
            self.display_surface.blit(text_surf[i], self.ptitle_rect)

    def show_entry_pc(self, text_surf, top):
        for i in range(3):
            pcontent_rect = pygame.Rect(self.main_rect.left + i*self.main_rect.width/3, top,
                                        (self.main_rect.width-self.space*2)/3, text_surf.get_height() + (self.padding * 2))
            pygame.draw.rect(self.display_surface, 'White', pcontent_rect, 0, 4)

            self.pcontent_rect = text_surf.get_rect(center=(pcontent_rect.centerx, pcontent_rect.centery))
            self.display_surface.blit(text_surf, self.pcontent_rect)

    def show_entry_pd(self, text_surf, top):
        for i in range(3):
            pdata_rect = pygame.Rect(self.main_rect.left + i*self.main_rect.width/3, top,
                                        (self.main_rect.width-self.space*2)/3, text_surf[i].get_height() + (self.padding * 2))
            pygame.draw.rect(self.display_surface, 'White', pdata_rect, 0, 4)

            self.pdata_rect = text_surf[i].get_rect(center=(pdata_rect.centerx, pdata_rect.centery))
            self.display_surface.blit(text_surf[i], self.pdata_rect)

    def show_entry_img(self, file_path, top):
        # 이미지를 파일의 형태로 넘겨주기만 하면 완성.
        img = pygame.image.load(file_path)
        img_ratio = img.get_height()/img.get_width()
        img = pygame.transform.scale(img, ((self.bg_rect.height-8*self.space)/img_ratio, self.bg_rect.height-8*self.space - self.date_rect.height))
        img_rect = pygame.Rect(SCREEN_WIDTH/2 - img.get_width()/2, top,
                               img.get_width(), img.get_height())
        pygame.draw.rect(self.display_surface, 'White', img_rect, 0, 4)

        # 이미지 그리기
        self.img_rect = img.get_rect(center=(img_rect.centerx, img_rect.centery))
        self.display_surface.blit(img, self.img_rect)

    def show_entry_btn(self, file_path, top):
        for i in range(3):
            img = pygame.image.load(file_path[i])
            img_ratio = img.get_height() / img.get_width()
            img = pygame.transform.scale(img, ((self.main_rect.width-self.space*2)/3, (self.main_rect.width-self.space*2)/3 * img_ratio))
            img_rect = pygame.Rect(self.main_rect.left + i*(self.space+img.get_width()), top,
                                   img.get_width(), img.get_height())

            # 이미지 그리기
            self.img_rect = img.get_rect(center=(img_rect.centerx, img_rect.centery))
            self.display_surface.blit(img, self.img_rect)

    def show_entry_bg(self, file_path):
        img = pygame.image.load(file_path)
        img_ratio = img.get_height()/img.get_width()
        img = pygame.transform.scale(img, [self.main_rect.width + 200, (self.main_rect.width+200)*img_ratio])
        img_rect = pygame.Rect(SCREEN_WIDTH/2 - img.get_width()/2, SCREEN_HEIGHT/2 - img.get_height()/2,
                               img.get_width(), img.get_height())
        # 이미지 그리기
        self.bg_rect = img.get_rect(center=(img_rect.centerx, img_rect.centery))
        self.display_surface.blit(img, self.bg_rect)

    # dashboard_page2
    def show_entry_date(self, text_surf, top):
        date_rect = pygame.Rect(SCREEN_WIDTH/2 - self.bg_rect.left/2, top,
                                (self.main_rect.width-self.space*2)/3, text_surf.get_height() + self.space*2)
        self.date_rect = text_surf.get_rect(center=(date_rect.centerx, date_rect.centery))
        self.display_surface.blit(text_surf, self.date_rect)

    def get_chamber_data(self):
        self.options_data = self.get_data

        self.data_surf = []
        self.data_height = 0

        for item in self.options_data:
            text_surf = self.font.render(item, False, 'black')
            self.data_surf.append(text_surf)
            self.data_height = text_surf.get_height() + 2*self.space
        self.total_height += self.data_height

    def get_grh_data(self):
        self.options_grh_data = self.get_greenhouse_data

        self.data_grh_surf = []
        self.data_grh_height = 0

        for item in self.options_grh_data:
            text_surf = self.font.render(str(item), False, 'black')
            self.data_grh_surf.append(text_surf)
            self.data_grh_height = text_surf.get_height() + 2*self.space
        self.total_height += self.data_height
    def get_lab208_data(self):
        self.options_208_data = self.get_lab_data

        self.data_208_surf = []
        self.data_208_height = 0

        for item in self.options_208_data:
            text_surf = self.font.render(str(item), False, 'black')
            self.data_208_surf.append(text_surf)
            self.data_208_height = text_surf.get_height() + 2*self.space
        self.total_height += self.data_height



    def get__graph(self):
        date = self.options_dates[self.date_index]
        self.get_data_graph.get_week_data()
        self.get_graph = self.get_data_graph.get_chamber_graph(date, 't_h')
        self.get_graph_lux = self.get_data_graph.get_chamber_graph(date, 'lux')
        self.get_graph_week = self.get_data_graph.get_week_data()

    # def get_week_graph(self):
    #     date = self.options_dates[self.date_index]
    #     self.get_graph = self.get_data_graph.get_chamber_graph(date, 't_h')
    #     self.get_graph_lux = self.get_data_graph.get_chamber_graph(date, 'lux')

    def update(self):
        print('update dashboard')
        self.input()
        self.get_chamber_data()
        self.get_grh_data()
        self.get_lab208_data()

        self.show_entry_bg('graphics/edit/monitor.png')
        pygame.draw.rect(self.display_surface, 'white', self.bg_rect)
        self.show_entry_bg('graphics/edit/monitor.png')

        print(self.player.pos_layer, self.index)
        if self.player.pos_layer == 'lab_chamber':
            if self.index == 0:
                for title_index, title_surf in enumerate(self.title_surf):
                    top = self.main_rect.top + title_index * (self.main_rect.height / 2 )
                    self.show_entry(title_surf, top)

                for title_index, surf in enumerate((self.tdata_surf, self.tcontrol_surf)):
                    top = self.main_rect.top + title_index * (self.main_rect.height / 2 )  + self.space
                    self.show_entry_p(surf, top)


                for text_index, text_surf in enumerate([self.data_surf]):
                    top = self.main_rect.top + self.space + self.ptitle_rect.height + self.space
                    self.show_entry_pd(text_surf, top)

                # control
                light_btn = self.control_status[self.index_light]
                water_btn = self.control_status[self.index_water]
                vent_btn = self.control_status[self.index_vent]

                for btn_index, btn_img in enumerate([[light_btn, water_btn, vent_btn]]):
                    top = self.main_rect.top + (self.main_rect.height / 2 ) + self.ptitle_rect.height + (self.space)*2
                    self.show_entry_btn(btn_img, top)

            elif self.index == 1:
                date_surf = self.date_surf[self.date_index]
                top = self.bg_rect.top + self.space*4
                self.show_entry_date(date_surf, top)

                file_path = 'graphics/chamber_graph/chamber_t_h.png'
                top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
                self.show_entry_img(file_path, top)

            elif self.index == 2:
                date_surf = self.date_surf[self.date_index]
                top = self.bg_rect.top + self.space*4
                self.show_entry_date(date_surf, top)

                file_path = 'graphics/chamber_graph/chamber_lux.png'
                top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
                self.show_entry_img(file_path, top)

            elif self.index == 3:
                date_surf = self.date_surf[-1]
                top = self.bg_rect.top + self.space*4
                self.show_entry_date(date_surf, top)

                file_path = 'graphics/chamber_graph/week_graph_t_h.png'
                top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
                self.show_entry_img(file_path, top)

            elif self.index == 4:
                date_surf = self.date_surf[-1]
                top = self.bg_rect.top + self.space*4
                self.show_entry_date(date_surf, top)

                file_path = 'graphics/chamber_graph/week_graph.png'
                top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
                self.show_entry_img(file_path, top)


        if self.player.pos_layer == 'greenhouse':
            if self.index == 0:
                for title_index, title_surf in enumerate(self.title_surf):
                    top = self.main_rect.top + title_index * (self.main_rect.height / 2 )
                    self.show_entry(title_surf, top)

                for title_index, surf in enumerate((self.tdata_surf, self.tcontrol_surf)):
                    top = self.main_rect.top + title_index * (self.main_rect.height / 2 )  + self.space
                    self.show_entry_p(surf, top)


                for text_index, text_surf in enumerate([self.data_grh_surf]):
                    top = self.main_rect.top + self.space + self.ptitle_rect.height + self.space
                    self.show_entry_pd(text_surf, top)

                for text_index, text_surf in enumerate([self.text_surf]):
                    top = self.main_rect.top + self.main_rect.height/2 + self.space + self.ptitle_rect.height + self.space
                    self.show_entry_pd(text_surf, top)

            elif self.index == 1:
                date_surf = self.date_surf[self.date_index]
                top = self.bg_rect.top + self.space*4
                self.show_entry_date(date_surf, top)

                # self.chamber_t_h = f'..\graphics\chamber_graph\chamber_t&h.png'
                # top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
                # self.show_entry_img(self.chamber_t_h, top)

            elif self.index == 2:
                date_surf = self.date_surf[self.date_index]
                top = self.bg_rect.top + self.space*4
                self.show_entry_date(date_surf, top)

                # self.chamber_lux = f'..\graphics\chamber_graph\chamber_lux.png'
                # top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
                # self.show_entry_img(self.chamber_lux, top)

        if self.player.pos_layer == 'lab_208':
            if self.index == 0:
                for title_index, title_surf in enumerate(self.title_surf):
                    top = self.main_rect.top + title_index * (self.main_rect.height / 2 )
                    self.show_entry(title_surf, top)

                for title_index, surf in enumerate((self.tdata_surf, self.tcontrol_surf)):
                    top = self.main_rect.top + title_index * (self.main_rect.height / 2 )  + self.space
                    self.show_entry_p(surf, top)


                for text_index, text_surf in enumerate([self.data_208_surf]):
                    top = self.main_rect.top + self.space + self.ptitle_rect.height + self.space
                    self.show_entry_pd(text_surf, top)

                for text_index, text_surf in enumerate([self.text_surf]):
                    top = self.main_rect.top + self.main_rect.height/2 + self.space + self.ptitle_rect.height + self.space
                    self.show_entry_pd(text_surf, top)


            elif self.index == 1:
                date_surf = self.date_surf[self.date_index]
                top = self.bg_rect.top + self.space*4
                self.show_entry_date(date_surf, top)
                #
                # self.chamber_t_h = f'..\graphics\chamber_graph\chamber_t&h.png'
                # top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
                # self.show_entry_img(self.chamber_t_h, top)

            elif self.index == 2:
                date_surf = self.date_surf[self.date_index]
                top = self.bg_rect.top + self.space*4
                self.show_entry_date(date_surf, top)

                # self.chamber_lux = f'..\graphics\chamber_graph\chamber_lux.png'
                # top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
                # self.show_entry_img(self.chamber_lux, top)


















