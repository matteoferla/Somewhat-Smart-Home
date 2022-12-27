import digitalio, board  # noqa
import time, math
from typing import List, Union
from .base import BaseHall


class Anemometer(BaseHall):
    def __init__(self, pin_id: Union[board.pin.Pin, int] = board.D15,
                 window: int = 60 * 5,  # sec
                 radius: float = 0.07,  # meter
                 ):
        """
        Initialising this class results in
        the thread ``_counter`` taking timepoints stored in ``self.times``,
        when the hall transistor becomes high.

        ane = Anemometer(15)
        ane.frequency
        """
        super().__init__(pin_id=pin_id, window=window)
        self.radius = radius  # unit: m

    def _assess(self):
        ongoing = False
        while self.measuring:
            if bool(self.pin.value) and not ongoing:
                ongoing = True
                self.times.append(time.time())
            elif bool(self.pin.value):
                pass  # it's not passed the magnet yet
            elif ongoing:
                ongoing = False
            else:  # it's in the spinning phase
                pass

    @property
    def angular_frequency(self) -> float:
        """
        w in radian per sec
        """
        return self.frequency * 2 * math.pi

    @property
    def speed(self):
        """
        tangential speed in m/s
        """
        return self.angular_frequency * self.radius
