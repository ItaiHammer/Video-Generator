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