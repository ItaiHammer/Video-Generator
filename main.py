import os
import shutil
from projectManager import outDir, createRedditVideo

def run():
    print('Type your command below:')

    command = input().split(" ")

    if (command[0] == "dump"):
        dump()
    elif (command[0] == 'createredditvideo'):
        name = command[1]
        data = {
            'type': 'reddit',
            'subreddit': command[2],
            'music': command[3] == 'y' or command[3] == 'yes'
        }
        
        createRedditVideo(name, data)


def dump():
    for video in os.listdir(outDir):
        try:
            shutil.rmtree(f"{outDir}/{video}")
        except Exception as e:
            print(f'Failed to delete directory: {e}')


run()