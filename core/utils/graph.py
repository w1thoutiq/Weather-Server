import os
import warnings

from datetime import datetime as dt

from core.utils.session_db import create_session
from core.utils.simple_func import get_weather
from core.utils.connect_db import AlertGraph, User
import matplotlib.pyplot as plt


def save_data():
    with create_session() as db:
        for ct in get_city_set():
            temp = [i if i is not None else 'None' for i in db.query(
                AlertGraph.am12,
                AlertGraph.am1,
                AlertGraph.am2,
                AlertGraph.am3,
                AlertGraph.am4,
                AlertGraph.am5,
                AlertGraph.am6,
                AlertGraph.am7,
                AlertGraph.am8,
                AlertGraph.am9,
                AlertGraph.am10,
                AlertGraph.am11,
                AlertGraph.pm12,
                AlertGraph.pm1,
                AlertGraph.pm2,
                AlertGraph.pm3,
                AlertGraph.pm4,
                AlertGraph.pm5,
                AlertGraph.pm6,
                AlertGraph.pm7,
                AlertGraph.pm8,
                AlertGraph.pm9,
                AlertGraph.pm10,
                AlertGraph.pm11
            ).where(AlertGraph.city == str(ct)).all()[0]]
            y = []
            while True:
                try:
                    temp.remove('None')
                except Exception as e:
                    e.__str__()
                    break
            y.extend(temp)
            x = list(range(len(y)))
            try:
                file_name = f'Graph\\{ct}\\{dt.now().date()}.png'
                os.mkdir(f'Graph\\{ct}\\')
                fig = plt.figure()
                plt.plot(x, y)
                fig.savefig(file_name, dpi=150)
            except FileExistsError:
                warnings.simplefilter("ignore", UserWarning)
                figure = plt.figure()
                plt.plot(x, y)
                figure.savefig(file_name, dpi=150)


def admin_graph(ct: str):
    with create_session() as db:
        temp = [i if i is not None else 'None' for i in db.query(
            AlertGraph.am12,
            AlertGraph.am1,
            AlertGraph.am2,
            AlertGraph.am3,
            AlertGraph.am4,
            AlertGraph.am5,
            AlertGraph.am6,
            AlertGraph.am7,
            AlertGraph.am8,
            AlertGraph.am9,
            AlertGraph.am10,
            AlertGraph.am11,
            AlertGraph.pm12,
            AlertGraph.pm1,
            AlertGraph.pm2,
            AlertGraph.pm3,
            AlertGraph.pm4,
            AlertGraph.pm5,
            AlertGraph.pm6,
            AlertGraph.pm7,
            AlertGraph.pm8,
            AlertGraph.pm9,
            AlertGraph.pm10,
            AlertGraph.pm11
        ).where(AlertGraph.city == ct).all()[0]]
        y = []
        while True:
            try:
                temp.remove('None')
            except ValueError:
                break
        y.extend(temp)
        x = list(range(len(y)))
        try:
            file_name = f'Graph\\{ct}\\{dt.now().date()}.png'
            os.mkdir(f'Graph\\{ct}\\')
            fig = plt.figure()
            plt.plot(x, y)
            fig.savefig(file_name, dpi=150)
        except FileExistsError:
            warnings.simplefilter("ignore", UserWarning)
            figure = plt.figure()
            plt.plot(x, y)
            figure.savefig(file_name, dpi=150)


def get_city_set():
    city_set = set()
    with create_session() as db:
        city_lst = list(ctt[0].split(', ') for ctt in db.query(User.city).all())
        for ct in city_lst:
            for c in ct:
                city_set.add(c)
    try:
        city_set.remove('')
    except KeyError:
        pass
    return city_set


time_of_dict = {
    '0': AlertGraph.am12,
    '1': AlertGraph.am1,
    '2': AlertGraph.am2,
    '3': AlertGraph.am3,
    '4': AlertGraph.am4,
    '5': AlertGraph.am5,
    '6': AlertGraph.am6,
    '7': AlertGraph.am7,
    '8': AlertGraph.am8,
    '9': AlertGraph.am9,
    '10': AlertGraph.am10,
    '11': AlertGraph.am11,
    '12': AlertGraph.pm12,
    '13': AlertGraph.pm1,
    '14': AlertGraph.pm2,
    '15': AlertGraph.pm3,
    '16': AlertGraph.pm4,
    '17': AlertGraph.pm5,
    '18': AlertGraph.pm6,
    '19': AlertGraph.pm7,
    '20': AlertGraph.pm8,
    '21': AlertGraph.pm9,
    '22': AlertGraph.pm10,
    '23': AlertGraph.pm11
}


def graph():
    time = str(dt.now().hour)
    with create_session() as db:
        for ct in get_city_set():
            if db.query(AlertGraph).where(AlertGraph.city == str(ct)).first() is None:
                db.add(AlertGraph(city=ct))
                db.commit()
            db.query(AlertGraph).where(AlertGraph.city == str(ct)).update(
                {time_of_dict[time]: get_weather(ct, for_graph=True)}
            )
            db.commit()
        db.commit()


async def temperature_graph():
    with create_session() as db:
        db.query(AlertGraph).delete()
        db.commit()
        for ct in get_city_set():
            try:
                db.add(AlertGraph(
                    city=ct
                ))
                db.commit()
            except Exception as e:
                print(e)
        db.commit()
