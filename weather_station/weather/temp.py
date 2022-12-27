import board  # noqa
import adafruit_dht  # noqa
from typing import Union
import time

class Temperature:
    def __init__(self, pin_id: Union[board.pin.Pin, int] = board.D4):
        pin_id: board.pin.Pin = pin_id if isinstance(pin_id, board.pin.Pin) else board.pin.Pin(pin_id)
        try:
            self.dht = adafruit_dht.DHT22(pin_id)
            self.dht()
        except Exception as error:
            time.sleep(10)
            self.dht.exit()
            self.dht = adafruit_dht.DHT22(pin_id)

    def __call__(self):
        """
        This is a shitty sensor
        """
        error_level = 0
        while error_level < 100:
            try:
                self.dht.measure()
                temperature = self.dht.temperature
                humidity = self.dht.humidity
                if temperature is None:
                    raise RuntimeError('no temp')
                return temperature, humidity
            except RuntimeError as error:
                error_level += 1
                print(error.__class__.__name__, str(error))
                continue
