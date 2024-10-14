import json
import urllib.request

import numpy as np
from PIL import Image
import io

import requests
import pygame
from settings import *
import pandas as pd
from datetime import datetime, timedelta

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from matplotlib.dates import DateFormatter

import os

class Get_data:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        #
        self.my_font = pygame.font.SysFont(None, 50)
        self.text_x_pos = 0
        self.text_y_pos = 0

        self.lab_display_dt = 0
        self.gh_display_dt = 0
        self.chamber_display_dt = 0

        self.lab_text = {'day_time': '--', 'day_temp' : -99, 'day_hum' : -99}
        self.gh_text = {'day_time': '--', 'day_temp' : -99, 'day_hum' : -99}
        self.chamber_text = {'Time': '--', 'temp' : -99, 'hum' : -99, 'lux': -99}

        self.livedata_mini_chamber = False
        self.mini_chamber_graph = False

    # 헤이홈 연구실 데이터 
    def get_lab_data(self):
        url = 'http://web01.taegon.kr:7600/recent'

        response = requests.get(url)
        output = {}

        print(response.status_code)
        if response.status_code == 200:
            result = response.content
            dic_lab = json.loads(result.decode('utf-8'))
            realtime_lab = dic_lab['lab']

            output['day_time'] = realtime_lab['timestamp']
            output['day_temp'] = realtime_lab['temperature']
            output['day_hum'] = realtime_lab['humidity']

            # return output
            return [output['day_temp'], output['day_hum'], '--']

    # 헤이홈 온실 데이터
    def get_gh_data(self):
        url = 'http://web01.taegon.kr:7600/recent'
        print("get_lab_data")

        response = requests.get(url)
        output = {}

        print(response.status_code)
        if response.status_code == 200:
            result = response.content
            dic_lab = json.loads(result.decode('utf-8'))
            realtime_lab = dic_lab['grh']

            output['day_time'] = realtime_lab['timestamp']
            output['day_temp'] = realtime_lab['temperature']
            output['day_hum'] = realtime_lab['humidity']

            # return output
            return [output['day_temp'], output['day_hum'], '--']
        
    # 헤이홈 온실 데이터 정리 (화면에 표시되는 형식으로)
    def gh_display(self,dt):
        self.gh_display_dt += dt
        if self.gh_display_dt < 1 and self.gh_text["day_time"] == '--':
            self.gh_text = self.get_gh_data()

        if self.gh_display_dt >= 10:
            self.gh_text = self.get_gh_data()
            self.gh_display_dt = 0
        else:
            pass

        self.my_text = self.my_font.render(
            f'{self.gh_text["day_time"]} - {self.gh_text["day_temp"]:.1f}C, {self.gh_text["day_hum"]:.1f}%', True,
            (255, 255, 255))
        self.display_surface.blit(self.my_text, [200, 500])

    # 헤이홈 연구실 데이터 정리 (화면에 표시되는 형식으로)
    def lab_display(self, dt):
        self.lab_display_dt += dt
        if self.lab_display_dt < 1 and self.lab_text["day_time"] == '--':
            self.lab_text = self.get_lab_data()

        if self.lab_display_dt >= 10:
            self.lab_text = self.get_lab_data()
            self.lab_display_dt = 0
        else:
            pass

        self.my_text = self.my_font.render(f'lab : {self.lab_text["day_time"]} - {self.lab_text["day_temp"]:.1f}C, {self.lab_text["day_hum"]:.1f}%', True, (0, 0, 0))
        self.display_surface.blit(self.my_text, [200,200])

    # 미니챔버 데이터 가져오기
    def chamber_data(self):
        for i in range(1,3):
            url = f'https://api.thingspeak.com/channels/1999884/fields/{i}.json?api_key=TYCQQ3CFQME0PITO&results=2'

            output = {}
            response = requests.get(url)
            if response.status_code == 200:
                self.livedata_mini_chamber = True
                if i == 1:
                    df = pd.DataFrame(response.json()['feeds'])
                    df.rename(columns={'field1': 'temp'}, inplace=True)

                elif i == 2:
                    df['hum'] = response.json()['feeds'][0]['field2']

        df = df.iloc[0:1]
        df.insert(loc=0, column='Time', value=df['created_at'].apply(lambda x: x.split('T')[1].split('Z')[0]))
        df.insert(loc=0, column='Date', value=df['created_at'].apply(lambda x: x.split('T')[0]))

        output['Time'] = df['created_at'].apply(lambda x: x.split('T')[1].split('Z')[0])
        output['Time'] = output['Time'].values + pd.Timedelta(hours=9)
        output['Time'] = str(output['Time']).split(' ')[-1].split("'")[0]
        output['Date'] = df['created_at'].apply(lambda x: x.split('T')[0]).values[0]

        output['temp'] = str(int(float(df['temp'].values[0])))
        output['hum'] = str(int(float(df['hum'].values[0])))
        output['lux'] = 'None'

        # 실시간 데이터가 반영되지 않을때 (과거 데이터를 수신할 때)
        set_time = datetime.strptime(output['Time'], '%H:%M:%S')
        if (datetime.now() - set_time).seconds/60 > 5 and output['Date'] != datetime.now().strftime('%Y-%m-%d'):
            self.livedata_mini_chamber = False

        return {'Date' : output['Date'], 'Time' : output['Time'], 'temp' : output['temp'], 'hum' : output['hum'], 'lux' : output['lux']}


    # def get_chamber_data(self):
    #     url = 'https://api.thingspeak.com/channels/1999883/feeds.json?api_key=XP1R5CVUPVXTNJT0&'
    #
    #     output = {}
    #     response = requests.get(url + 'results=5000')
    #     if response.status_code == 200:
    #         df = pd.DataFrame(response.json()['feeds'])
    #         df.rename(columns={'field1': 'temp', 'field2': 'hum', 'field3':'lux'}, inplace=True)
    #         df.insert(loc=0, column='Time', value=df['created_at'][0].split('T')[1].split('Z')[0])
    #         df.drop(columns=['created_at','entry_id','field4'], inplace=True)
    #
    #         df['Time'] = pd.to_datetime(df['Time']) + pd.Timedelta(hours=9)
    #         df['Time'] = df['Time'].dt.strftime('%H:%M:%S')
    #         output['Time'] = df['Time'].values[0]
    #         output['temp'] = df['temp'].values[0]
    #         output['hum'] = df['hum'].values[0]
    #         output['lux'] = df['lux'].values[0]
    #     return [output['temp'], output['hum'], output['lux']]

    def chamber_display(self,dt):
        self.chamber_display_dt += dt

        if self.chamber_display_dt < 1 and self.chamber_text["Time"][0] == '--':
            self.chamber_text = self.chamber_data()
            # self.chamber_text['Time'] = data['Time']
            # self.chamber_text['temp'] = data['temp']
            # self.chamber_text['hum'] = data['hum']
        if self.chamber_display_dt >= 10:
            self.chamber_text = self.chamber_data()
            self.chamber_display_dt = 0
        else:
            pass

        return [self.chamber_text['temp'], self.chamber_text['hum'], self.chamber_text['lux']]

    def get_chamber_graph(self, date, y):
        print('run get_chamber_graph')
        url = f"https://raw.githubusercontent.com/Yanghuiwon22/chamber_data/main/outpugraph/{date}_{y}.png"
        try:
            response = urllib.request.urlopen(url)

            if response.getcode() == 200:
                self.mini_chamber_graph = True
                print(f'success {y}')
                data = response.read()
                image = Image.open(io.BytesIO(data))
                print(image)
                file_path = os.path.join(ALL_PATH, 'graphics/chamber_graph/chamber_{y}.png')
                print(file_path)
                image.save(file_path)  # savefig 대신 save 사용
        except:
            self.mini_chamber_graph = False

    def get_week_data(self):
        date = datetime.now()
        date = date.date()

        date_range = [date - timedelta(days=x) for x in range(7)]
        date_range.sort()

        df_all = pd.DataFrame()

        try:
            for url_date in date_range:
                url = f'https://raw.githubusercontent.com/Yanghuiwon22/chamber_data/main/output/csv/{url_date}.csv'
                response = urllib.request.urlopen(url)

                if response.getcode() == 200:
                    data = response.read().decode('utf-8')
                    df = pd.read_csv(io.StringIO(data))
                    df_all = pd.concat([df_all, df])
                    df_all.reset_index(drop=True)

            # url = 'https://api.thingspeak.com/channels/1999883/feeds.json?api_key=XP1R5CVUPVXTNJT0&'
            #
            # output = {}
            # response = requests.get(url + 'results=5000')
            # if response.status_code == 200:
            #     df = pd.DataFrame(response.json()['feeds'])
            #     df.rename(columns={'field1': 'temp', 'field2': 'hum', 'field3':'lux'}, inplace=True)
            #     df.insert(loc=0, column='Time', value=df['created_at'][0].split('T')[1].split('Z')[0])
            #     df.drop(columns=['created_at','entry_id','field4'], inplace=True)
            #
            #     df['Time'] = pd.to_datetime(df['Time']) + pd.Timedelta(hours=9)
            #     df['Time'] = df['Time'].dt.strftime('%H:%M:%S')
            #     output['Time'] = df['Time'].values[0]
            #     output['temp'] = df['temp'].values[0]
            #     output['hum'] = df['hum'].values[0]
            #     output['lux'] = df['lux'].values[0]
            # return [output['temp'], output['hum'], output['lux']]
            df_all.to_csv('./df_all.csv')
        except:
            pass

    def draw_week_data(self):
        try:
            df = pd.read_csv('./df_all.csv')
        except:
            df = pd.read_csv('./fake_df.csv')

        df = df[['Date&Time','Time', 'temp', 'hum', 'lux']].dropna()
        df['Date&Time'] = pd.to_datetime(df['Date&Time'])

        fig, ax1 = plt.subplots(figsize=(10, 6))
        color_lux = 'y'
        sns.lineplot(x=df['Date&Time'], y=df['lux'], ax=ax1, c=color_lux, lw=2, label='lux')
        for s in ["left", "right", "top"]:
            ax1.spines[s].set_visible(False)
        ax1.spines['bottom'].set_linewidth(3)
        ax1.grid(axis="y")

        date_format = DateFormatter("%Y-%m-%d")
        ax1.xaxis.set_major_formatter(date_format)
        ax1.xaxis.set_major_locator(plt.MaxNLocator(7))  # X 축에 표시할 눈금 수 조절

        plt.tight_layout()
        # plt.show()
        plt.savefig(os.path.join(ALL_PATH, f'graphics/chamber_graph/week_graph_lux.png'))

    def draw_week_graph_t_h(self):
        df = pd.read_csv(os.path.join(ALL_PATH, 'fake_df.csv'))
        df = df[['Date&Time', 'temp', 'hum', 'lux']].dropna()
        df['Date&Time'] = pd.to_datetime(df['Date&Time'])
        color_temp = 'r'
        color_hum = 'b'
        color_lux = 'y'


        fig, ax1 = plt.subplots(figsize=(10, 6))

        sns.lineplot(x=df['Date&Time'], y=df['temp'], ax=ax1, c=color_temp, lw=2, label='temp')
        ax2 = ax1.twinx()
        sns.lineplot(x=df['Date&Time'], y=df['hum'], ax=ax2, c=color_hum, lw=2, label='hum', legend=False)

        for s in ["left", "right", "top"]:
            ax1.spines[s].set_visible(False)
            ax2.spines[s].set_visible(False)
        ax1.spines['bottom'].set_linewidth(3)

        ax1.grid(axis="y")
        ax1.xaxis.set_major_locator(plt.MaxNLocator(7))  # X 축에 표시할 눈금 수 조절

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        lines = lines1 + lines2
        labels = labels1 + labels2
        ax1.legend(lines, labels, loc='upper right')

        plt.tight_layout()
        plt.savefig(os.path.join(ALL_PATH, f'graphics/chamber_graph/week_graph_t_h.png'))

    def draw_week_data(self):
        df = pd.read_csv('fake_df.csv')

        df = df[['Date&Time','Time', 'temp', 'hum', 'lux']].dropna()
        # df['Date'] = df['Date&Time'].str.split(' ').str[0]
        df['Date&Time'] = pd.to_datetime(df['Date&Time'])

        fig, ax1 = plt.subplots(figsize=(10, 6))
        color_lux = 'y'
        sns.lineplot(x=df['Date&Time'], y=df['lux'], ax=ax1, c=color_lux, lw=2, label='lux')
        for s in ["left", "right", "top"]:
            ax1.spines[s].set_visible(False)
        ax1.spines['bottom'].set_linewidth(3)
        ax1.grid(axis="y")

        date_format = DateFormatter("%Y-%m-%d")

        ax1.xaxis.set_major_formatter(date_format)
        ax1.xaxis.set_major_locator(plt.MaxNLocator(7))  # X 축에 표시할 눈금 수 조절

        plt.tight_layout()
        # plt.show()
        plt.savefig(os.path.join(ALL_PATH, f'graphics/chamber_graph/week_graph.png'))






#
if __name__ == '__main__':
    data = Get_data()
    data.chamber_data()
#     # data.draw_week_data()
#     data.get_chamber_graph('2024-05-28', 't_h')
#     data.get_chamber_graph('2024-05-28', 'lux')
#     # data.get_chamber_data()
#     data.draw_week_graph_t_h()
