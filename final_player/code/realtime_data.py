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
        self.lab_error = False

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


    def get_grh_heyhome(self):
        url = 'http://web01.taegon.kr:7600/today'

        response = requests.get(url)

        if response.status_code == 200:
            result = response.content
            dic_lab = json.loads(result.decode('utf-8'))['grh']
            df = pd.DataFrame(dic_lab)
            df['hour'] = df['time'].apply(lambda x: x.split(':')[0])

            print(df)

            fig, ax1 = plt.subplots(figsize=(10, 6))

            # 첫 번째 Y축 (온도)
            ax1.plot(df['time'], df['temp'], color='red', marker='o', label='Temperature (°C)')
            ax1.set_xlabel('Time', fontweight='bold', fontsize=20)
            ax1.set_ylabel('Temperature (°C)', color='red', fontweight='bold', fontsize=20)
            ax1.tick_params(axis='y', labelcolor='red')

            ax1.set_xticks(df['time'][::6])
            ax1.set_xticklabels(df['time'][::6], rotation=45, fontweight='bold', fontsize=20)  # X축 레이블 회전

            ax1.set_yticks(df['temp'])
            ax1.set_yticklabels(df['temp'], rotation=45, fontweight='bold', fontsize=20)  # X축 레이블 회전

            # 두 번째 Y축 (습도)
            ax2 = ax1.twinx()  # 두 번째 Y축 추가
            ax2.plot(df['time'], df['humid'], color='blue', marker='o', label='Humidity (%)')
            ax2.set_ylabel('Humidity (%)', color='blue', fontweight='bold', fontsize=20)

            ax2.set_yticks(df['humid'])
            ax2.set_yticklabels(df['humid'], fontsize=15)  # X축 레이블 회전
            ax2.tick_params(axis='y', labelcolor='blue')

            # 그래프 타이틀 설정 및 레이아웃 조정
            fig.tight_layout()
            plt.savefig('../graphics/temperature_humidity_graph_grh.png')


    def get_lab_heyhome(self):
        url = 'http://web01.taegon.kr:7600/today'

        response = requests.get(url)

        if response.status_code == 200:
            result = response.content
            dic_lab = json.loads(result.decode('utf-8'))['lab']
            df = pd.DataFrame(dic_lab)
            df['hour'] = df['time'].apply(lambda x: x.split(':')[0])

            print(df)

            fig, ax1 = plt.subplots(figsize=(10, 6))

            # 첫 번째 Y축 (온도)
            ax1.plot(df['time'], df['temp'], color='red', marker='o', label='Temperature (°C)')
            ax1.set_xlabel('Time', fontweight='bold', fontsize=20)
            ax1.set_ylabel('Temperature (°C)', color='red', fontweight='bold', fontsize=20)
            ax1.tick_params(axis='y', labelcolor='red')

            ax1.set_xticks(df['time'][::6])
            ax1.set_xticklabels(df['time'][::6], rotation=45, fontweight='bold', fontsize=20)  # X축 레이블 회전

            ax1.set_yticks(df['temp'])
            ax1.set_yticklabels(df['temp'], rotation=45, fontweight='bold', fontsize=20)  # X축 레이블 회전

            # 두 번째 Y축 (습도)
            ax2 = ax1.twinx()  # 두 번째 Y축 추가
            ax2.plot(df['time'], df['humid'], color='blue', marker='o', label='Humidity (%)')
            ax2.set_ylabel('Humidity (%)', color='blue', fontweight='bold', fontsize=20)

            ax2.set_yticks(df['humid'])
            ax2.set_yticklabels(df['humid'], fontsize=15)  # X축 레이블 회전

            ax2.tick_params(axis='y', labelcolor='blue')

            # 그래프 타이틀 설정 및 레이아웃 조정
            fig.tight_layout()
            plt.savefig('../graphics/temperature_humidity_graph.png')
        # return df

    def get_buan_soilmoisture_data(self):
        url = 'http://web01.taegon.kr:7500/api/zentra/data/plot'

        response = requests.get(url)
        output = {}


        if response.status_code == 200:
            result = response.content
            data = json.loads(result.decode('utf-8'))
            print(type(data))

            # realtime_lab = dic_lab['grh']

            output['Field 1'] = str(data['plot1'][-1])
            output['Field 2'] = str(data['plot2'][-1])
            output['Field 3'] = str(data['plot3'][-1])
            output['Field 4'] = str(data['plot4'][-1])
            output['Field 5'] = str(data['plot5'][-1])
            output['Field 6'] = str(data['plot6'][-1])
            output['Field 7'] = str(data['plot7'][-1])
            output['Field 8'] = str(data['plot8'][-1])

            return output

    def get_buan_weather_data(self):
        url = 'http://web01.taegon.kr:7500/weather_now/buan'
        response = requests.get(url)
        output = {}
        output_dic = {}

        if response.status_code == 200:
            result = response.content
            data = json.loads(result.decode('utf-8'))

            try:
                now_time = data.split(',')[0]
                ta = data.split(',')[1]
                ws = data.split(',')[2]
                wd = data.split(',')[5]
                ww = data.split(',')[6]

                for name, value in {'updated_time': now_time, 'temperature': ta, 'wind power': ws, 'wind direction': ww, 'weather_status':wd}.items():

                    value = value.split('": ')[-1]
                    value = value.replace('"', '')

                    output_dic[name] = value

                output['updated_time'] = output_dic['updated_time']
                output['temperature'] = output_dic['temperature']
                output['wind(direction)'] = f"{output_dic['wind power']}({output_dic['wind direction']})"
                output['weather'] = output_dic['weather_status']

            except:
                output['updated_time'] = 'YYYY-mm-DD HH:MM'
                output['temperature'] = '--'
                output['wind(direction)'] = '--m/s(-)'
                output['weather'] = '--'

        return output

    # 헤이홈 온실 데이터
    def get_gh_data(self):
        url = 'http://web01.taegon.kr:7600/recent'

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
        for i in [1, 2, 4]:
            url = f'https://api.thingspeak.com/channels/1999884/fields/{i}.json?api_key=TYCQQ3CFQME0PITO&results=2'

            output = {}
            response = requests.get(url)
            if response.status_code == 200:
                self.livedata_mini_chamber = False
                if i == 1:
                    df = pd.DataFrame(response.json()['feeds'])
                    df.rename(columns={'field1': 'temp'}, inplace=True)

                elif i == 2:
                    df['hum'] = response.json()['feeds'][0]['field2']

                elif i == 4:
                    df['lux'] = response.json()['feeds'][0]['field4']

        df = df.iloc[0:1]
        df.insert(loc=0, column='Time', value=df['created_at'].apply(lambda x: x.split('T')[1].split('Z')[0]))
        df.insert(loc=0, column='Date', value=df['created_at'].apply(lambda x: x.split('T')[0]))

        output['Time'] = df['created_at'].apply(lambda x: x.split('T')[1].split('Z')[0])
        output['Time'] = output['Time'].values + pd.Timedelta(hours=9)
        output['Time'] = str(output['Time']).split(' ')[-1].split("'")[0]
        output['Date'] = df['created_at'].apply(lambda x: x.split('T')[0]).values[0]

        output['temp'] = str(int(float(df['temp'].values[0])))
        output['hum'] = str(int(float(df['hum'].values[0])))
        output['lux'] = str(int(float(df['lux'].values[0])))

        # 실시간 데이터가 반영되지 않을때 (과거 데이터를 수신할 때)
        set_time = datetime.strptime(output['Time'], '%H:%M:%S')
        if (datetime.now() - set_time).seconds/60 > 5 and output['Date'] != datetime.now().strftime('%Y-%m-%d'):
            self.livedata_mini_chamber = False

        return {'Date' : output['Date'], 'Time' : output['Time'], 'temp': output['temp'], 'hum' : output['hum'], 'lux' : output['lux']}


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


    def aws_data(self):
        df = pd.DataFrame()
        for i in range(1,8):  # 수정
            url = 'https://thingspeak.mathworks.com/channels/2328695/field/'
            url += f'{i}.json'
            response = requests.get(url)

            if response.status_code == 200:
                result = response.json()['feeds']

                result_df = pd.DataFrame(result)
                df[f'field{i}'] = result_df['field' + str(i)]

        df = df.rename(columns={'field1': 'temp', 'field2': 'hum', 'field3': 'lux', 'field4': 'wind_dir', 'field5': 'wind_speed', 'field6': 'rainfall', 'field7': 'battery_power'})
        df.insert(0, 'Time', pd.to_datetime(result_df['created_at']) + pd.Timedelta(hours=9))
        df = df.iloc[-30:]

        # df['time'] = df['Time'].astype(str).apply(lambda x: x.split(' ')[1].split('+')[0])
        df['time'] = pd.to_datetime(df['Time'].astype(str).apply(lambda x: x.split(' ')[1].split('+')[0]),
                                    format='%H:%M:%S').dt.strftime('%H:%M:%S')

        df['temp'] = df['temp'].astype(float)
        df['hum'] = df['hum'].astype(float)
        print(df)
        ############################ 그래프 그리기
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # 첫 번째 Y축 (온도)
        ax1.plot(df['time'], df['temp'], color='red', marker='o', label='Temperature (°C)')
        ax1.set_xlabel('time', fontweight='bold', fontsize=20)
        ax1.set_ylabel('Temperature (°C)', color='red', fontweight='bold', fontsize=20)
        ax1.tick_params(axis='y', labelcolor='red')

        ax1.set_xticks(df['time'][::6])
        ax1.set_yticks(np.arange(-15, 51, 10))

        ax1.set_xticklabels(df['time'][::6], fontweight='bold', fontsize=15)  # X축 레이블 회전

        # 두 번째 Y축 (습도)
        ax2 = ax1.twinx()  # 두 번째 Y축 추가
        ax2.plot(df['time'], df['hum'], color='blue', marker='o', label='Humidity (%)')
        ax2.set_ylabel('Humidity (%)', color='blue', fontweight='bold', fontsize=20)

        ax2.set_yticks(np.arange(0, 101, 10))

        ax2.tick_params(axis='y', labelcolor='blue')

        # 그래프 타이틀 설정 및 레이아웃 조정
        fig.tight_layout()
        plt.savefig('../graphics/aws_temp_hum.png')


        # lux
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # 첫 번째 Y축 (온도)
        ax1.plot(df['time'], df['lux'], color='green', marker='o', label='Lux')
        ax1.set_xlabel('time', fontweight='bold', fontsize=20)
        ax1.set_ylabel('Temperature (°C)', color='red', fontweight='bold', fontsize=20)
        ax1.tick_params(axis='y', labelcolor='red')

        ax1.set_xticks(df['time'][::6])
        ax1.set_yticks(np.arange(-15, 51, 10))

        ax1.set_xticklabels(df['time'][::6], fontweight='bold', fontsize=15)  # X축 레이블 회전

        # 두 번째 Y축 (습도)
        ax2 = ax1.twinx()  # 두 번째 Y축 추가
        ax2.plot(df['time'], df['hum'], color='blue', marker='o', label='Humidity (%)')
        ax2.set_ylabel('Humidity (%)', color='blue', fontweight='bold', fontsize=20)

        ax2.set_yticks(np.arange(0, 101, 10))

        ax2.tick_params(axis='y', labelcolor='blue')

        return df

if __name__ == '__main__':
    data = Get_data()
    # data.get_buan_soilmoisture_data()
    # data.get_buan_weather_data()
    data.aws_data()
#     # data.draw_week_data()
#     data.get_chamber_graph('2024-05-28', 't_h')
#     data.get_chamber_graph('2024-05-28', 'lux')
#     # data.get_chamber_data()
#     data.draw_week_graph_t_h()
