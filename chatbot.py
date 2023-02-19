#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: cbk914
# Import the OpenAI library
import openai
import argparse
import hashlib
import stdiomask
import os

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
                print("Invalid API key. Exiting program.")
                exit()
        else:
            api_key = get_api_key()
else:
    api_key = get_api_key()

openai.api_key = api_key

# Define a function that sends a message to ChatGPT:
def chat_query(prompt):
    completions = openai.Completion.create(
        engine=MODEL_ENGINE,
        prompt=prompt,
        max_tokens=TOKEN_LIMIT,
        n=1,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message


# Define a function that handles the conversation:
def conversation_handler(prompt):
    # Send the prompt to ChatGPT:
    response = chat_query(prompt)
    print(f"ChatGPT: {response}")

    # End the conversation if ChatGPT says goodbye:
    if "goodbye" in response.lower():
        return

    # Otherwise, get user input and continue the conversation:
    prompt = input("You: ")
    conversation_handler(prompt)


# Main program starts here:
if __name__ == "__main__":
    try:
        # Start the conversation:
        prompt = input("You: ")
        conversation_handler(prompt)
    except KeyboardInterrupt:
        print("\nExiting...")
