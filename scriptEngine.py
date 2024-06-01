import sys
import os
import praw
import random
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
NUMBER_OF_POSTS_TO_CHECK = 3000

topic_related_words = [
    "advice",
    "funny",
    "reddit",
    "stories",
    "tips",
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
    # adds all tags togther
    tags = topic_related_words
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
def makeRedditScript(subredditName, numPostsWanted, isChatGPT):
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
        newScript = f"{post.title}. {post.selftext}."
        print(f"\n\n \033[31m printing the Script Before ChatGPT for video: {i+1} \033[0m")
        print(newScript)
        if isChatGPT == True:
            newScript = checkScript(newScript)
        out = {
            'script': newScript,
            'title': post.title,
            'score': post.score,
            'subreddit': subredditName,
            'commentCount': len(post.comments),
            'url': post.url,
        }

        tagList = GenerateTags(out)
        out['tags'] = tagList
        returningPosts.append(out)
    return returningPosts