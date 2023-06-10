from os import makedirs

from matplotlib import pyplot as plt
from requests import get
from datetime import datetime as dt, timedelta


async def get_weather(city, tomorrow: bool = False):
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    api_of_weather = '352c751a80237a51813f0ae93d864822'
    params = {'APPID': api_of_weather,
              'q': city,
              'units': 'metric',
              'lang': 'ru'}
    result = get(url, params=params).json()
    description = {
        'Clouds': 'skyblue',
        'Rain': 'blue',
        'Clear': 'yellow'
    }
    time_in_city = (dt.now()-timedelta(seconds=10800)) + timedelta(seconds=result['city']['timezone'])
    temperature = {}
    weather = []
    fig = plt.figure()
    if time_in_city.hour < 3 or time_in_city.hour > 20:
        plt.rcParams.update({
            "figure.facecolor": "black",
            "axes.facecolor": "black",
            "savefig.facecolor": "black",
            "axes.edgecolor": "white",
            "axes.labelcolor": "white",
            "xtick.color": "white",
            "ytick.color": "white",
            "grid.color": "white"
        })
        plt.title(f'{city}', color='white')
    else:
        plt.title(f'{city}', color='black')
    plt.xlabel('Время, часы')
    plt.ylabel('Температура, °C')
    if tomorrow is True:
        for i in result['list']:
            if str((time_in_city+timedelta(days=1)).date()) == i['dt_txt'].split(' ')[0]:
                temperature[i['dt_txt'].split(' ')[1][:5:]] = i['main']['temp']
                weather.append(description[i['weather'][0]['main']])
        y = temperature.values()
        x = temperature.keys()
        plt.bar(x, y, color=weather)
        file_name = f'Bar\\{city}\\{(dt.now() + timedelta(days=1)).date()}.png'
        try:
            fig.savefig(file_name, dpi=150)
        except FileNotFoundError:
            makedirs(f'Bar\\{city}')
            fig.savefig(file_name, dpi=150)
        finally:
            return
    elif tomorrow is False:
        for i in result['list']:
            if str(time_in_city.date()) == i['dt_txt'].split(' ')[0]:
                temperature[i['dt_txt'].split(' ')[1][:2:]] = i['main']['temp']
                weather.append(description[i['weather'][0]['main']])
        x = temperature.keys()
        y = temperature.values()
        plt.bar(x, y, color=weather)
        file_name = f'Bar\\{city}\\{dt.now().date()}.png'
        try:
            fig.savefig(file_name, dpi=150)
        except FileNotFoundError:
            makedirs(f'Bar\\{city}')
            fig.savefig(file_name, dpi=150)
        finally:
            return
