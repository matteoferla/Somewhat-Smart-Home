"""
FurbyMotor adds motor control

SoundMotor controls motor by sound

"""
from .sound_motor import SoundMotor

if __name__ == '__main__':
    #pwma: int = 7, stby: int = 13, ain1: int = 16, ain2: int = 11
    furby = SoundMotor()
    while True:
        furby.move_on_play()