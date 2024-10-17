import pygame
from settings import *
from timer import Timer
from realtime_data import Get_data
from PIL import Image
import requests
import json
from datetime import datetime, timedelta

import os


class DashBoard:

    def __init__(self, player, toggle_dashboard, get_data):

        # general setup
        self.player = player
        self.toggle_dashboard = toggle_dashboard
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(os.path.join(ALL_PATH, 'font/LycheeSoda.ttf'), 30)

        # options
        self.width = 600
        self.space = 10
        self.padding = 0

        self.paragraph_height = 75
        self.title_width = 200

        # data
        self.get_data = get_data.chamber_data() # ---> 미니챔버 실시간 데이터 로드
        self.get_data_graph = get_data
        self.get_lab_data = get_data.get_lab_data()
        self.get_greenhouse_data = get_data.get_gh_data()
        self.get_buan_soilmoisture_data = get_data.get_buan_soilmoisture_data()
        self.get_buan_weather_data = get_data.get_buan_weather_data()
        self.aws_data = get_data.aws_data()
        self.lab_heyhome_graph = get_data.get_lab_heyhome()
        self.grh_heyhome_graph = get_data.get_grh_heyhome()

        self.lab_error = get_data.lab_error


        # self.livedata_mini_chamber = get_data.livedata_mini_chamber
        self.livedata_mini_chamber = False

        # control
        self.index_light = 0
        self.index_water = 0
        self.index_vent = 0

        self.control_led = ['L_fan', 'H_fan']
        self.control_water = ['water_off', 'water_on']
        self.control_vent = ['L_fan', 'H_fan']

        self.light_data = 'led_off'
        self.water_data = 'water_off'
        self.vent_data = 'fan_off'
        self.have_to_vent = 'off'
        self.have_to_water = 'off'

        on_button = os.path.join(ALL_PATH, 'graphics/edit/on_button.png')
        off_button = os.path.join(ALL_PATH, 'graphics/edit/off_button.png')
        self.control_status = [off_button, on_button]

        lab_led_r = os.path.join(ALL_PATH, 'graphics/lab/lab_led_r.png')
        lab_led_g = os.path.join(ALL_PATH, 'graphics/lab/lab_led_g.png')
        lab_led_b = os.path.join(ALL_PATH, 'graphics/lab/lab_led_b.png')
        lab_led_w = os.path.join(ALL_PATH, 'graphics/lab/lab_led_w.png')
        lab_led_off = os.path.join(ALL_PATH, 'graphics/lab/lab_led_off.png')
        self.led_control_status = [lab_led_off, lab_led_r, lab_led_g, lab_led_b, lab_led_w]

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
        try:
            self.get_week_data = get_data.get_week_data()
        except:
            self.get_week_data = None
        self.get_graph_week = get_data.draw_week_data()

        self.mini_chamber_graph = get_data.mini_chamber_graph

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
        #
        # for item in self.options_dates:
        #     if not self.livedata_mini_chamber:
        #         color = 'red'
        #     else:
        #         color = 'black'
        #     text_surf = self.font.render(item, False, color)
        #     self.date_surf.append(text_surf)
        #     self.date_height += 2*self.padding + text_surf.get_height()
        #


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

                self.timer.activate()

            if key_right > 0.5 and self.index < 4:
                self.index += 1
                self.timer.activate()

            if self.index == 0:
                if self.player.pos_layer == 'lab_chamber':
                    # print(f"self.options_data \n {self.options_data['light']}")
                    # if int(self.options_data['light']) >= 40:
                    #     self.index_light = 1
                    #
                    # if int(self.options_data['light']) < -15:
                    #     self.index_light = 3

                    if key_1:
                        self.index_light += 1



                        if self.index_light == 1:  # RED
                            self.light_data = 'R'
                        elif self.index_light == 2:  # GREEN
                            self.light_data = 'G'
                        elif self.index_light == 3: # BLUE
                            self.light_data = 'B'
                        elif self.index_light == 4: # WHITE
                            self.light_data = 'RGB'
                        elif self.index_light > 4:
                            self.light_data = 'RGBOFF'
                            self.index_light = 0

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

            # if self.player.pos_layer == 'buan_api':
            #     if self.index >= 2:
            #         self.index = 2

            if self.index == 1 or self.index == 2:
                if key_1 and self.date_index > -len(self.options_dates):
                    self.date_index += -1
                    self.timer.activate()

                if key_3 and self.date_index < -1:
                    self.date_index += 1
                    self.timer.activate()

                if key_2:
                    self.get__graph()
                    self.timer.activate()

            if self.index == 3 or self.index == 4:
                if key_2:
                    # date = self.options_dates[self.date_index]
                    self.get__graph()
                    self.timer.activate()

    def control_chamber(self, data):
        url = "http://192.168.0.3/"
        url = url + data
        response = requests.get(url)

        print(response.status_code, data)

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

    # 부안 필지별 토양수분 데이터 표시
    def show_field_text(self, text_surf, left, top):
        text_pos = pygame.Rect(left, top,
                                (self.main_rect.width-self.space*2)/3, text_surf.get_height() + self.space*2)
        self.text_pos = text_surf.get_rect(center=(text_pos.centerx, text_pos.centery))
        self.display_surface.blit(text_surf, self.text_pos)

    def show_entry_fake(self, top):
        fake_surf = self.font.render('Live data is currently not available : The data being displayed is historical', False, 'red')
        fake_rect = pygame.Rect(SCREEN_WIDTH/2 -  fake_surf.get_width()/2, top,
                                fake_surf.get_width(), fake_surf.get_height())
        self.fake_rect = fake_surf.get_rect(center=(fake_rect.centerx, fake_rect.centery))
        self.display_surface.blit(fake_surf, self.fake_rect)

    def show_entry_updated_time(self, text_surf, color='black'):
        updateed_time_surf = self.font.render(text_surf, False, color)
        top = self.bg_rect.bottom - updateed_time_surf.get_height() - self.space*3
        updated_time_rect = pygame.Rect(self.bg_rect.right-updateed_time_surf.get_width()-self.space*3, top,
                                        updateed_time_surf.get_width(), updateed_time_surf.get_height())

        self.updated_time_rect = updateed_time_surf.get_rect(center=(updated_time_rect.centerx, updated_time_rect.centery))
        self.display_surface.blit(updateed_time_surf, self.updated_time_rect)



    def get_chamber_data(self):
        self.options_data = self.get_data

        self.data_surf = []
        self.data_height = 0

        for item in [self.options_data['temp'], self.options_data['hum'], self.options_data['lux']]: #----------> 실시간 데이터 출력

            color = 'black'
            if item == self.options_data['temp']:
                if int(self.options_data['temp']) >= 40:
                    self.lab_error = True
                    color = 'red'

                elif int(self.options_data['temp']) < 0:
                    color = 'blue'
                    self.lab_error = True
                else:
                    self.lab_error = False

            text_surf = self.font.render(item, False, color)

            self.data_surf.append(text_surf)
            self.data_height = text_surf.get_height() + 2*self.space
        self.total_height += self.data_height
        return self.lab_error

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
            text_surf = self.font.render(f'{item}', False, 'black')
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
        self.input()
        self.get_chamber_data()
        self.get_grh_data()
        self.get_lab208_data()

        self.show_entry_bg(os.path.join(ALL_PATH, 'graphics/edit/monitor.png'))
        pygame.draw.rect(self.display_surface, 'white', self.bg_rect)
        self.show_entry_bg(os.path.join(ALL_PATH, 'graphics/edit/monitor.png'))


        if self.player.pos_layer == 'lab_chamber':
            if self.index == 0:
                # 실시간 데이터
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
                light_btn = self.led_control_status[self.index_light]
                water_btn = self.control_status[self.index_water]
                vent_btn = self.control_status[self.index_vent]

                for btn_index, btn_img in enumerate([[light_btn, water_btn, vent_btn]]):
                    top = self.main_rect.top + (self.main_rect.height / 2 ) + self.ptitle_rect.height + (self.space)*2
                    self.show_entry_btn(btn_img, top)

                self.livedata_mini_chamber = True
                if not self.livedata_mini_chamber:
                    self.show_entry_fake(top=self.bg_rect.bottom + self.space)
                    self.show_entry_updated_time(f'UPDATED TIME : {self.get_data["Date"]} {self.get_data["Time"]}',
                                             color='red')
                else:
                    self.show_entry_updated_time(f'UPDATED TIME : {self.get_data["Date"]} {self.get_data["Time"]}',
                                             color='black')

            elif self.index == 1:
                # 온습도 그래프 표시
                pass
                # title_text = 'Temperature and Humidity over Time'
                # title_surf = self.font.render(title_text, False, 'black')
                #
                # top = self.bg_rect.top + self.space * 4
                # left = self.bg_rect.left + self.bg_rect.width / 2 - title_surf.get_width() / 2
                #
                # self.display_surface.blit(title_surf, (left, top))
                #
                # # 2페이지 구성 - 그래프 이미지
                # img = pygame.image.load('../graphics/aws_temp_hum.png')
                # img = pygame.transform.scale(img, (700, 0.6 * 700))
                #
                # top_img = self.bg_rect.top + self.space * 4 + title_surf.get_height()
                # left_img = self.bg_rect.left + self.bg_rect.width / 2 - img.get_width() / 2
                #
            #     # self.display_surface.blit(img, (left_img, top_img))
            # elif self.index == 2:
            #     # 광 그래프 표시
            #     self.mini_chamber_graph = False
            #
            #     if not self.mini_chamber_graph:
            #         file_path = os.path.join(ALL_PATH, 'graphics/chamber_graph/fake_lux.png')
            #         date_text = '2024-05-23'
            #         date_surf = self.font.render(date_text, False, 'red')
            #         top = self.bg_rect.top + self.space * 4
            #         self.show_entry_date(date_surf, top)
            #     else:
            #         file_path = os.path.join(ALL_PATH, 'graphics/chamber_graph/chamber_lux.png')
            #         date_text = (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')
            #         date_surf = self.font.render(date_text, False, 'black')
            #         top = self.bg_rect.top + self.space * 4
            #         self.show_entry_date(date_surf, top)
            #
            #     # 날짜 표시
            #     top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
            #     self.show_entry_img(file_path, top)
            #
            #     if not self.mini_chamber_graph:
            #         self.show_entry_fake(top=self.bg_rect.bottom + self.space)
            #
            # elif self.index == 3:
            #     # date_surf = self.date_surf[-1]
            #     # top = self.bg_rect.top + self.space*4
            #     # self.show_entry_date(date_surf, top)
            #     #
            #     # file_path = '../graphics/chamber_graph/week_graph_t_h.png'
            #     # top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
            #     # self.show_entry_img(file_path, top)
            #     if not self.mini_chamber_graph:
            #         file_path = os.path.join(ALL_PATH, 'graphics/chamber_graph/fake_lux.png')
            #         date_text = '2024-05-23'
            #         date_surf = self.font.render(date_text, False, 'red')
            #         top = self.bg_rect.top + self.space * 4
            #         self.show_entry_date(date_surf, top)
            #     else:
            #         file_path = os.path.join(ALL_PATH, 'graphics/chamber_graph/chamber_lux.png')
            #         date_text = (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')
            #         date_surf = self.font.render(date_text, False, 'red')
            #         top = self.bg_rect.top + self.space * 4
            #         self.show_entry_date(date_surf, top)
            #
            #         # 날짜 표시
            #     top = self.bg_rect.top + self.space * 4 + self.date_rect.height + self.space
            #     self.show_entry_img(file_path, top)
            #
            #     if not self.mini_chamber_graph:
            #         self.show_entry_fake(top=self.bg_rect.bottom + self.space)
            #
            #
            # elif self.index == 4:
            #     date_surf = self.date_surf[-1]
            #     top = self.bg_rect.top + self.space*4
            #     self.show_entry_date(date_surf, top)
            #
            #     file_path = os.path.join(ALL_PATH, 'graphics/chamber_graph/week_graph.png')
            #     top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
            #     self.show_entry_img(file_path, top)
            #


        if self.player.pos_layer == 'lab_api':
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
                # 2페이지 구성 - 그래프 제목
                self.lab_heyhome_graph

                title_text = 'Temperature and Humidity over Time'
                title_surf = self.font.render(title_text, False, 'black')

                top = self.bg_rect.top + self.space * 4
                left = self.bg_rect.left + self.bg_rect.width/2 - title_surf.get_width()/2

                self.display_surface.blit(title_surf, (left, top))

                # 2페이지 구성 - 그래프 이미지
                img = pygame.image.load('../graphics/temperature_humidity_graph.png')
                img = pygame.transform.scale(img, (700, 0.6*700))

                top_img = self.bg_rect.top + self.space * 4 + title_surf.get_height()
                left_img = self.bg_rect.left + self.bg_rect.width/2 - img.get_width()/2

                self.display_surface.blit(img, (left_img, top_img))
            #
            # elif self.index == 2:
            #     date_surf = self.date_surf[self.date_index]
            #     top = self.bg_rect.top + self.space*4
            #     self.show_entry_date(date_surf, top)

                # self.chamber_lux = f'..\graphics\chamber_graph\chamber_lux.png'
                # top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
                # self.show_entry_img(self.chamber_lux, top)

        if self.player.pos_layer == 'grh_api':
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
                # 2페이지 구성 - 그래프 제목
                self.grh_heyhome_graph

                title_text = 'Temperature and Humidity over Time'
                title_surf = self.font.render(title_text, False, 'black')

                top = self.bg_rect.top + self.space * 4
                left = self.bg_rect.left + self.bg_rect.width / 2 - title_surf.get_width() / 2

                self.display_surface.blit(title_surf, (left, top))

                # 2페이지 구성 - 그래프 이미지
                img = pygame.image.load('../graphics/temperature_humidity_graph_grh.png')
                img = pygame.transform.scale(img, (700, 0.6 * 700))

                top_img = self.bg_rect.top + self.space * 4 + title_surf.get_height()
                left_img = self.bg_rect.left + self.bg_rect.width / 2 - img.get_width() / 2

                self.display_surface.blit(img, (left_img, top_img))

            # elif self.index == 2:
            #         date_surf = self.date_surf[self.date_index]
            #         top = self.bg_rect.top + self.space*4
            #         self.show_entry_date(date_surf, top)
            #
            #         # self.chamber_lux = f'..\graphics\chamber_graph\chamber_lux.png'
            #         # top = self.bg_rect.top + self.space*4 + self.date_rect.height + self.space
            #         # self.show_entry_img(self.chamber_lux, top)

        if self.player.pos_layer == 'buan_api':
            if self.index == 0:
                # 1페이지 구성
                # 1페이지 구성 - 제목
                text_surf = 'BUAN weather data'
                title_surf = self.font.render(text_surf, False, 'black')

                left = (self.bg_rect.left + self.bg_rect.width/2) - title_surf.get_width()/2
                top = self.bg_rect.top + self.space * 4

                self.show_field_text(title_surf, left, top)
                
                # 1페이지 구성 - 요소 텍스트 + 기상 데이터
                buan_weather_data = self.get_buan_weather_data
                top = self.bg_rect.top + self.space * 4 + title_surf.get_height() + self.space * 2
                i = 1
                for name, value in buan_weather_data.items():
                    if name != 'updated_time':
                        text_surf = self.font.render(name, False, 'brown')
                        data_surf = self.font.render(value, False, 'black')

                        left = self.bg_rect.left + (i - 1) * (self.bg_rect.width / 3) + self.space*3
                        top_data = self.bg_rect.top + self.space * 4 + title_surf.get_height() + self.space * 2 + text_surf.get_height() + self.space * 2

                        self.show_field_text(text_surf, left, top)
                        self.show_field_text(data_surf, left, top_data)
                        i += 1

            elif self.index == 1:
                # 2페이지 구성
                # 2페이지 구성 - 제목
                text_surf = 'Per-plot soil moisture'
                title_surf = self.font.render(f'{text_surf}kPa', False, 'black')

                left = (self.bg_rect.left + self.bg_rect.width/2) - title_surf.get_width()/2
                top = self.bg_rect.top + self.space * 4

                self.show_field_text(title_surf, left, top)

                # 2페이지 구성 - 필지 텍스트 & 토양수분 데이터
                for i in range(1,9): # 1, 2, 3, 4
                    text_surf = f'Field {i}'
                    field_surf = self.font.render(text_surf, False, 'brown')
                    text_surf_data = self.get_buan_soilmoisture_data[text_surf]
                    data_surf = self.font.render(text_surf_data, False, 'black')

                    if i <= 4:
                        top = self.bg_rect.top + self.space * 4 + title_surf.get_height() + self.space * 2
                        left = self.bg_rect.left + (i - 1) * (self.bg_rect.width / 4)

                        top_data = self.bg_rect.top + self.space * 4 + title_surf.get_height() + self.space * 2 + field_surf.get_height() + self.space * 2
                    else:
                        top = self.bg_rect.top + self.space * 4 + title_surf.get_height() + self.space * 2 + (
                                    self.bg_rect.height - title_surf.get_height()) / 2
                        left = self.bg_rect.left + ((i - 4) - 1) * (self.bg_rect.width / 4)

                        top_data = self.bg_rect.top + self.space * 4 + title_surf.get_height() + self.space * 2 + (
                                    self.bg_rect.height - title_surf.get_height()) / 2 + field_surf.get_height() + self.space * 2

                    self.show_field_text(field_surf, left, top)
                    self.show_field_text(data_surf, left, top_data)

        if self.player.pos_layer == 'aws_lab':
            if self.index == 0:
                # 1페이지 구성
                # 1페이지 구성 - 제목
                text_surf = 'JBNU AWS weather data'
                title_surf = self.font.render(text_surf, False, 'black')

                left = (self.bg_rect.left + self.bg_rect.width / 2) - title_surf.get_width() / 2
                top = self.bg_rect.top + self.space * 4

                self.display_surface.blit(title_surf, (left, top))

                # 1페이지 구성 - 실시간 데이터 텍스트
                aws_df = self.aws_data
                realtime_aws = aws_df.iloc[-1]

                realtime_aws_dic = {'updated_time' : realtime_aws['Time'],
                                    'temp' : realtime_aws['temp'],
                                    'hum' : realtime_aws['hum'],
                                    'wind' : f"{realtime_aws['wind_speed']}({ realtime_aws['wind_dir']})",
                                    'lux' : realtime_aws['lux'],
                                    'rainfall' : realtime_aws['rainfall']}
                i = 0
                for name, value in realtime_aws_dic.items():
                    if name != 'updated_time':
                        text_surf = self.font.render(name, False, 'brown')
                        data_surf = self.font.render(str(value), False, 'black')
                        if name == 'temp' or name == 'hum' or name == 'wind':
                            top = self.bg_rect.top + self.space * 4 + title_surf.get_height() + self.space * 2
                            left = self.bg_rect.left + (i - 1) * (self.bg_rect.width / 3) + (self.bg_rect.width / 3)/2 - text_surf.get_width()/2

                            left_data = self.bg_rect.left + (i - 1) * (self.bg_rect.width / 3) + (self.bg_rect.width / 3)/2 - data_surf.get_width()/2
                            top_data = self.bg_rect.top + self.space * 4 + title_surf.get_height() + self.space * 2 + text_surf.get_height() + self.space * 2


                        if name == 'rainfall' or name == 'lux':
                            if name == 'lux':
                                i = 1

                            print(name, i)
                            top = self.bg_rect.top + self.space * 4 + title_surf.get_height() + self.space * 2 + (self.bg_rect.height - title_surf.get_height())/2
                            left = self.bg_rect.left + (i - 1) * (self.bg_rect.width / 2) + (self.bg_rect.width / 2)/2 - text_surf.get_width()/2

                            left_data = self.bg_rect.left + (i - 1) * (self.bg_rect.width / 2) + (self.bg_rect.width / 2) / 2 - data_surf.get_width() / 2
                            top_data = self.bg_rect.top + self.space * 4 + self.space * 2 + (self.bg_rect.height - title_surf.get_height())/2 + text_surf.get_height() + self.space * 2

                        self.display_surface.blit(text_surf, (left, top))
                        self.display_surface.blit(data_surf, (left_data, top_data))

                    i += 1
                    
                # 1페이지 구성 - 날짜
                date_text = str(realtime_aws['Time']).split('+')[0]
                date_surf = self.font.render(date_text, False, 'black')

                top = self.bg_rect.bottom - date_surf.get_height() - self.space*2
                left = self.bg_rect.right - date_surf.get_width() - self.space*2
                # pygame.draw.rect(self.display_surface, 'red', self.bg_rect)

                self.display_surface.blit(date_surf, (left, top))

                # self.show_field_text(date_surf, text_rect.left, text_rect.top)

            elif self.index == 1:
                # 2페이지 구성
                # 2페이지 구성 - 제목
                title_text = 'Temperature and Humidity over Time'
                title_surf = self.font.render(title_text, False, 'black')

                top = self.bg_rect.top + self.space * 4
                left = self.bg_rect.left + self.bg_rect.width / 2 - title_surf.get_width() / 2

                self.display_surface.blit(title_surf, (left, top))

                # 2페이지 구성 - 그래프 이미지
                img = pygame.image.load('../graphics/aws_temp_hum.png')
                img = pygame.transform.scale(img, (700, 0.6 * 700))

                top_img = self.bg_rect.top + self.space * 4 + title_surf.get_height()
                left_img = self.bg_rect.left + self.bg_rect.width / 2 - img.get_width() / 2

                self.display_surface.blit(img, (left_img, top_img))

            elif self.index == 2:
                title_text = 'Lux over Time'
                title_surf = self.font.render(title_text, False, 'black')

                top = self.bg_rect.top + self.space * 4
                left = self.bg_rect.left + self.bg_rect.width / 2 - title_surf.get_width() / 2

                self.display_surface.blit(title_surf, (left, top))

                # 2페이지 구성 - 그래프 이미지
                img = pygame.image.load('../graphics/aws_lux.png')
                img = pygame.transform.scale(img, (700, 0.6 * 700))

                top_img = self.bg_rect.top + self.space * 4 + title_surf.get_height()
                left_img = self.bg_rect.left + self.bg_rect.width / 2 - img.get_width() / 2

                self.display_surface.blit(img, (left_img, top_img))