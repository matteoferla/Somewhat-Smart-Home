from .motor import FurbyMotor


class SoundMotor(FurbyMotor):
    soundcard_status_file = '/proc/asound/card0/pcm0p/sub0/status'

    @property
    def playing(self):
        with open(self.soundcard_status_file, 'r') as fh:
            value = fh.read()
        if value == 'RUNNING':
            return True
        else:  # 'closed'
            return False

    def move_on_play(self):
        if self.playing:
            self.move_clockwise()
        else:
            self.halt()