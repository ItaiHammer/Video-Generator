import os
from random import randint, uniform
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, TextClip, CompositeVideoClip, CompositeAudioClip, concatenate_audioclips, vfx, afx, concatenate_videoclips
from audioEngine import Music

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
        
    def createRedditCaptions(script, voiceover_duration=0.3, fps=30, font='Times New Roman', fontsize=45, color='white', stroke_color='black'):
        # Initialize a list to store TextClips
        text_clips = []
        
        # Create TextClips for each set of 5 words
        words_list = script["script"].split(" ")
        words_list = [item for item in words_list if item != ""] # sometimes it has empty which cause bugs so must keep this!

        word_count = len(words_list)
        duration_per_caption = voiceover_duration / word_count

        for i, word in enumerate(words_list):
            # if word == '': # sometimes it splits with ""
            #     continue
            text_clip = TextClip(word, font=font, fontsize=fontsize, color=color, stroke_color=stroke_color, stroke_width=2)
            text_clips.append(text_clip.set_duration(duration_per_caption))
        
        # Concatenate all TextClips into a single VideoClip
        final_clip = concatenate_videoclips(text_clips, method="compose").set_pos(("center","center"))
        
        return final_clip
    
# def transcribe_gcs_with_word_time_offsets(gcs_uri: str): #-> speech.RecognizeResponse:
#     from google.cloud import speech

#     client = speech.SpeechClient()

#     audio = speech.RecognitionAudio(uri=gcs_uri)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
#         sample_rate_hertz=16000,
#         language_code="en-US",
#         enable_word_time_offsets=True,
#     )

#     operation = client.long_running_recognize(config=config, audio=audio)

#     print("Waiting for operation to complete...")
#     result = operation.result(timeout=90)

#     for result in result.results:
#         alternative = result.alternatives[0]
#         print(f"Transcript: {alternative.transcript}")
#         print(f"Confidence: {alternative.confidence}")

#         for word_info in alternative.words:
#             word = word_info.word
#             start_time = word_info.start_time
#             end_time = word_info.end_time

#             print(
#                 f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
#             )

#     return result

class VideoGenerator:
    def createRedditVideo(path: str, banner, music, redditPost):
        
        # Generate Everything
        introDuration = 4
        introBanner = banner.set_duration(introDuration+1).set_pos(("center","center"))
        voiceover = AudioFileClip(f"{path}/voiceover.mp3")

        # transcribe_gcs_with_word_time_offsets(f"{path}/voiceover.mp3")


        gameplay = AssetManager.chooseRandomSubclip(voiceover.duration+ 1, VideoFileClip(f"{gameplayDir}{AssetManager.getRandomGameplay().name}")).fx(vfx.fadein, introDuration)
        captions = AssetManager.createRedditCaptions(redditPost, voiceover.duration)

        # Compose all togther
        video = CompositeVideoClip([gameplay, captions, introBanner]) # includes order of things on the screen, first is below everything else

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

        video.close()
        # video.audio.close()
