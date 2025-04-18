# RLHF-Utils

[![PyPI version](https://badge.fury.io/py/rlhf-utils.svg)](https://badge.fury.io/py/rlhf-utils)
[![Python Versions](https://img.shields.io/pypi/pyversions/rlhf-utils.svg)](https://pypi.org/project/rlhf-utils/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A streamlined Python toolkit for building and working with Large Language Models (LLMs), designed for researchers and engineers.

## 🚀 Installation

```bash
pip install rlhf-utils
```

## ✨ Features

- **Online Server Module**: Efficient utilities for LLM API integrations
  - ⚡ Parallel OpenAI API calls with multithreading
  - 📊 Built-in progress tracking for batch requests
  - 🛡️ Error handling and retry logic
  - 🔄 Complete API response access

## 🔍 Usage Examples

### Parallel OpenAI API Calls

Process multiple prompts simultaneously with optimal resource utilization:

```python
from rlhf_utils.online_server import multithread_openai_chat_completions_call
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="your-api-key")

# Define messages for multiple API calls
messages = [
    [{"role": "user", "content": "Explain quantum computing"}],
    [{"role": "user", "content": "Write a short poem about AI"}],
    [{"role": "user", "content": "Summarize the history of the internet"}]
]

# Make parallel API calls (returns complete response objects)
responses = multithread_openai_chat_completions_call(
    client=client,
    messages=messages,
    model_name="gpt-3.5-turbo",
    max_workers=3
)

# Access response data
for i, response in enumerate(responses):
    if response is None:
        print(f"Request {i} failed")
        continue
        
    # Get the generated content
    content = response.choices[0].message.content
    print(f"Response {i+1}:\n{content}\n")
    
    # Access metadata like token usage
    print(f"Total tokens: {response.usage.total_tokens}")
```

### Working with Response Objects

The function returns complete [OpenAI ChatCompletion](https://platform.openai.com/docs/api-reference/chat/object) objects with all API response data:

```python
# Access different parts of the response
response = responses[0]  # First response

# Message content
content = response.choices[0].message.content

# Token usage
completion_tokens = response.usage.completion_tokens
prompt_tokens = response.usage.prompt_tokens
total_tokens = response.usage.total_tokens

# Model information
model = response.model

# Other metadata
finish_reason = response.choices[0].finish_reason
```

### Performance Benchmarking

The parallel implementation offers significant speedups:

- Processing 10 prompts sequentially: ~20 seconds
- With `multithread_openai_chat_completions_call`: ~3 seconds

## 🛠️ For Developers

Clone the repository to contribute:

```bash
git clone https://github.com/yourusername/rlhf-utils.git
cd rlhf-utils
pip install -e .
```

Run tests:

```bash
python -m unittest discover tests
```

## 📝 License

MIT 