# Guide For Devs

🚀 Introducing **[App Name]** - Your Reddit Stories, Your TikTok Moments! 🎉

# Reddit API

We use the official reddit API for all of our program's purposes.

You can find the official API page on this **[website](https://www.reddit.com/prefs/apps)**

# Dependencies

1.  python-dotenv - Enviroment Variables
2.  praw - Reddit Scraper
3.  pyttsx3 - Speech Synthesizer 1
4.  gTTS - Speech Synthesizer 2
5.  elevenlabs - Speech Synthesizer 3
6.  moviepy - Video Editor
7.  nltk - The Natural Language Toolkit

Install Command
    `pip install python-dotenv elevenlabs praw pyttsx3 gTTS moviepy g4f[all] opencv-python`

Follow these instructions as well from (make sure you have NodeJS and npm installed): https://github.com/makiisthenes/TiktokAutoUploader 
    `cd TiktokAutoUploader`
    `pip install -r requirements.txt`
    `cd tiktok_uploader/tiktok-signature/`
    `npm i`

First and maybe second time when running code it will never work, give it a minute and then try again, it will work immediately!

When running, make sure the load_env has or does't have "utf-16" for the program to work in all instances!