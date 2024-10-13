import requests
import pandas as pd
import pygame
import matplotlib.pyplot as plt
import seaborn as sns

def get_data(date):
    date = '2024-05-23'
    url = f'http://web01.taegon.kr:7600/history/{date}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame([])
        # df['date'] = data['th1_date']
        # df['hour'] = df['date'].str.split(':').str[0]
        # df['temp'] = data['th1_temp']
        # df['hum'] = data['th1_humid']

        df['date'] = data['grh_date']
        df['hour'] = df['date'].str.split(':').str[0]
        df['temp'] = data['grh_temp']
        df['hum'] = data['grh_humid']

        return df
    else:
        print('fail')

def draw_graph(df, date):
    ax = sns.lineplot(data=df, x='hour', y='temp')
    ax.set_ylabel('temp')
    ax.set_xlabel('date')
    ax.set_title(f'{date}-temp graph')
    plt.show()
    # plt.savefig(f'output/graph/{date}_{y}.png')

def main():
    date = '2024-05-23'
    data = get_data(date)
    draw_graph(data, date)


if __name__ == '__main__':
    main()