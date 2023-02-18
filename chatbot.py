#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: cbk914
import argparse
import requests
import json

class Chatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = 'https://api.openai.com/v1/engines/davinci-codex/completions'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        self.payload = {
            'temperature': 0.5,
            'max_tokens': 2048,
            'n': 1,
            'stop': ['\n']
        }

    def get_chatbot_response(self, input_text):
        if not input_text.strip():
            return "Sorry, I didn't catch that. Can you please rephrase your question?"

        self.payload['prompt'] = input_text
        response = requests.post(self.endpoint, data=json.dumps(self.payload), headers=self.headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data['choices'][0]['text'].strip()
        else:
            return 'Oops! Something went wrong.'

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--apikey', help='API key for ChatGPT', required=True)
args = parser.parse_args()

chatbot = Chatbot(api_key=args.apikey)

while True:
    user_input = input('You: ')
    chatbot_response = chatbot.get_chatbot_response(user_input)
    print('Chatbot:', chatbot_response)
