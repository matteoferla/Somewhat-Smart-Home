from threading import Thread
import digitalio, board  # noqa
from typing import List, Union
import time
from statistics import median


class BaseHall:

    def __init__(self, pin_id: Union[board.pin.Pin, int], window: int):
        """
        Initialising this class results in
        the thread ``_counter`` taking timepoints stored in ``self.times``.
        The frequency is calculated within the time window ``window`` in secs.
        """
        pin_id: board.pin.Pin = pin_id if isinstance(pin_id, board.pin.Pin) else board.pin.Pin(pin_id)
        self.pin = digitalio.DigitalInOut(pin_id)
        self.pin.direction = digitalio.Direction.INPUT

        self.window = window
        self.times: List[float] = []  # unix-times the hall transistor became on
        self.measuring = True  # changing this will end the thread.
        self._counter = Thread(target=self._assess, args=[])
        self._counter.start()

    def _assess(self):
        raise NotImplementedError('virtual method')

    def __del__(self):
        self.measuring = False  # kills ``self._counter``.

    @property
    def recent_measurements(self) -> List[float]:
        now: float = time.time()
        return [t for t in self.times if now - t < self.window]

    @property
    def total(self) -> int:
        return len(self.recent_measurements)

    @property
    def period(self) -> float:
        """
        length of a cycle
        """
        recent_measurements: List[float] = self.recent_measurements
        if len(recent_measurements) < 2:  # never spun or no spin in 5 minutes...
            return 0
        intervals: List[float] = [post - pre for pre, post in zip(recent_measurements[:-1], recent_measurements[1:])]
        return median(intervals)

    @property
    def frequency(self) -> float:
        """
        f in Hertz. cycles per second
        """
        p = self.period
        return 1 / p if p != 0 else 0
