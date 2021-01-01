#!/usr/bin/env python

import time, digitalio, board, pulseio

class FurbyMotor:
    soundcard_status_file = '/proc/asound/card0/pcm0p/sub0/status'
    high_speed = 0xffff

    def __init__(self, pwma: int = 7, stby: int = 13, ain1: int = 16, ain2: int = 11):
        # standby: H-bridges to work when high
        self.standby_pin = digitalio.DigitalInOut(digitalio.Pin(stby))
        self.standby_pin.switch_to_output(False)
        # direction 1
        self.ain1_pin = digitalio.DigitalInOut(digitalio.Pin(ain1))
        self.ain1_pin.switch_to_output(False)
        # direction 2
        self.ain2_pin = digitalio.DigitalInOut(digitalio.Pin(ain2))
        self.ain2_pin.switch_to_output(False)
        # pwma
        self.pwm_pin = pulseio.PWMOut(pin=digitalio.Pin(pwma),
                                      duty_cycle=0,
                                      frequency=100)

    def move_clockwise(self):
        self.standby_pin.value = True
        self.pwm_pin.duty_cycle = self.high_speed
        self.ain1_pin.value = True
        self.ain2_pin.value = False

    def move_counterclockwise(self):
        self.standby_pin.value = True
        self.pwm_pin.duty_cycle = self.high_speed
        self.ain1_pin.value = False
        self.ain2_pin.value = True

    def halt(self):
        self.standby_pin.value = False
        self.pwm_pin.duty_cycle = 0
        self.ain1_pin.value = False
        self.ain2_pin.value = False

    @property
    def playing(self):
        with open(self.soundcard_status_file, 'r') as fh:
            value = fh.read()
        if value == 'RUNNING':
            return True
        else: # 'closed'
            return False

    def move_on_play(self):
        if self.playing:
            self.move_clockwise()
        else:
            self.halt()

    def set_percent_speed(self, speed:int):
        self.high_speed = int(speed/100 * 0xffff)


if __name__ == '__main__':
    furby = FurbyMotor()
    while True:
        furby.move_on_play()

