
# from gpt4all import GPT4All
# # model = GPT4All(model_name='orca-mini-3b-gguf2-q4_0.gguf', allow_download=False)
# #orca-mini-3b-gguf2-q4_0.gguf

# def extract_text_within_quotes(text):
#     pattern = r"^(.*?)(?=\b(?:EDIT|UPDATE)\b)"

#     # Use re.search to find the first match of the pattern in the input text
#     match = re.search(pattern, text, re.DOTALL)  # re.DOTALL allows . to match newline characters

#     if match:
#         extracted_text = match.group(1).strip()  # Extract the matched text and strip any leading/trailing whitespace
#         return extracted_text
#     else:
#         return text

import re
from g4f.client import Client
from g4f.Provider import RetryProvider, Phind, FreeChatgpt, Liaobots, Bing
import g4f.debug
g4f.debug.logging = True

def remove_first_line(text):
    return '\n'.join(text.split('\n')[:-1])

def extract_text_between_backticks(text):
    pattern = r'```([\s\S]*?)```'  # Match everything between triple backticks, including newlines
    matches = re.findall(pattern, text)
    return ''.join(matches)

def checkStory(script):
    # return script
    print("\033[35m \n\n\n  working on chatGPT  \n\n\n")
    prompt1 = f"You are a professional Video Creator specializing in short two-minute videos featuring engaging stories. I'll provide you with a story, and then I'll guide you on enhancing it. Understand? Here's the story: {script}"
    prompt2=f"""Now that you're familiar with the story, follow these steps to enhance it:
                1. Correct spelling errors.
                2. Ensure sentence endings are refined without summarizing or omitting details.
                3. Add appropriate slang and eliminate any abbreviations. Don't make it romantic please, its not a book!
                4. Infuse a dramatic teenage tone while retaining the adult audience's engagement, with a powerful punchline.
                5. Remove any links.
                6. Expand the script to 250 words, retaining the hook and title.
                7. After all that if there is a section where the author responds to the comments regarding the post then remove it or even an EDIT or UPDATE part then find a way to blend it in nicely without explicitly saying Edit or Update so that the new script is one whole story.
                8. Ignore introductions unrelated to the story and reminders about offensive usage.
                9. Always end with the punchline, followed by "-Like and Share for more!-"

                Please ensure the final video script adheres to these instructions. """
    prompt3=f"Good, so now make this story 250 words please."
    # prompt4=f"""Ok. Now I want you to Learn these hooks and generate one that can fit the Story: 
    #             1. I can’t believe what I just discovered!
    #             2. This may be controversial but ___
    #             6. Everything you knew about ___ is 100% WRONG!
    #             11. Come with me to do ___
    #             16. Did you know that ___?
    #             21. This is the story of ___
    #             24. What would you do if ___?
    #             26. I discovered the secret to ___
    #             45. Don’t believe this ___ myth!
    #             47. This ___ will blow your mind!
    #             48. Is it just me, or ___""" 
    # prompt5=f"Good, now please incorporate the Hook at the beginning of the story. Then, return to me JUST and ONLY the STORY with the HOOK at the beginning. The story and hook should be encapsulated in backticks please! Do it please!"
    prompt5 = f"Great! Please return only the STORY encapsulated in backticks. Avoid any redundant conclusions or summaries at the end. Proceed, please!"

    client = Client(provider=RetryProvider([FreeChatgpt, Liaobots, Bing], shuffle=False))
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        # messages=[{"role": "user", "content": "Helllllllo"}],
        max_tokens=100000,
        # provider="ChatgptFree",
        messages=[{"role": "user", "content": prompt1},{"role": "user", "content": prompt2},{"role": "user", "content": prompt3},{"role": "user", "content": prompt5}],
    )

    betterTxt = extract_text_between_backticks(response.choices[0].message.content)
    betterTxt = remove_first_line(betterTxt)
    print("\033[32m" + betterTxt + "\033[0m")
    print("\n\n\n")

    if betterTxt == "":
        return checkStory(script)
    return f"{betterTxt} Like and Share for more!"


def removeStoryEndSummary(script):
    # return script
    print("\033[35m \n\n  working on chatGPT Remove Summary  \n\n")
    prompt1 = f"You are a professional Video Creator specializing in short two-minute videos featuring engaging stories. I'll provide you with a story, and then I'll guide you on enhancing it. Understand? Here's the story: {script}"
    prompt2=f"""Now that you're familiar with the story, follow these steps to enhance it:
                1. I want you to divide the script into 4 sections: beginning, middle, punchline, and conclusion.
                2. The conclusion is not always present but if it is I want you to completely remove it.
                3. That conclusion can look like any redundant conclusions or summaries at the end or even the theme or what one might learn from the video!
                4. Please END the story with the punchline please! 
                4. This is not for educational purposes, this is for a private use to feature an engaging story.
                5. Always end with the punchline, followed by "-Like and Share for more!-"
                6. for your reference, the conclusion is the part that comes right after the "-Like and Share for more!-"
                Please ensure the final video script adheres to these instructions. Never change any part of the first three sections, I need the beginning, middle and punchline only to remain the same. So you return only the story without the 4th section, the conclusion!
                Please return only the STORY encapsulated in backticks. Avoid any redundant conclusions or summaries at the end. Proceed, please!
                """

    client = Client(provider=RetryProvider([FreeChatgpt, Liaobots, Bing], shuffle=False))
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        # messages=[{"role": "user", "content": "Helllllllo"}],
        max_tokens=100000,
        # provider="ChatgptFree",
        messages=[{"role": "user", "content": prompt1},{"role": "user", "content": prompt2},],
    )

    betterTxt = extract_text_between_backticks(response.choices[0].message.content)
    print("\033[32m" + betterTxt + "\033[0m")
    print("\n\n")

    if betterTxt == "":
        return checkStory(script)
    return betterTxt



# script = """A lost dog strays into a jungle. A lion sees this from a distance and says with caution "this guy looks edible, never seen his kind before".. So the lion starts rushing towards the dog with menace. The dog notices and starts to panic but as he's about to run he sees some bones next to him and gets an idea and says loudly "mmm...that was some good lion meat!".

# The lion abruptly stops and says " woah! This guy seems tougher then he looks, I better leave while I can".

# Over by the tree top, a monkey witnessed everything. Evidently, the monkey realizes the he can benefit from this situation by telling the lion and getting something in return. So the monkey proceeds to tell the lion what really happened and the lion says angrily "get on my back, we'll get him together".

# So they start rushing back to the dog. The dog sees them and realized what happened and starts to panic even more. He then gets another idea and shouts "where the hell is that monkey! I told him to bring me another lion an hour ago..."

# Edit: OMG my first gold! Thank you!. Like and Share for more!"""
# checkStory(script)