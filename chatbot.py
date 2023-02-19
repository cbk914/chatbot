#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: cbk914
# Import the OpenAI library
import openai
import argparse

title = "GPT CHAT BOT"
print(r"""
 \\               =o) 
 (o>              /\\ 
_(()_GPT CHAT BOT_\_V_
 //                \\ 
                    \\
""")

# Define a function that securely gets the API key
def get_api_key():
    try:
        with open("apikey.txt", "r") as f:
            api_key = f.readline().strip()
            if api_key:
                return api_key
    except FileNotFoundError:
        pass

    api_key = input("Please enter your OpenAI API key: ").strip()
    with open("apikey.txt", "w") as f:
        f.write(api_key)
    return api_key

# Set up the OpenAI API client using the secure method of getting the API key:
openai.api_key = get_api_key()

# Set up the model (more models, visit https://beta.openai.com/docs/models/overview)
model_engine = "text-davinci-003"


# Define a function that sends a message to ChatGPT
def chat_query(prompt):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        n=1,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message


# Define a function that handles the conversation
def conversation_handler(prompt):
    # Send the prompt to ChatGPT
    response = chat_query(prompt)
    print(f"ChatGPT: {response}")
    
    # End the conversation if ChatGPT says goodbye
    if "goodbye" in response.lower():
        return
    
    # Otherwise, get user input and continue the conversation
    prompt = input("You: ")
    conversation_handler(prompt)


# Main program starts here:
if __name__ == "__main__":
    # Define the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--apikey", help="OpenAI API key")
    args = parser.parse_args()

    # Use the command-line API key if provided, otherwise get it securely
    if args.apikey:
        openai.api_key = args.apikey
    else:
        openai.api_key = get_api_key()

    # Example of prompt to query
    prompt = "GPT-3 vs ChatGPT: What is the difference?"

    # Start the conversation
    conversation_handler(prompt)
