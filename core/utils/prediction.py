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
        'Clouds': 'cyan',
        'Rain': 'blue',
        'Clear': 'yellow'
    }
    temperature = {}
    weather = []
    fig = plt.figure()
    plt.xlabel('Время')
    plt.ylabel('Температура')
    plt.title(city)
    if tomorrow is True:
        for i in result['list']:
            if str((dt.now()+timedelta(days=1)).date()) == i['dt_txt'].split(' ')[0]:
                temperature[i['dt_txt'].split(' ')[1][:2:]] = i['main']['temp']
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
            if str(dt.now().date()) == i['dt_txt'].split(' ')[0]:
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
