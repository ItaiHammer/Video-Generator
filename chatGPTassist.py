
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

def remove_first_line(text):
    return '\n'.join(text.split('\n')[1:])

def extract_text_between_backticks(text):
    pattern = r'```([\s\S]*?)```'  # Match everything between triple backticks, including newlines
    matches = re.findall(pattern, text)
    return ''.join(matches)

def checkStory(script):
    # return script
    print("\033[35m \n\n\n  working on chatGPT  \n\n\n")
    prompt1=f"You are a professional Video Creator who specializes in short two minute videos about short stories. I will send you my story and then I will give you instructions on how to improve it, understood? Once you improve it according to my requests, you I will use it to generate a TikTok video. Here is my story, learn about it. : {script}"
    prompt2=f"""Now that you have learned this story I need you to follow these steps to generate me a better story!
                1. Enhance the given script to include spelling adjustments.
                2. Then correct sentence endings while never summarizing and keeping every detail from the story and the same perspective of the person speaking in the script.
                3. Follow it by incorporating slang and remove abbreviations.
                4. Then infuse a teenager's dramatic tone to your adult audience.
                5. After that maintain or increase the length of the script to about 250-500 words while retaining the hook and title.
                6. After all that if there is a section where the author responds to the comments regarding the post then remove it or even an EDIT or UPDATE part then find a way to blend it in nicely without explicitly saying Edit or Update so that the new script is one whole story.
                7. finish by ensuring each video ends with -Like and Share for more!-."""
    prompt3=f"Good, so now make this story 250-500 words please."
    prompt4=f"""Ok. Now I want you to Learn these hooks and generate one that can fit the Story: 
                1. I can’t believe what I just discovered!
                2. This may be controversial but ___
                4. I promise you’ve never seen anything like this before!
                6. Everything you knew about ___ is 100% WRONG!
                11. Come with me to do ___
                13. Do you have problems with ___?
                15. This is the only thing you need to know about ___!
                16. Did you know that ___?
                17. You don’t want to miss this!
                21. This is the story of ___
                24. What would you do if ___?
                25. Why does no one talk about ___?
                26. I discovered the secret to ___
                33. Are you tired of ___?
                36. This one simple mistake could be costing you ___
                42. This is why your ___ isn’t working!
                43. This hack changed my life!
                45. Don’t believe this ___ myth!
                46. Other ___ are lying to you!
                47. This ___ will blow your mind!
                48. Is it just me, or ___""" 
    prompt5=f"Good, now please incorporate the Hook at the beginning of the story. Then, return to me JUST and ONLY the STORY with the HOOK at the beginning. Please NEVER REPEAT INSTRUCTIONS!!!"

    client = Client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt1},{"role": "user", "content": prompt2},{"role": "user", "content": prompt3},{"role": "user", "content": prompt4},{"role": "user", "content": prompt5}],
    )
    print(client.chat)
    betterTxt = extract_text_between_backticks(remove_first_line(response.choices[0].message.content))
    print("\033[32m" + betterTxt + "\033[0m")
    print("\n\n\n\n\n")
    # for i in range(response.choices[0]):
    #     print(response.choices[0].message.content)
    #     print("\n\n\n\n")
    # print("\n")
    return betterTxt