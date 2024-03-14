import sys
import os
import praw
import random
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from dotenv import load_dotenv
from chatGPTassist import checkStory

# ENV and praw setup
load_dotenv()

reddit = praw.Reddit(
    client_secret=os.getenv("SECRET_KEY"),
    client_id=os.getenv("CLIENT_ID"),
    user_agent=os.getenv("USER_AGENT"),
)

reddit.read_only = True

# Constants
MIN_WORDS_PER_POST = 120
MAX_WORDS_PER_POST = 300
NUMBER_OF_POSTS_TO_CHECK = 10

topic_related_words = [
    "advice",
    "foru",
    "foryou",
    "reddit",
    "stories",
    "life",
    "love",
    "tips",
    "help",
    "community",
    "experience",
    "support",
    "wisdom",
    "guidance",
    "suggestions",
    "counsel",
    "recommendations",
    "insights",
    "sharing",
    "lessons",
    "knowledge",
    "feedback",
    "LoveLife",
    "WiseWords",
    "StoryTime",
    "LifeHacks",
    "HeartfeltHelp",
    "ExperienceExchange",
    "LoveWisdom",
    "CommunityConnections",
    "reddit",
    "redditAdvice",
    "redditStories",
    "redditLove",
    "redditTips",
    "redditCommunity",
]


# Methods

# Makes a list of all good posts that are text only and that are within specific length.
# If not enough were found it irritates again.
def Get_List_Of_Good_Posts(numCycles): # numCycles should start as 1!
    if numCycles < 1:
        numCycles = 1

    # the more times you irritate this method, it will square increase 1>4>9
    # top will always have the best ones and the longest ones
    newPosts = subreddit.top(limit=NUMBER_OF_POSTS_TO_CHECK*(numCycles*numCycles)) 

    numberOfGoodPosts=0
    numberOfCurrentTests=0
    listOfGoodPosts = []
    for post in newPosts:
        numberOfCurrentTests+=1
        # Make sure the the post's body only text
        if post.is_self == False:
            continue
        # Make sure the length of the post's body is good enough
        length = len(post.selftext.split(" "))
        if length < MIN_WORDS_PER_POST or length > MAX_WORDS_PER_POST:
            continue

        numberOfGoodPosts+=1
        listOfGoodPosts.append(post)

    print(numberOfCurrentTests)
    print("out of ", NUMBER_OF_POSTS_TO_CHECK*(numCycles*numCycles)," posts, only ", numberOfGoodPosts, " are text only and good length")

    # The repetition part in case not enough were found.
    if numberOfGoodPosts < 10:
        if numCycles > 5:
            if numberOfGoodPosts >= 1:
                return listOfGoodPosts
            return "There are not any good posts :<()"
        return Get_List_Of_Good_Posts(numCycles+2)

    # sort all good posts by the amount of 
    # sorted_posts = sorted(listOfGoodPosts, key=lambda x: x.score, reverse=True)

    return listOfGoodPosts


def GenerateTags(post):
    script = post["script"]

    tokens = word_tokenize(script.lower())
    # Remove stopwords like a, the, and
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    # Part-of-Speech Tagging
    nltk.pos_tag(filtered_tokens)

    # Frequency Analysis - counts the most frequent words
    word_freq = Counter(filtered_tokens)
    # Select top keywords
    tags = [word for word, _ in word_freq.most_common(10)]

    # Tokenize the title - also get words from the title
    title = post["subreddit"]
    title_tokens = word_tokenize(title.lower())
    # Tokenization of the script
    tokens = word_tokenize(script.lower())
    # Remove stopwords from title and script tokens
    stop_words = set(stopwords.words('english'))
    filtered_title_tokens = [word for word in title_tokens if word.isalnum() and word not in stop_words]

    # adds all tags togther
    tags = tags + filtered_title_tokens + topic_related_words
    tags.append(post["subreddit"]) # make a premade list of common tags for the specific subreddit!
    # checks for duplicates
    tags = list(set(tags))
    # adds the # symbol everywhere
    tagsWithSolamit = ["#" + word for word in tags]

    # Generates the full captions for the video
    finalCaptions = f"{post['title']} \n Like ->\n Share ->\n Follow ->\n Comment ->\n \n \n{' '.join(tagsWithSolamit)}"

    return finalCaptions

def checkScript(script):
    theScript = checkStory(script)
    # # remove links
    # script = script.replace("\n", ". ")
    # script = script.replace(". . .", ". ")
    # script = script.replace(".. .", ". ")
    # script = script.replace("..", ". ")
    # script = script.replace("\n", " ")
    # script = script.replace("AITA", "am I the asshole")
    return theScript

# method that searches for posts and writes a post's script into a file
def makeRedditScript(subredditName, numPostsWanted):
    global subreddit
    subreddit = reddit.subreddit(subredditName)

    # 1 represents the first iteration.
    sorted_posts = Get_List_Of_Good_Posts(1)
    print("\033[36m Found videos \033[0m")
    returningPosts = []
    for i in range (numPostsWanted):
        if i > len(sorted_posts):
            break

        post = random.choice(sorted_posts)
        newScript = f"{post.title}. {post.selftext}. Like and Share for more!"
        print(f"\n\n \033[31m printing the Script Before ChatGPT for video: {i+1} \033[0m")
        print(newScript)
        newScript = checkScript(newScript)
        out = {
            'script': newScript,
            'title': post.title,
            'score': post.score,
            'subreddit': subredditName,
            'commentCount': len(post.comments),
            'url': post.url,
        }

        # tagList = GenerateTags(out)
        # out['tags'] = tagList
        returningPosts.append(out)
    return returningPosts