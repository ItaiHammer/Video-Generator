import os
from random import randint
from projectManager import base_dir
import sys
# speech_dir = f'{base_dir}/SpeechSynthesizers'
# print("speech_dir---------------------------------------------")
# print(speech_dir)
# sys.path.append('/SpeechSynthesizers')
from SpeechSynthesizers import speechSynthesizer1, speechSynthesizer2, speechSynthesizer3

musicDir = f'{base_dir}/assets/music/'

class SpeechSynthesizer:
    speechSynthesizer1 = speechSynthesizer1.SpeechSynthesizer
    speechSynthesizer2 = speechSynthesizer2.SpeechSynthesizer
    speechSynthesizer3 = speechSynthesizer3.SpeechSynthesizer

class Music:
    def getRandomMusic():
        songs = []

        for file in os.scandir(musicDir):
            split = os.path.splitext(file)
            fileExt = split[1]

            # checking if it's a video file
            if fileExt == ".mp3":
                songs.append(file)

        if len(songs) == 1:
            return songs[0]

        return songs[randint(0, len(songs) - 1)]