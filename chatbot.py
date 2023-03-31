#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: cbk914
# Import the OpenAI library
import openai
import argparse
import hashlib
import stdiomask
import os
from dotenv import load_dotenv, set_key
import dotenv

# Set up the model (more models, visit https://beta.openai.com/docs/models/overview)
APIKEY_FILENAME = ".env"
# Max TOKEN_LIMIT 4087
TOKEN_LIMIT = 4050
MODEL_ENGINE = "gpt-3.5-turbo"

title = "GPT CHAT BOT"
print(r"""
 \\               =o)
  (o>             /\\
_(()_GPT CHAT BOT_\_V_
 \\                \\
""")

# Define a function that securely gets the API key (more secure):
def read_hashed_api_key():
    dotenv.load_dotenv()
    return os.getenv("OPENAI_API_KEY_HASHED")


def save_hashed_api_key(hashed_api_key):
    dotenv.set_key(APIKEY_FILENAME, "OPENAI_API_KEY_HASHED", hashed_api_key)


def ask_for_api_key():
    while True:
        api_key = stdiomask.getpass("Please enter your OpenAI API key: ").strip()
        hashed_api_key = hashlib.sha512(api_key.encode()).hexdigest()
        if read_hashed_api_key() == hashed_api_key:
            return api_key
        save_hashed_api_key(hashed_api_key)
        print("Invalid API key. Please try again.")
        
# Define a function that stores the API key in plaintext (less secure) 
# def read_api_key():
#    dotenv.load_dotenv()
#    return os.getenv("OPENAI_API_KEY")


# def save_api_key(api_key):
#    dotenv.set_key(APIKEY_FILENAME, "OPENAI_API_KEY", api_key)


# def ask_for_api_key():
#    api_key = stdiomask.getpass("Please enter your OpenAI API key: ").strip()
#    if read_api_key() is None:
#        save_api_key(api_key)
#    return api_key


# Set up the OpenAI API client using the secure method of getting the API key:
api_key = ask_for_api_key()
openai.api_key = api_key

# Define a function that sends a message to ChatGPT:
def chat_query(prompt):
    completions = openai.ChatCompletion.create(
        model=MODEL_ENGINE,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=TOKEN_LIMIT,
        n=1,
        temperature=0.5
    )

    message = completions.choices[0].message['content']
    return message

# Define a function that handles the conversation:
def conversation_handler(prompt):
    # Send the prompt to ChatGPT:
    response = chat_query(prompt)
    print(f"ChatGPT: {response}")

    goodbye_phrases = [
        "bye", "deu", "adios", "doei", "hasta la vista",
        "hasta luego", "ciao", "agur", "adeus", "tchau"
    ]    

    # End the conversation if any of the specified expressions are included in the user input:
    if any(phrase in prompt.lower() for phrase in goodbye_phrases):
        print("You ended the conversation.")
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
