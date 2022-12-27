import digitalio, board  # noqa
import time
from typing import Union
from .base import BaseHall


class RainGauge(BaseHall):
    def __init__(self, pin_id: Union[board.pin.Pin, int] = board.D18,
                 window:int=60 * 5,
                 volume: float = 0.0085,
                 area: float = 0.0063615):
        super().__init__(pin_id=pin_id, window=window)
        self.volume = volume
        self.area = area

    def _assess(self):
        previous = None
        while self.measuring:
            if bool(self.pin.value) is not previous:
                previous = bool(self.pin.value)
                self.times.append(time.time())

    @property
    def rate(self) -> float:
        return self.frequency * self.volume / self.area  # liter per m2 per sec
