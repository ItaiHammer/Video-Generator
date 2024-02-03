import projectManager
import os
from audioEngine import SpeechSynthesizer
from videoEngine import VideoGenerator, AssetManager

class Video:
    def __init__(self, name, data):
        # making project folder
        self.path = f"{projectManager.outDir}{name}"
        self.name = name

        while os.path.exists(self.path):
            if self.path[len(self.path)-1:].isdigit():
                self.path = f"{self.path[0:len(self.path)-1]}{int(self.path[len(self.path)-1])+1}"
            else:
                self.path = f"{self.path}_1"

        os.mkdir(self.path)

    def createAudio(self, script: str):
        # SS3 Eleven Labs
        # tts = SpeechSynthesizer.speechSynthesizer3()
        # tts.createMP3(script, self.path, 'Adam')
       
       # SS2 Google Assistant
    #    tts = SpeechSynthesizer.speechSynthesizer2()
    #    tts.createMP3(script, self.path)
       
       # SS1 Windows Synthesizer
       tts = SpeechSynthesizer.speechSynthesizer1(None, 150, 1.0)
       tts.createMP3(script, self.path)

    def createRedditVideo(self, redditPost, data):
        banner = AssetManager.createRedditBanner(redditPost)
        # captions = AssetManager.createRedditCaptions(redditPost)
        
        VideoGenerator.createRedditVideo(self.path, banner, data['music'])