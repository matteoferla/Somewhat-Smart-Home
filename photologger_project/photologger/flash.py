import digitalio
import board

###################################################
#
class Flash:
    """
    this should be using camera.led_pin! and flash_mode

    """
    light = digitalio.DigitalInOut(board.D21)
    light.direction = digitalio.Direction.OUTPUT

    def __init__(self):
        pass

    def __enter__(self):
        self.light.value = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.light.value = False

