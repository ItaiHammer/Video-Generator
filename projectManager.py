import sys
import os
from video import Video
from scriptEngine import makeRedditScript

outDir = './out/'
assetsDir = './assets/'
currentRunVideosProduced = 1
# create video
def createRedditVideo(name, data):        

    redditPosts = makeRedditScript(data["subreddit"], data["numberVideos"])
    for i in range(len(redditPosts)):
        print(f"\033[35m working on video #{i+1} \033[0m")
        video = Video(name, data)
        redditPost = redditPosts[i]
        file = open(f"{video.path}/script.txt", 'a', encoding='utf-8')
        file.write(redditPost["script"])
        file.close()
        # print("Do you approve the script? respond \"y\" if yes")
        # scriptApproval = input()
        # if (scriptApproval == "y"):
        video.createAudio(redditPost['script'])
        video.createRedditVideo(redditPost, data)
    return "videos complete!"

def createScriptedVideo(name, data):        
    print(data)
    for i in range(len(data["data"]["scripts"])):
        video = Video(name, data)
        redditPost = {"script": f"{data["data"]["scripts"][i]["Hook"]} {data["data"]["scripts"][i]["Script"]["Step 1"]} {data["data"]["scripts"][i]["Script"]["Step 2"]} {data["data"]["scripts"][i]["Script"]["Step 3"]}"}
        file = open(f"{video.path}/script.txt", 'a', encoding='utf-8')
        file.write(redditPost["script"])
        file.close()
        video.createAudio(redditPost['script'])
        video.createScriptedVideo(redditPost, data)
    return "videos complete!"