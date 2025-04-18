# RLHF-Utils

A Python package containing utilities for working with Large Language Models (LLMs).

## Installation

```bash
pip install rlhf-utils
```

## Features

- **Online Server Module**: Utilities for making API calls to LLM providers
  - Parallel OpenAI API calls using multithreading
  - Progress tracking for batch API requests

## Usage Examples

### Parallel OpenAI API Calls

```python
from rlhf_utils.online_server import multithread_openai_call
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="your-api-key")

# Define messages for multiple API calls
messages = [
    [{"role": "user", "content": "Explain quantum computing"}],
    [{"role": "user", "content": "Write a short poem about AI"}],
    [{"role": "user", "content": "Summarize the history of the internet"}]
]

# Make parallel API calls
responses = multithread_openai_call(
    client=client,
    messages=messages,
    model_name="gpt-3.5-turbo",
    max_workers=3
)

# Process responses
for i, response in enumerate(responses):
    print(f"Response {i+1}:\n{response}\n")
```

## License

MIT 