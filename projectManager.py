from video import Video
from scriptEngine import makeRedditScript

outDir = './out/'
assetsDir = './assets/'

# create video
def createRedditVideo(name, data):
    video = Video(name, data)

    redditPost = makeRedditScript(video.path, data["subreddit"])

    print("Do you approve the script? respond \"y\" if yes")
    scriptApproval = input()

    if (scriptApproval == "y"):
        video.createAudio(redditPost['script'])
        video.createRedditVideo(redditPost, data)
    return video