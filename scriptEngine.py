import sys
import os
import praw
import random
from dotenv import load_dotenv

# ENV and praw setup
load_dotenv(encoding="utf-16")

reddit = praw.Reddit(
    client_secret=os.getenv("SECRET_KEY"),
    client_id=os.getenv("CLIENT_ID"),
    user_agent=os.getenv("USER_AGENT"),
)

reddit.read_only = True

# Constants
MIN_WORDS_PER_POST = 35
MAX_WORDS_PER_POST = 160
NUMBER_OF_POSTS_TO_CHECK = 10000


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
        if numCycles > 3:
            return "There are not any good posts :<()"
        Get_List_Of_Good_Posts(numCycles+0.5)

    # sort all good posts by the amount of 
    # sorted_posts = sorted(listOfGoodPosts, key=lambda x: x.score, reverse=True)

    return listOfGoodPosts

# method that searches for posts and writes a post's script into a file
def makeRedditScript(path, subredditName):
    file = open(f"{path}/script.txt", 'a')
    global subreddit
    subreddit = reddit.subreddit(subredditName)

    # path: "./out/videoName/"
    # Check if there's already a file for this subreddit
    # subreddit_file_path = f"./assets//{subredditName}.json"
    # if os.path.exists(subreddit_file_path):
    #     # If the file exists, read the list of posts from it
    #     with open(subreddit_file_path, 'r') as subreddit_file:
    #         sorted_posts = json.load(subreddit_file)
    # make sure u don't run this every time and just pick a random one out of the list we have.

    # 1 represents the first iteration.
    sorted_posts = Get_List_Of_Good_Posts(1)
    post = random.choice(sorted_posts)
    # if type(sorted_posts) == "<class 'str'>":
    #     print(sorted_posts)
    # else:
    #     for post in sorted_posts[:2]:
    #         print("\n")
    #         print("Title -", post.title)
    #         print("URL -", post.url)
    #         print("Score -", post.score)
    #         print(post.selftext)
    #         # for comment in post.comments[:2]: # first couple of comments
    #         #     print(comment.body)

    file.write(post.selftext)
    file.close()

    out = {
        'script': post.selftext,
        'title': post.title,
        'score': post.score,
        'subreddit': subredditName,
        'commentCount': len(post.comments),
        'url': post.url,
    }
    
    return out