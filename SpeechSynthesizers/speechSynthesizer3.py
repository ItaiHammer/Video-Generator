import os
from elevenlabs import set_api_key, generate, save
from dotenv import load_dotenv

# ENV and praw setup
load_dotenv(encoding="utf-16")

class SpeechSynthesizer:
    def __init__(self):
        set_api_key(os.getenv("ELEVEN_LABS_API_KEY"))

    def createMP3(self, text: str, path: str, voice: str):
        tts = generate(text=text, voice=voice)
        save(tts, f"{path}/voiceover.mp3")

