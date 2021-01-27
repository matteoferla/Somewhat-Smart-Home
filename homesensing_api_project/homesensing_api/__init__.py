import requests, os, shutil
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

    # ==================================================================================================================

    def read(self, delta: int = 7):
        """
        ``read`` reads the values recorded with ``record``,
        unlike ``show`` which shows the photo stored with ``store``.

        :param delta: time delta in days (int)
        :return: dict reply from server
        """
        reply = requests.get(f'{self.base_url}/read', {'delta': delta})
        return self.get_json(reply)


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

    # ==================================================================================================================

    def show(self, delta: int = 7):
        """
        Shows the list of image paths

        :param delta: time delta in days (int)
        :return:
        """
        reply = requests.get(f'{self.base_url}/show', {'delta': delta})
        return self.get_json(reply)

    def download_img(self, address, filename):
        """
        downloads a photo within the folder static/photos.

        :param address: everything after ``static/photos/``
        :param filename:
        :return:
        """
        url = f'{self.base_url}/static/photos/{address.split("static/photos/")[-1]}'
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            return True
        else:
            raise ConnectionError

    def store(self,
              sensor: str,
              filename: str,
              datetime: Optional[dt.datetime] = None):
        """
        Record is to record a value, store is to store an image

        :param sensor: name
        :param filename: to be read and sent
        :param datetime:
        :return:
        """
        isodate = self.isodatify(datetime)
        extension = os.path.splitext(filename)[1]
        reply = requests.post(f'{self.base_url}/store', {'key': self.key,
                                                         'extension': extension,
                                                         'datetime': isodate,
                                                         'sensor': sensor},
                              files={'photo': open(filename, 'rb')}
                              )
        return self.get_json(reply)

    # ==================================================================================================================

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

    # ==================================================================================================================

    def isodatify(self, datetime):
        if datetime is None:
            return dt.datetime.now().isoformat()
        elif isinstance(datetime, str):
            return datetime
        elif isinstance(datetime, dt.datetime):
            return datetime.isoformat()
        else:
            raise ValueError

    def get_json(self, reply):
        if reply.status_code != 200:
            raise ValueError(reply.text)
        else:
            return reply.json()
