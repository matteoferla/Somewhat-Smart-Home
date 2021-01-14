"""
FurbyMotor adds motor control

SoundMotor controls motor by sound

"""

from .buttons import FurbyButtons
from .motor import FurbyMotor
from .talk import FurbyTalk
from .sound import FurbySound
from .test_moves import FurbyTests


class Furby(FurbyMotor, FurbyButtons, FurbyTalk, FurbySound, FurbyTests):

    def __init__(self,
                 pwma: int = 22,  # white
                 stby: int = 4,  # yellow
                 ain1: int = 27,
                 ain2: int = 17,
                 cycle: int = 21,
                 red: int = 14,
                 green: int = 24,
                 mouth: int = 18,
                 chest: int = 20,
                 back: int = 16,
                 voice_name: str = 'en-scottish+m4',
                 voice_volume: int = 0.7,
                 voice_rate: int = 200):
        FurbyMotor.__init__(self, pwma=pwma, stby=stby, ain1=ain1, ain2=ain2, cycle=cycle)
        FurbyButtons.__init__(self, red=red, green=green, mouth=mouth, chest=chest, back=back)
        FurbyTalk.__init__(self, voice_name=voice_name, voice_rate=voice_rate, voice_volume=voice_volume)
        # FurbySound and FurbyTests no init.

    def move_on_play(self):
        if self.playing:
            self.move_clockwise()
        else:
            self.halt()

    def say(self, text:str, move: bool=True):
        self.move_clockwise()
        super().say(text)
        self.halt()

    def action_cycle(self):
        pass

# if __name__ == '__main__':
#     #pwma: int = 7, stby: int = 13, ain1: int = 16, ain2: int = 11
#     furby = SoundMotor()
#     while True:
#         furby.move_on_play()
