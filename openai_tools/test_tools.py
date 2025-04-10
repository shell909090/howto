#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2025-03-15
@author: Shell.Xu
@copyright: 2025, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
from gevent import monkey
monkey.patch_all()

import os
import re
import sys
import json
import logging
import argparse
from os import path

import requests
from gevent.pool import Pool

# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}


def setup_logging(lv):
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(lv)


def fmt_openai_stat(usage):
    return f"total_tokens: {usage['total_tokens']}, prompt_tokens: {usage['prompt_tokens']}, completion_tokens: {usage['completion_tokens']}"


def openai_chat(messages, tools=None):
    headers = {
        'Content-Type': 'application/json',
    }
    if args.openai_apikey:
        headers['Authorization'] = f'Bearer {args.openai_apikey}'
    logging.info(f'send request to openai: {args.openai_endpoint} {args.model}')
    payload = {
        'model': args.model,
        'stream': False,
        'messages': messages,
    }
    if tools:
        payload['tools'] = tools
    resp = requests.post(f'{args.openai_endpoint}/chat/completions', headers=headers, json=payload)
    resp.raise_for_status()
    logging.info('received response from openai')
    data = resp.json()
    logging.info(fmt_openai_stat(data['usage']))
    return data


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true', help='debug mode')
    parser.add_argument('--log-level', '-l', default='INFO', help='log level')
    parser.add_argument('--ollama-endpoint', '-ae', default=os.getenv('OLLAMA_ENDPOINT'), help='ollama endpoint')
    parser.add_argument('--openai-endpoint', '-ie', default=os.getenv('OPENAI_ENDPOINT'), help='openai endpoint')
    parser.add_argument('--openai-apikey', '-ik', default=os.getenv('OPENAI_APIKEY'), help='openai apikey')
    parser.add_argument('--model', '-m', default=os.getenv('MODEL', 'deepseek-r1:14b'), help='model')
    parser.add_argument('--from-input', '-fi', action='store_true', help='read background from stdin')
    parser.add_argument('--max-context-length', '-c', type=int, default=16384, help='maximum context length')
    parser.add_argument('--remove-think', '-rt', action='store_true', help='remove think')
    parser.add_argument('--file', '-f', action='append', help='input file')
    parser.add_argument('--url', '-u', action='append', help='source url')
    parser.add_argument('--search-duckduckgo', '-ddgs', action='store_true', help='search duckduckgo as source')
    parser.add_argument('--search-engine-max-results', '-semr', type=int, default=5, help='max results for refer')
    parser.add_argument('rest', nargs='*', type=str)
    args = parser.parse_args()

    setup_logging(args.log_level.upper())

    if not args.ollama_endpoint and not args.openai_endpoint:
        args.ollama_endpoint = 'http://127.0.0.1:11434'

    messages = [
        {'role': 'user', 'content': '现在东京天气怎么样？'},
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. Chicago, IL"
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]

    data = openai_chat(messages, tools=tools)
    print(json.dumps(data, indent=2))

    if 'tool_calls' not in data['choices'][0]['message']:
        logging.error('no tool calls')
        logging.info(f"response: {data['choices'][0]['message']['content']}")
        raise Exception()

    tool_calls = data['choices'][0]['message']['tool_calls']

    messages.append(data['choices'][0]['message'])
    for tool_call in tool_calls:
        logging.info(f"start run tools: {tool_call['type']}, return 'Good'.")
        messages.append({
            'role': 'tool',
            'tool_call_id': tool_call['id'],
            'content': 'Good',
        })

    logging.debug(json.dumps(messages, indent=2))
    data = openai_chat(messages, tools=tools)
    print(json.dumps(data, indent=2))

    print(data['choices'][0]['message']['content'])


if __name__ == '__main__':
    main()
