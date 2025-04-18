"""Utilities for interacting with LLM APIs."""

import concurrent.futures
import time
from typing import List, Dict, Optional, Callable
from tqdm import tqdm
from openai import OpenAI, OpenAIError
from openai.types.chat import ChatCompletion


def multithread_openai_chat_completions_call(
    client: OpenAI,
    messages: List[List[Dict[str, str]]],
    model_name: str,
    max_workers: int = 20,
    max_retries: int = 3,
    retry_delay: float = 0.5,
    error_handler: Optional[Callable] = None,
    **kwargs
) -> List[Optional[ChatCompletion]]:
    """Make parallel [OpenAI API chat completions](https://platform.openai.com/docs/api-reference/chat) calls using multiple threads.
    Raw openai chat completion API only supports single message, this function will return a list of responses in the same order as input messages.
    
    Args:
        client: OpenAI client instance
        messages: List of message lists to process
        model_name: Name of the model to use
        max_workers: Maximum number of worker threads
        max_retries: Maximum number of retry attempts for failed requests
        retry_delay: Delay between retry attempts in seconds
        error_handler: Optional custom error handler function
        **kwargs: Additional arguments to pass to the API call
        
    Returns:
        List[Optional[ChatCompletion]]: List of complete OpenAI API response objects in the same order as input messages.
        See https://platform.openai.com/docs/api-reference/chat/object for response structure details.
        If a request fails after all retries, None will be returned at that position.
        
    Example:
        >>> responses = multithread_openai_chat_completions_call(client, messages, "gpt-3.5-turbo")
        >>> # Get message content from the first response
        >>> content = responses[0].choices[0].message.content
        >>> # Get token usage from the first response
        >>> total_tokens = responses[0].usage.total_tokens
    """
    def call_openai_with_retry(message: List[Dict[str, str]], **kwargs) -> Optional[ChatCompletion]:
        """Call the OpenAI API with retry logic."""
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=model_name, 
                    messages=message,
                    **kwargs
                )
                return response
                    
            except OpenAIError as e:
                if error_handler:
                    error_handler(e, attempt, message)
                # If this is our last attempt, either raise or return None
                if attempt == max_retries - 1:
                    return None
                # Wait with exponential backoff
                time.sleep(retry_delay * (2 ** attempt))
        
        return None  # Should not reach here but added for safety

    responses = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_message = {
            executor.submit(call_openai_with_retry, message, **kwargs): i 
            for i, message in enumerate(messages)
        }
        
        with tqdm(total=len(messages), desc="Processing messages") as pbar:
            for future in concurrent.futures.as_completed(future_to_message):
                message_idx = future_to_message[future]
                try:
                    response = future.result()
                    responses.append((message_idx, response))
                except Exception as e:
                    print(f"Request {message_idx} failed with error: {e}")
                    responses.append((message_idx, None))
                pbar.update(1)
    
    # Sort responses to match the order of input messages
    responses.sort(key=lambda x: x[0])
    return [r[1] for r in responses]


def default_error_handler(error: Exception, attempt: int, message: List[Dict[str, str]]) -> None:
    """Default error handler for API calls.
    
    Args:
        error: The exception that was raised
        attempt: The current retry attempt (0-indexed)
        message: The message that caused the error
    """
    print(f"Error on attempt {attempt + 1}: {error}. Retrying...") 