import os
import shutil
from projectManager import outDir, createRedditVideo

def run():
    print('Type your command below:')

    command = input().split(" ")

    if (command[0] == "dump"):
        dump()
    elif (command[0] == 'createredditvideo'):
        while len(command) < 5:
            command.append(None)

        if command[1] == None: command[2] = "video"
        if command[2] == None: command[2] = "shortStories"
        # Convert command[5] to integer before assigning
        number_videos = int(command[4]) if command[4] is not None else 1

        name = command[1]

        data = {
            'type': 'reddit',
            'subreddit': command[2],
            'music': command[3] == 'y' or command[3] == 'yes',
            'captions': command[4] == 'y' or command[4] == 'yes',
            'numberVideos': number_videos
        }
        
        createRedditVideo(name, data)


def dump():
    for video in os.listdir(outDir):
        try:
            shutil.rmtree(f"{outDir}/{video}")
        except Exception as e:
            print(f'Failed to delete directory: {e}')


run()