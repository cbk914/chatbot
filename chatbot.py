#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: cbk914
import openai
import hashlib
import stdiomask
import os
from dotenv import load_dotenv, set_key

load_dotenv()

APIKEY_ENV_VAR = "OPENAI_API_KEY"
TOKEN_LIMIT = 4050
MODEL_ENGINE = "text-davinci-003"

title = "GPT CHAT BOT"
print(r"""
 \\               =o)
  (o>             /\\
_(()_GPT CHAT BOT_\_V_
 \\                \\
""")

def get_api_key():
    while True:
        api_key = stdiomask.getpass("Please enter your OpenAI API key: ").strip()
        set_key(".env", APIKEY_ENV_VAR, api_key)
        return api_key

def setup_openai_api_client():
    api_key = os.getenv(APIKEY_ENV_VAR)

    if not api_key:
        api_key = get_api_key()

    openai.api_key = api_key

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

def conversation_handler(prompt):
    response = chat_query(prompt)
    print(f"ChatGPT: {response}")

    if "goodbye" in response.lower():
        return

    prompt = input("You: ")
    conversation_handler(prompt)

if __name__ == "__main__":
    try:
        setup_openai_api_client()
        prompt = input("You: ")
        conversation_handler(prompt)
    except KeyboardInterrupt:
        print("\nExiting...")
