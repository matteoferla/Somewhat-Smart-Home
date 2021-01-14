import board, digitalio, time
from typing import Optional

class FurbyTests:
    """
    This is a test mode.
    """

    def ambulance(self, cycles: int = 50):
        for i in range(cycles):
            self.green_pin.value = True
            self.red_pin.value = False
            time.sleep(0.2)
            self.green_pin.value = False
            self.red_pin.value = True
            time.sleep(0.2)
        self.green_pin.value = False
        self.red_pin.value = False

    def dance(self, speed:Optional[float]=None):
        if speed:
            self.set_percent_speed(speed)
        self.move_clockwise()
        for i in range(5):
            while True:
                if not self.cycle_pin.value:
                    print(f'{i} CCW')
                    self.move_counterclockwise()
                    time.sleep(1)
                    break
            while  True:
                if not self.cycle_pin.value:
                    print(f'{i} CW')
                    self.move_clockwise()
                    time.sleep(1)
                    break
        self.halt()

    def bite(self):
        while self.mouth_pin.value:
            pass
        print('woof')
        for i in range(20):
            self.green_pin.value = True
            self.red_pin.value = True
            time.sleep(0.05)
            self.green_pin.value = False
            self.red_pin.value = False
            time.sleep(0.05)
