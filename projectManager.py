import sys
import os
from video import Video
from scriptEngine import makeRedditScript
import json

outDir = './out/'
assetsDir = './assets/'
currentRunVideosProduced = 1
# create video
def createRedditVideo(name, data):        
    redditPosts = makeRedditScript(data["subreddit"], data["videoCount"], data["chatGPT"])
    
    if not data["makeVideo"]: 
        # Serializing json
        dictionary = {
            "redditPosts": redditPosts,
            "data": data,
            "name": name,
        }
        json_object = json.dumps(dictionary, indent=4)
        # Writing to sample.json
        os.remove("./scripts/scripts.json")
        with open("./scripts/scripts.json", "w") as outfile:
            outfile.write(json_object)
        return "json complete!"
    
    makeVideo(name, data, redditPosts)
    return "videos complete!"

def createScriptedVideo(json_data):    
    redditPosts = json_data["redditPosts"]   
    name = json_data["name"]
    data = json_data["data"] 
    makeVideo(name, data, redditPosts)
    return "videos complete!"

def makeVideo(name, data, redditPosts):
    for i in range(len(redditPosts)):
        print(f"\033[35m working on video #{i+1} \033[0m")
        video = Video(name, data)
        redditPost = redditPosts[i]
        print(f"\033[36m Writing script to file for #{i+1} \033[0m")
        file = open(f"{video.path}/script.txt", 'a', encoding='utf-8')
        file.write(redditPost["script"])
        file.close()
        # print("Do you approve the script? respond \"y\" if yes")
        # scriptApproval = input()
        # if (scriptApproval == "y"):
        print(f"\033[37m Generating TTS for #{i+1} \033[0m")
        video.createAudio(redditPost['script'])
        print(f"\033[38m Starting the video gen for #{i+1} \033[0m")
        video.createRedditVideo(redditPost, data)