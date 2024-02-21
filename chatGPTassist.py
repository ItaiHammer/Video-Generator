import re
from gpt4all import GPT4All
model = GPT4All(model_name='orca-mini-3b-gguf2-q4_0.gguf')

def extract_text_within_quotes(text):
    return re.findall(r'\n\n(.*)', text)

def checkStory(script):
    print("working on chatGPT")
    with model.chat_session():
        i = 0
        response1 = model.generate(prompt=f"Enhance the given script to include spelling adjustments, correct sentence endings while never summarizing, incorporate slang and remove abbreviations, infuse a teenager's dramatic tone, maintain or increase the length of the script while retaining the hook and title, if there is an EDIT or UPDATE part then remove it, and ensure each video ends with -Like and Share for more!-. answer to my prompt in double quotations: {script}", temp=0)        
        if len(model.current_chat_session[2]["content"]) < 120:
            response2 = model.generate(prompt=f"Remember to enhance this script and return in double quotations: {script}")
            i=i+1
        # response2 = model.generate(prompt=f"Remember to end the videos with 'Like and Share for more!'. Now I will send you my fake script and I want you to return only the script as answer to my prompt in double quotations: {script}")
        # response2 = model.generate(prompt=f"Now I want you to find me 6 of the best hashtags which I can use to ")
        print(model.current_chat_session)
        assistant_responses = [item['content'] for item in model.current_chat_session if item['role'] == 'assistant']
        # betterTxt = extract_text_within_quotes(assistant_responses[i])
        # if len(betterTxt) == 0:
        #     response3 = model.generate(prompt=f"Remember to enhance this script and return in double quotations: {script}")
        #     i=i+1
        #     assistant_responses = [item['content'] for item in model.current_chat_session if item['role'] == 'assistant']
        betterTxt = extract_text_within_quotes(assistant_responses[i])[0]


        print(betterTxt)
        print("\n")
        if betterTxt.index("Like and Share for more!") != -1:
            print("Nope Nope")
            betterTxt = f"{betterTxt} Like and Share for more!"
        print(betterTxt)
        print("\n")
        return betterTxt