import pyttsx3


class SpeechSynthesizer:
    engine: pyttsx3.engine

    def __init__(self, voice, rate: int, volume: float):
        self.engine = pyttsx3.init()
        if voice:
            self.engine.setProperty('voice', voice)
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def listVoices(self):
        voices: list = [self.engine.getProperty('voices')]

        for i, voice in enumerate(voices[0]):
            print(f"{i + 1} {voice.name} {voice.age}: {voice.languages[0]} ({voice.gender}) [{voice.id}]")

    def say(self, text: str):
        self.engine.say(text)

    def createMP3(self, text: str, path: str):
        fileName = f"{path}/voiceover.mp3"

        self.engine.save_to_file(text, fileName)
        self.engine.runAndWait()

