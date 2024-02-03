from gtts import gTTS


class SpeechSynthesizer:
    def createMP3(self, text: str, path: str):
        tts = gTTS(text)
        tts.save(f"{path}/voiceover.mp3")

