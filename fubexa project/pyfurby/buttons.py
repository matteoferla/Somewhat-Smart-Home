import board, digitalio, time

from .motor import FurbyMotor


class FurbyButtons:
    """
    There are a few buttons. All configured as pull-ups
    """

    def __init__(self, red: int = 14, green: int = 24, mouth: int = 18, chest: int=20, back: int=16):
        super().__init__()
        # LEDs
        self.red_pin = digitalio.DigitalInOut(digitalio.Pin(red))
        self.green_pin = digitalio.DigitalInOut(digitalio.Pin(green))
        for color_pin in (self.red_pin, self.green_pin):
            color_pin.switch_to_output(False)
        # buttons
        self.mouth_pin = digitalio.DigitalInOut(digitalio.Pin(mouth))
        self.chest_pin = digitalio.DigitalInOut(digitalio.Pin(chest))
        self.back_pin = digitalio.DigitalInOut(digitalio.Pin(back))
        for button_pin in (self.mouth_pin, self.chest_pin, self.back_pin):
            button_pin.switch_to_input(pull=digitalio.Pull.UP)

    @property
    def bitten(self):
        return not self.mouth_pin.value

    @property
    def fore_squeezed(self):
        return not self.chest_pin.value

    @property
    def aft_squeezed(self):
        return not self.back_pin.value

    @property
    def squeezed(self):
        return self.fore_squeezed or self.aft_squeezed