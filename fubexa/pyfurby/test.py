import board, digitalio, time

from .motor import FurbyMotor


class Dummy(FurbyMotor):
    """
    This is a test mode.
    """

    def __init__(self, red: int = 14, green: int = 24, mouth: int = 18):
        super().__init__()
        self.red_pin = digitalio.DigitalInOut(digitalio.Pin(red))
        self.red_pin.switch_to_output(False)
        self.green_pin = digitalio.DigitalInOut(digitalio.Pin(green))
        self.green_pin.switch_to_output(False)
        self.mouth_pin = digitalio.DigitalInOut(digitalio.Pin(mouth))
        self.mouth_pin.switch_to_input(pull=digitalio.Pull.UP)

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

    def dance(self):
        self.set_percent_speed(70)
        with :

            d.move_clockwise()
            for i in range(5):
                while True:
                    if not cycle_pin.value:
                        print(f'{i} CCW')
                        self.move_counterclockwise()
                        time.sleep(1)
                        break
                while  True:
                    if not cycle_pin.value:
                        print(f'{i} CW')
                        self.move_clockwise()
                        time.sleep(1)
                        break
        d.halt()

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
