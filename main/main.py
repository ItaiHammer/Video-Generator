import os
import json
import shutil
from projectManager import createRedditVideo, createScriptedVideo

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def run():
    print('Type your command below:')

    # best starter to create a vid is: createredditvideo jokes jokes y y y n n ZiaGamez 1 y n
    # starter to create a vid from script: scripts


    command = input().split(" ")

    if (command[0] == "dump"):
        dump()
    elif (command[0] == 'createredditvideo'):
        while len(command) <= 7:
            command.append(None)

        if command[1] == None: command[2] = "video"
        if command[2] == None: command[2] = "shortStories"
        if (command[8] == None): command[8] = ""
        if (command[9] == None): command[9] = 1

        name = command[1]

        data = {
            'type': 'reddit',
            'subreddit': command[2],
            'music': command[3] == 'y' or command[3] == 'yes',
            'subtitles': command[4] == 'y' or command[4] == 'yes',
            'upload': command[5] == 'y' or command[5] == 'yes',
            'chatGPT': command[6] == 'y' or command[6] == 'yes',
            'chatGPTImages': command[7] == 'y' or command[7] == 'yes',
            'watermark': command[8],
            'videoCount': int(command[9]),
            'makeVideo': command[10] == 'y' or command[10] == 'yes',
            'crop': command[11] == 'y' or command[11] == 'yes',
        }
        
        createRedditVideo(name, data)
    elif command[0] == "scripts":
        print("\033[32m going over files \033[0m")
        json_data = read_json_file(f"{os.path.dirname(os.path.dirname(__file__))}/scripts/scripts.json")
        
        createScriptedVideo(json_data)


def dump():
    outDir = f'{os.path.dirname(os.path.dirname(__file__))}/out/'
    for video in os.listdir(outDir):
        try:
            shutil.rmtree(f"{outDir}/{video}")
        except Exception as e:
            print(f'Failed to delete directory: {e}')


run()