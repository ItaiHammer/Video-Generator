import os
from random import randint, uniform
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, TextClip, CompositeVideoClip, CompositeAudioClip, concatenate_audioclips, ColorClip, vfx, afx, concatenate_videoclips
from moviepy.video.fx.all import crop
from uploadTik import upload_video_from_json
from audioEngine import Music
# import speech_recognition as sr
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
import wave
import soundfile

assetsDir = f"./assets/"
gameplayDir = f"{assetsDir}/gameplay/"

# list of all words and their time in the video
transcript = []

def cutString(text, characterPerRow, maxRowCount):
    textArr = text.split(' ')
    output = ""

    curRow = 0
    rows = [""]

    for i in range(len(textArr)):
        if (len(rows[curRow]) + len(textArr[i]) + 1 <= characterPerRow):
            if (rows[curRow] == ""):
                rows[curRow] += textArr[i]
            else:
                rows[curRow] += f" {textArr[i]}"
        elif (len(rows) + 1 > maxRowCount):
            rows[curRow] += "..."
            break
        else:
            curRow += 1
            rows.append("")
            rows[curRow] += textArr[i]

    for i in range(len(rows)):
        output += f"{rows[i]}\n"
    
    return output

def numberShortner(number):
    if (number >= 1000000):
        return f"{int(number/1000000)}M+"
    if (number >= 1000):
        return f"{int(number/1000)}K+"
    else:
        return number


class AssetManager:
    def getRandomGameplay():
        gameplayVideos = []

        for file in os.scandir(gameplayDir):
            split = os.path.splitext(file)
            fileExt = split[1]

            # checking if it's a video file
            if fileExt == ".mp4":
                gameplayVideos.append(file)

        if len(gameplayVideos) == 1:
            return gameplayVideos[0]

        return gameplayVideos[randint(0, len(gameplayVideos) - 1)]
    
    def chooseRandomSubclip(duration, clip):
        # if cut is bigger than clip
        if duration > clip.duration:
            return -1
        
        # if cut is bigger than clip
        if duration == clip.duration:
            return clip
        
        # finds a random start to the clip
        start = uniform(0, clip.duration - duration)
        
        clippedVideo = clip.subclip(start, start+duration)
        return clippedVideo
    
    def createRedditBanner(redditPost):
        templateBanner = ImageClip('./assets/reddit/intro banner.png').resize(height=200).set_pos('center')

        pfp = ImageClip('./assets/reddit/pfp.png').resize(height=50).set_position((10, 10))
        
        name = TextClip(f"r/{redditPost['subreddit'][0].upper()}{redditPost['subreddit'][1:]}", fontsize = 20, font="Amiri-bold", color = 'black').set_position((70, 25))

        titleText = cutString(redditPost['title'], 23, 3)
        title = TextClip(titleText, fontsize = (28 + 15/(len(titleText.split('\n')) * 4)), font="Calibri-Bold", align="West", color = 'black').set_position((25, 45 + 90/len(titleText.split('\n'))))

        score = TextClip(f"{numberShortner(redditPost['score'])}", fontsize = 20, font="Amiri-bold", color = '#404040').set_position((65, 163))

        commentCount = TextClip(f"{numberShortner(redditPost['commentCount'])}", fontsize = 20, font="Amiri-bold", color = '#404040').set_position((147, 163))

        return CompositeVideoClip([templateBanner, pfp, name, title, score, commentCount])
       
    # def createRedditCaptions(script, voiceover_duration=0.3, fps=30, font='Times New Roman', fontsize=45, color='white', stroke_color='black'):
    #     # Initialize a list to store TextClips
    #     text_clips = []
        
    #     # Create TextClips for each set of 5 words
    #     words_list = script["script"].split(" ")
    #     words_list = [item for item in words_list if item != ""] # sometimes it has empty which cause bugs so must keep this!

    #     word_count = len(words_list)
    #     duration_per_caption = voiceover_duration / word_count

    #     for i, word in enumerate(words_list):
    #         # if word == '': # sometimes it splits with ""
    #         #     continue
    #         text_clip = TextClip(word, font=font, fontsize=fontsize, color=color, stroke_color=stroke_color, stroke_width=2)
    #         text_clips.append(text_clip.set_duration(duration_per_caption))
        
    #     # Concatenate all TextClips into a single VideoClip
    #     final_clip = concatenate_videoclips(text_clips, method="compose").set_pos(("center","center"))
        
    #     return final_clip

    def generateTrascript(path: str):
        # fixing wav file
        data, samplerate = soundfile.read(f"{path}/voiceover.wav")
        soundfile.write(f"{path}/voiceover.wav", data, samplerate)


        # Open WAV file
        wf = wave.open(f"{path}/voiceover.wav", "rb")

        # Initialize model and recognizer
        model = Model("./config/vosk-model")
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part_result = json.loads(rec.Result())
                transcript.append(part_result)
        part_result = json.loads(rec.FinalResult())
        transcript.append(part_result)

        wf.close()

    
    def generateSubtitles(path: str, duration):

        subtitles = []

        subtitles.append(ColorClip(size =(500, 500), color =[0, 0, 0]).set_start(duration).subclip(0, 0))
        
        for sentence in transcript:
            if len(sentence) == 1:
                # sometimes there are bugs in recognition 
                # and it returns an empty dictionary
                # {'text': ''}
                continue
            for i, word in enumerate(sentence['result']):
                duration = 0
                if i+1 >= len(sentence['result']):
                    duration = 1
                else:
                    duration = sentence['result'][i+1]['start'] - word['start']

                word['word'] = word['word'][0:1].upper() + word['word'][1:]

                textOutline = TextClip(word["word"], fontsize = 60, font="Calibri-Bold", color = 'yellow', stroke_color="black", stroke_width=4).set_start(word['start']).set_pos(("center","center")).set_duration(duration)
                text = TextClip(word["word"], fontsize = 60, font="Calibri-Bold", color = 'yellow').set_start(word['start']).set_pos(("center","center")).set_duration(duration)
                
                w = CompositeVideoClip([textOutline, text]).set_pos(("center","center"))
                
                subtitles.append(w)
        
        print("Subtitle Transcription complete!!!")

        return CompositeVideoClip(subtitles).set_pos(("center","center"))
    
    def findRedditIntroLength(redditPost):

        title = redditPost['title']
        title = title.replace(',', '').replace('.', '').replace('?', '').replace(']', '').replace('[', '')
        title = title.split(' ')

        currIndex = len(redditPost['title'].split(' '))-1
        lastWord = title[currIndex]
        introEndTime = 0

        transcriptFirstSentence = transcript[0]

        while introEndTime == 0 and currIndex >= 0:
            for i, word in reversed(list(enumerate(transcriptFirstSentence['result']))):
                if (word["word"] == lastWord):
                    introEndTime = round(word["end"])
                    break

            currIndex -= 1
            lastWord = title[currIndex]

        return introEndTime

class VideoGenerator:
    def createScriptedVideo(path: str, music, redditPost):
        
        # Generate Everything
        introDuration = 4
        voiceover = AudioFileClip(f"{path}/voiceover.mp3")

        # transcribe_gcs_with_word_time_offsets(f"{path}/voiceover.mp3")


        gameplay = AssetManager.chooseRandomSubclip(voiceover.duration+ 1, VideoFileClip(f"{gameplayDir}{AssetManager.getRandomGameplay().name}")).fx(vfx.fadein, introDuration)
        captions = AssetManager.createRedditCaptions(redditPost, voiceover.duration)

        # Compose all togther
        video = CompositeVideoClip([gameplay, captions]) # includes order of things on the screen, first is below everything else

        # add music
        if (music):
            music = AudioFileClip(f"./assets/music/{Music.getRandomMusic().name}").fx(afx.volumex, 0.2)

            # music will be same duration as video
            while (music.duration < voiceover.duration):
                music = concatenate_audioclips([music, music])

            music = music.subclip(0, voiceover.duration)

            video.audio = CompositeAudioClip([voiceover, music])
        else:
            video.audio = voiceover

        # write to file
        video.write_videofile(f"{path}/video.mp4")

        # upload video
        data = {
            "video_path": f"{path}/video.mp4",
            "title": redditPost["tags"],
            "schedule_time": 0,
            "comment": 1,
            "duet": 0,
            "stitch": 0,
            "visibility": 0,
            "brandorganic": 0,
            "brandcontent": 0,
            "ailabel": 0,
            "proxy": ""
        }
        upload_video_from_json(data)

        video.close()
        # video.audio.close()

    def createRedditVideo(path: str, banner, data, redditPost):
        AssetManager.generateTrascript(path)
        introDuration = AssetManager.findRedditIntroLength(redditPost)
        video = []
        voiceover = AudioFileClip(f"{path}/voiceover.wav")
        gameplay = AssetManager.chooseRandomSubclip(voiceover.duration+ 1, VideoFileClip(f"{gameplayDir}{AssetManager.getRandomGameplay().name}")).fx(vfx.fadein, introDuration)
        introBanner = banner.set_duration(introDuration+1).set_pos(("center","center")).resize(width=(((gameplay.size[1] * 9/16)/100) * 70))
        
        video.append(gameplay)
        if len(data['watermark']) != 0:
            w = TextClip(data['watermark'], fontsize = 50 - (len(data['watermark'])/2), font="Calibri-Bold", color = 'white').set_pos(("center", (gameplay.size[1]/100) * 55)).set_duration(voiceover.duration+ 1).set_opacity(.2).set_start(introDuration).set_duration(voiceover.duration+ 1 - introDuration)
            video.append(w)
        if data['subtitles']:
            video.append(AssetManager.generateSubtitles(path, voiceover.duration + 1))
        video.append(introBanner)

        video = CompositeVideoClip(video)

        if (data['music']):
            music = AudioFileClip(f"./assets/music/{Music.getRandomMusic().name}").fx(afx.volumex, 0.2)

            while (music.duration < voiceover.duration + 1):
                music = concatenate_audioclips([music, music])

            music = music.subclip(0, voiceover.duration + 1)

            video.audio = CompositeAudioClip([voiceover, music])
        else:
            video.audio = voiceover

        # cropping it to tiktok aspect ratio
        # (w, h) = video.size
        # if (w % 9 != 0 or h % 16 != 0):

        #     cropWidth = h * 9/16
        #     # x1,y1 is the top left corner, and x2, y2 is the lower right corner of the cropped area.

        #     x1, x2 = (w - cropWidth)//2, (w+cropWidth)//2
        #     y1, y2 = 0, h
        #     video = crop(video, x1=x1, y1=y1, x2=x2, y2=y2)

        video.write_videofile(f"{path}/video.mp4")

        # upload video
        data = {
            "video_path": f"{path}/video.mp4",
            "title": redditPost["tags"],
            "schedule_time": 0,
            "comment": 1,
            "duet": 0,
            "stitch": 0,
            "visibility": 0,
            "brandorganic": 0,
            "brandcontent": 0,
            "ailabel": 0,
            "proxy": ""
        }
        upload_video_from_json(data)

        video.close()
        # video.audio.close()
