import pyttsx3

class FurbyTalk:
    def __init__(self, voice_name:str='en-scottish+m4', voice_volume:int=0.7, voice_rate:int=200):
        self.engine = pyttsx3.init()
        self.engine.setProperty('volume', voice_volume)
        self.engine.setProperty('voice', voice_name)
        self.engine.setProperty('rate', voice_rate)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

