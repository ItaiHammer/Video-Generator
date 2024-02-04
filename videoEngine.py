import os
from random import randint, uniform
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, TextClip, CompositeVideoClip, CompositeAudioClip, vfx, afx, concatenate_videoclips
from audioEngine import Music
import math
assetsDir = f"./assets/"
gameplayDir = f"{assetsDir}/gameplay/"

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
        
        return clip.subclip(start, start+duration)
    
    def createRedditBanner(redditPost):
        templateBanner = ImageClip('./assets/reddit/intro banner.png').resize(height=200).set_pos('center')

        pfp = ImageClip('./assets/reddit/pfp.png').resize(height=50).set_position((10, 10))
        
        name = TextClip(f"r/{redditPost['subreddit'][0].upper()}{redditPost['subreddit'][1:]}", fontsize = 20, font="Amiri-bold", color = 'black').set_position((70, 25))

        titleText = cutString(redditPost['title'], 23, 3)
        title = TextClip(titleText, fontsize = (28 + 15/(len(titleText.split('\n')) * 4)), font="Calibri-Bold", align="West", color = 'black').set_position((25, 45 + 90/len(titleText.split('\n'))))

        score = TextClip(f"{numberShortner(redditPost['score'])}", fontsize = 20, font="Amiri-bold", color = '#404040').set_position((65, 163))

        commentCount = TextClip(f"{numberShortner(redditPost['commentCount'])}", fontsize = 20, font="Amiri-bold", color = '#404040').set_position((147, 163))

        return CompositeVideoClip([templateBanner, pfp, name, title, score, commentCount])        


class VideoGenerator:
    def createRedditVideo(path: str, banner, music):
        introDuration = 4
        introBanner = banner.set_duration(introDuration+1).set_pos(("center","center"))
        voiceover = AudioFileClip(f"{path}/voiceover.mp3")
        gameplay = AssetManager.chooseRandomSubclip(voiceover.duration+ 1, VideoFileClip(f"{gameplayDir}{AssetManager.getRandomGameplay().name}")).fx(vfx.fadein, introDuration)
        
        video = CompositeVideoClip([gameplay, introBanner])

        if (music):
            music = AudioFileClip(f"./assets/music/{Music.getRandomMusic().name}").fx(afx.volumex, 0.2)

            if (music.duration > voiceover.duration):
                music = music.subclip(0, voiceover.duration)

            video.audio = CompositeAudioClip([voiceover, music])
        else:
            video.audio = voiceover

        video.write_videofile(f"{path}/video.mp4")
