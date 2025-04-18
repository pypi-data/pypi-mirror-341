"""Example demonstrating parallel OpenAI API calls."""

import time
from openai import OpenAI
from rlhf_utils.online_server import multithread_openai_chat_completions_call

# Set your API key before running (or use environment variable)
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def custom_error_handler(error, attempt, message):
    """Custom error handler that logs additional information."""
    print(f"Error on attempt {attempt + 1} for message: '{message[0]['content'][:30]}...'")
    print(f"Error details: {error}")
    print(f"Retrying in {0.5 * (2 ** attempt):.2f} seconds...")

def compare_sequential_vs_parallel():
    """Compare sequential vs parallel API calls."""
    client = OpenAI()  # Will use OPENAI_API_KEY from environment by default
    
    # Prepare multiple messages
    messages = []
    for i in range(8):
        messages.append([{"role": "user", "content": f"Write a one-sentence definition of concept {i+1}: {['quantum computing', 'neural networks', 'blockchain', 'virtual reality', 'cloud computing', 'machine learning', 'artificial intelligence', 'internet of things'][i]}"}])
    
    print("Running sequential calls...")
    start_time = time.time()
    sequential_responses = []
    for message in messages:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message,
            temperature=0.7
        )
        sequential_responses.append(response.choices[0].message.content)
    sequential_time = time.time() - start_time
    print(f"Sequential time: {sequential_time:.2f} seconds")
    
    print("\nRunning parallel calls...")
    start_time = time.time()
    parallel_responses = multithread_openai_chat_completions_call(
        client=client,
        messages=messages,
        model_name="gpt-3.5-turbo",
        max_workers=8,
        temperature=0.7
    )
    # Extract content from the response objects
    parallel_contents = [response.choices[0].message.content for response in parallel_responses if response]
    parallel_time = time.time() - start_time
    print(f"Parallel time: {parallel_time:.2f} seconds")
    
    speedup = sequential_time / parallel_time
    print(f"Speedup: {speedup:.2f}x")
    
    return sequential_responses, parallel_contents

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
    print("\n--- Processing API Calls ---")
    responses = multithread_openai_chat_completions_call(
        client=client,
        messages=messages,
        model_name="gpt-3.5-turbo",
        max_workers=4,
        temperature=0.7,
        error_handler=custom_error_handler
    )
    
    # Process responses - showing how to access different parts of the response object
    for i, response in enumerate(responses):
        if response is None:
            print(f"\n--- Response {i+1}: Failed ---")
            continue
            
        print(f"\n--- Response {i+1} ---")
        # Extract content
        content = response.choices[0].message.content
        print(content)
        
        # Print useful metadata
        print(f"\nMetadata:")
        print(f"- Model: {response.model}")
        print(f"- Completion tokens: {response.usage.completion_tokens}")
        print(f"- Prompt tokens: {response.usage.prompt_tokens}")
        print(f"- Total tokens: {response.usage.total_tokens}")
        print(f"- Finish reason: {response.choices[0].finish_reason}")
        print("-" * 40)
    
    # Uncomment to compare sequential vs parallel performance
    # compare_sequential_vs_parallel()

if __name__ == "__main__":
    main() 