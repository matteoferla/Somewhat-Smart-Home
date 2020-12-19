# Code from thermometer pi with bindicator in living room
# 192.168.0.69
# "companion_pi"

"""



$ sudo nano /etc/systemd/system/scheduled.service

[Unit]
Description=Run python scheduler
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/
ExecStart=python3 /home/pi/scheduled_tasks.py
Restart=always

[Install]
WantedBy=multi-user.target
"""

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from functools import partial
from datetime import datetime, timedelta
import digitalio
import board
import time

# =============================================================================================================================

scheduler = BlockingScheduler()


# =============================================================================================================================

def binmaster(pin, weekday=3):
    while datetime.now().weekday() == weekday:
        binflasher(pin)


def binflasher(pin, tempo=0.5):
    with digitalio.DigitalInOut(pin) as led:
        led.direction = digitalio.Direction.OUTPUT
        led.value = True
        time.sleep(tempo)
        led.value = False
        time.sleep(tempo)


bluepin = board.D24
greenpin = board.D23
for pin in (bluepin, greenpin):  # check they dont raise errors.
    with digitalio.DigitalInOut(bluepin) as led:
        led.direction = digitalio.Direction.OUTPUT
        led.value = False

bluebinmaster = partial(binmaster, pin=bluepin)
greenbinmaster = partial(binmaster, pin=greenpin)

# next green
greenday = datetime.fromisoformat('2020-12-17 16:30:00')
while greenday < datetime.now():
    greenday += timedelta(days=14)

# next green
blueday = datetime.fromisoformat('2020-12-24 16:30:00')
while blueday < datetime.now():
    blueday += timedelta(days=14)

print(f'Greenday: {greenday}')
print(f'Blueday: {blueday}')

for i in range(10):
    if greenday < blueday:
        binflasher(greenpin, 2)
    else:
        binflasher(bluepin, 2)

# -----------------------------------------------------------------------------------------------------------------------------

scheduler.add_job(greenbinmaster, 'interval', weeks=2, start_date=greenday.isoformat())
scheduler.add_job(bluebinmaster, 'interval', weeks=2, start_date=blueday.isoformat())

# =============================================================================================================================

import requests, os
import datetime as dt
from typing import Optional


class HomieAPI:

    def __init__(self, base_url='http://0.0.0.0:8000', key='ERROR'):
        """

        :param base_url:
        :param key:
        """
        assert 'http' in base_url, 'Please add http:// or https://'
        self.base_url = base_url
        self.key = key

    def read(self, delta: int = 7):
        reply = requests.get(f'{self.base_url}/read', {'delta': delta})
        return self.get_json(reply)

    def store(self,
              sensor: str,
              filename: str,
              datetime: Optional[dt.datetime] = None):
        isodate = self.isodatify(datetime)
        extension = os.path.splitext(filename)[1]
        reply = requests.post(f'{self.base_url}/store', {'key': self.key,
                                                         'extension': extension,
                                                         'datetime': isodate,
                                                         'sensor': sensor},
                              files={'photo': open(filename, 'rb')}
                              )
        return self.get_json(reply)

    def isodatify(self, datetime):
        if datetime is None:
            return dt.datetime.now().isoformat()
        elif isinstance(datetime, str):
            return datetime
        elif isinstance(datetime, dt.datetime):
            return datetime.isoformat()
        else:
            raise ValueError

    def record(self, sensor: str, value: float, datetime: Optional[dt.datetime] = None):
        """
        >>> homie.record(sensor='test:A', value=34)

        :param sensor:
        :param value:
        :return:
        """
        isodate = self.isodatify(datetime)
        reply = requests.get(f'{self.base_url}/record', {'key': self.key,
                                                         'datetime': isodate,
                                                         'sensor': sensor,
                                                         'value': value})
        return self.get_json(reply)

    def get_json(self, reply):
        if reply.status_code != 200:
            raise ValueError(reply.text)
        else:
            return reply.json()

    def define(self, **definitions):
        """
        >>> homie.define(sensor='test:A',
        >>>     model='testathon3000',
        >>>     location='localhosted',
        >>>     unit='°C',
        >>>     graph_color='#c0c0c0',
        >>>     dashed=False,
        >>>     axis='hundred')

        sensor: str - Name of sensor
        model: str - sensor model
        location: str - location of the sensor
        unit: str - degrees
        graph_color: str - hex color for css
        dashed: bool - set to False. Is value for internet?
        axis: str - xaxis1 is 'hundred' (degrees, percentage)
        """
        reply = requests.get(f'{self.base_url}/define', {'key': self.key, **definitions})
        return self.get_json(reply)


# -----------------------------------------------------------------------------------------------------------------------------

homie = HomieAPI(base_url='http://192.168.0.75:8000', key='properbaltic')

# =============================================================================================================================

# https://github.com/matteoferla/Raspberry-Pi-irrigator/blob/master/models.py
from datetime import datetime
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import Adafruit_DHT
import adafruit_dht
from collections import namedtuple

# DHT = namedtuple('DHT', ['humidity', 'temperature'])

Base = declarative_base()


class Measurement(Base):
    """
    The table containing the measurements.
    """
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=True), unique=True, nullable=False)
    temperature = db.Column(db.Float, unique=False, nullable=False)
    humidity = db.Column(db.Float, unique=False, nullable=False)


# -----------------------------------------------------------------------------------------------------------------------------


engine = db.create_engine('sqlite://///home/pi/thermo/temperature.sqlite')
Session = sessionmaker()
session = Session(bind=engine)
Base.metadata.create_all(engine)


# -----------------------------------------------------------------------------------------------------------------------------

def sense():
    # dht = DHT(*Adafruit_DHT.read(22, 4))
    dht = adafruit_dht.DHT22(board.D4)
    if dht.temperature is None:
        return sense()
    datum = Measurement(datetime=datetime.now(),
                        temperature=dht.temperature,
                        humidity=dht.humidity)

    session.add(datum)
    session.commit()
    homie.record(sensor='livingroom:temperature', value=datum.temperature, datetime=datum.datetime)
    homie.record(sensor='livingroom:humidity', value=datum.humidity, datetime=datum.datetime)
    return datum


# -----------------------------------------------------------------------------------------------------------------------------

scheduler.add_job(func=sense, trigger="interval", hours=1)

# =============================================================================================================================

scheduler.start()
# scheduler.print_jobs()
