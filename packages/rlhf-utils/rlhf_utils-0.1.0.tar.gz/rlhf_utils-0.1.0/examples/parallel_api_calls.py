"""Example demonstrating parallel OpenAI API calls."""

import os
from openai import OpenAI
from rlhf_utils.online_server import multithread_openai_call

# Set your API key before running (or use environment variable)
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def main():
    client = OpenAI()  # Will use OPENAI_API_KEY from environment by default
    
    # Prepare multiple messages
    messages = [
        [{"role": "user", "content": "Explain quantum computing in one paragraph"}],
        [{"role": "user", "content": "Write a haiku about artificial intelligence"}],
        [{"role": "user", "content": "Recommend three sci-fi books about AI"}],
        [{"role": "user", "content": "Describe a Turing machine"}],
    ]
    
    # Make parallel API calls
    responses = multithread_openai_call(
        client=client,
        messages=messages,
        model_name="gpt-3.5-turbo",
        max_workers=4,
        temperature=0.7
    )
    
    # Process responses
    for i, response in enumerate(responses):
        print(f"\n--- Response {i+1} ---")
        print(response)
        print("-" * 40)

if __name__ == "__main__":
    main() 