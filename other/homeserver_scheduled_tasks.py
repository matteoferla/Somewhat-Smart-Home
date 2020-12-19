

"""

Code from homeserver. For now only CPU temp
# 192.168.0.84
# "homeserver"

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


scheduler = BlockingScheduler()


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




# -----------------------------------------------------------------------------------------------------------------------------

from datetime import datetime

def core():
    with open('/sys/class/thermal/thermal_zone0/temp') as core:
        v = int(core.read().strip()) / 1e3
        homie.record(sensor='homeserver:CPU_temperature', value=v, datetime=datetime.now())
        return v

# -----------------------------------------------------------------------------------------------------------------------------

print(core())
scheduler.add_job(func=core, trigger="interval", hours=1)

# =============================================================================================================================

scheduler.start()
# scheduler.print_jobs()
