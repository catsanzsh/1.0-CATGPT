#!/usr/bin/env python3

import os
import sys
import json
import requests
import argparse

# Set your LM Studio API endpoint to the correct endpoint
LM_STUDIO_API_URL = os.getenv('LM_STUDIO_API_URL', 'http://localhost:8080/v1/completions')

def make_request(prompt: str, max_tokens: int = 150) -> str:
    """
    Make a request to the LM Studio API and return the generated text.
    """
    payload = {
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": max_tokens,
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(LM_STUDIO_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get('choices', [{}])[0].get('text', '').strip()
    except requests.ConnectionError:
        print(f"Error: Unable to connect to LM Studio API at '{LM_STUDIO_API_URL}'. Please make sure the server is running.")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Error: An error occurred while making the request: {e}")
        if e.response is not None:
            print(f"Response content: {e.response.text}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Simple AI Assistant using LM Studio')
    parser.add_argument('prompt', type=str, nargs='*', help='The prompt you want to give to the AI.')
    args = parser.parse_args()

    if not args.prompt:
        print("Please provide a prompt for the AI.")
        sys.exit(1)
    else:
        prompt = ' '.join(args.prompt)

    print(f"Prompt:\n{prompt}\n")

    # Make request to the AI
    response_text = make_request(prompt)

    # Display the AI's response
    print("AI Response:")
    print(response_text)
    print("\n")

    print("Execution finished.")

if __name__ == "__main__":
    main()
