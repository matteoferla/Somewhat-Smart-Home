#!pip install -q Adafruit-DHT
#!pip install --upgrade -q six
#!pip install -q adafruit-circuitpython-dht
#! sudo apt-get install libgpiod2

from .base import BaseHall
from .wind import Anemometer
from .rain import RainGauge
from .temp import Temperature
