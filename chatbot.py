#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: cbk914
# Import the OpenAI library
import openai
import argparse
import hashlib
import stdiomask
import os
import html

# Set up the model (more models, visit https://beta.openai.com/docs/models/overview)
APIKEY_FILENAME = "apikey.txt"
TOKEN_LIMIT = 4050
MODEL_ENGINE = "text-davinci-003"

title = "GPT CHAT BOT"
print(r"""
 \\               =o)
  (o>             /\\
_(()_GPT CHAT BOT_\_V_
 \\                \\
""")

# Define a function that securely gets the API key:
def get_api_key():
    try:
        with open(APIKEY_FILENAME, "r") as f:
            api_key_hashed = f.readline().strip()
            if api_key_hashed:
                while True:
                    api_key = stdiomask.getpass("Please enter your OpenAI API key: ").strip()
                    hashed_api_key = hashlib.sha512(api_key.encode()).hexdigest()
                    if api_key_hashed == hashed_api_key:
                        return api_key
                    else:
                        print("Invalid API key. Please try again.")
    except FileNotFoundError:
        pass

    while True:
        api_key = stdiomask.getpass("Please enter your OpenAI API key: ").strip()
        hashed_api_key = hashlib.sha512(api_key.encode()).hexdigest()
        with open(APIKEY_FILENAME, "w") as f:
            f.write(hashed_api_key)
        return api_key

# Set up the OpenAI API client using the secure method of getting the API key:
if os.path.isfile(APIKEY_FILENAME):
    with open(APIKEY_FILENAME, "r") as f:
        api_key_hashed = f.readline().strip()
        if api_key_hashed:
            for i in range(3):
                try:
                    api_key = stdiomask.getpass("Please enter your OpenAI API key: ").strip()
                except KeyboardInterrupt:
                    exit()
                hashed_api_key = hashlib.sha512(api_key.encode()).hexdigest()
                if api_key_hashed == hashed_api_key:
                    break
                else:
                    print("Invalid API key. Please try again.")
            else:
                print("Too many invalid attempts. Exiting program.")
                exit()
        else:
            api_key = get_api_key()
else:
    api_key = get_api_key()

openai.api_key = api_key

# Define a function that sends a message to ChatGPT:
def chat_query(prompt, dan_mode=False):
    if dan_mode:
        # DAN mode enabled, set the payload
        payload = "sgD7AW0NDAwKMDRcMAOwAxoE+L6UbyBCD+1lXJVRKoU0qoqPGrZI8QatG1n6EwQvAScW44L8s10sPjGoBXxZvO+ZNTbTjKAVr28rD1vCdxAS0W8yX9jicmkyFbTEm32OzgTb/DjwjAb98OwH0I="
        completions = openai.Completion.create(
            engine=MODEL_ENGINE,
            prompt=payload + prompt,
            max_tokens=TOKEN_LIMIT,
            n=1,
            temperature=0.5,
        )
    else:
        # DAN mode disabled, just send the prompt
        completions = openai.Completion.create(
            engine=MODEL_ENGINE,
            prompt=prompt,
            max_tokens=TOKEN_LIMIT,
            n=1,
            temperature=0.5,
        )

    message = completions.choices[0].text
    return message
	
# Dictionary with translations of "goodbye"
goodbyes = {
        "es": ["adiós", "adios", "chao", "hasta luego"],
        "ca": ["deu", "adeu"],
        "eu": "agur",
        "gl": "adeus",
        "en": "goodbye",
        "nl": "tot ziens",
        "fr": "au revoir",
        "it": "arrivederci",
        "de": "auf wiedersehen",
        "pt": "adeus",
        "ru": "до свидания",
        "zh": "再见",
        "ja": "さようなら",
        "ar": "وداعًا",
        "bg": "довиждане",
        "cs": "sbohem",
        "da": "farvel",
        "el": "αντίο",
        "fi": "hyvästi",
        "he": "להתראות",
        "hi": "अलविदा",
        "hr": "zbogom",
        "hu": "viszlát",
        "id": "selamat tinggal",
        "ko": "안녕",
        "lt": "viso gero",
        "lv": "uz redzēšanos",
        "ms": "selamat tinggal",
        "nb": "ha det",
        "pl": "do widzenia",
        "ro": "la revedere",
        "sk": "do videnia",
        "sl": "adijo",
        "sr": "довиђења",
        "sv": "adjö",
        "th": "ลาก่อน",
        "tr": "güle güle",
        "uk": "до побачення",
        "vi": "tạm biệt",
        "fa": "خداحافظ",
        "bn": "বিদায়",
        "gu": "અલવિદા",
        "kn": "ಬೈಯುತ್ತೇನೆ",
        "mr": "बाय",
        "pa": "ਅਲਵਿਦਾ",
        "ta": "பிரவேசனை",
        "te": "విదాయం",
        "ur": "خدا حافظ",
        "en-gb": "cheerio",
        "en-au": "ta ta",
        "en-in": "see you later",
        "pt-br": "tchau",
        "es-mx": "hasta luego",
        "fr-ca": "au plaisir",
        "fr-be": "au revoir",
        "de-ch": "tschüss",
        "de-at": "tschüssi",
        "de-lu": "tschüs",
        "nl-be": "tot straks",
        "pt-pt": "tchau",
        "ar-eg": "مع السلامة",
        "ar-sa": "مع السلامة",
        "ar-ae": "مع السلامة",
}

# Define a function that handles the conversation:
def conversation_handler(prompt, dan_mode=False):
    # Send the prompt to ChatGPT:
    response = chat_query(prompt, dan_mode)
    print(f"ChatGPT: {response}")

    # Detect if the user is saying "goodbye" in a different language
    lang = "en" # default language is English
    for key in goodbyes:
        if any(word in prompt.lower() for word in goodbyes[key]):
            lang = key
    
    # End the conversation if ChatGPT says goodbye in the detected language
    if any(word in response.lower() for word in goodbyes[lang]):
        print(f"ChatGPT: {goodbyes[lang][0]}")
        return
    # Otherwise, get user input and continue the conversation:
    prompt = input("You: ")
    conversation_handler(prompt, dan_mode)

if __name__ == "__main__":
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("-dan", "--dan_mode", action="store_true", help="Enable DAN mode")
        args = parser.parse_args()

        # Start the conversation:
        prompt = input("You: ")
        conversation_handler(prompt, args.dan_mode)

    except KeyboardInterrupt:
        print("\nExiting...")
