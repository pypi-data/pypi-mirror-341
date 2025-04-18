"""Tests for the API utilities."""

import unittest
from unittest.mock import MagicMock, patch, call
from rlhf_utils.online_server import multithread_openai_chat_completions_call, default_error_handler


class TestMultithreadOpenAICall(unittest.TestCase):
    """Test the multithread_openai_call function."""
    
    @patch('concurrent.futures.ThreadPoolExecutor')
    def test_multithread_openai_call(self, mock_executor):
        """Test that the function returns response objects in the correct order."""
        # Mock setup
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "Test response"
        mock_response.choices = [mock_choice]
        mock_response.model = "test-model"
        mock_response.usage = MagicMock(
            completion_tokens=10,
            prompt_tokens=5,
            total_tokens=15
        )
        mock_client.chat.completions.create.return_value = mock_response
        
        # Test messages
        messages = [
            [{"role": "user", "content": "Test message 1"}],
            [{"role": "user", "content": "Test message 2"}],
        ]
        
        # Mock the async behavior
        mock_future = MagicMock()
        mock_future.result.return_value = mock_response
        mock_executor.return_value.__enter__.return_value.submit.return_value = mock_future
        
        # Call the function
        responses = multithread_openai_chat_completions_call(
            client=mock_client,
            messages=messages,
            model_name="test-model"
        )
        
        # Check the responses are complete objects
        self.assertEqual(len(responses), len(messages))
        for response in responses:
            self.assertEqual(response, mock_response)
            self.assertEqual(response.model, "test-model")
            self.assertEqual(response.choices[0].message.content, "Test response")
            self.assertEqual(response.usage.total_tokens, 15)

    @patch('time.sleep')
    def test_retry_logic(self, mock_sleep):
        """Test that retry logic works correctly."""
        # Mock setup
        mock_client = MagicMock()
        mock_error_handler = MagicMock()
        
        # Setup the API to fail twice then succeed
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Success after retry"))]
        side_effects = [
            Exception("API rate limit exceeded"),
            Exception("Server error"),
            mock_response
        ]
        mock_client.chat.completions.create.side_effect = side_effects
        
        # Test message
        message = [[{"role": "user", "content": "Test retry"}]]
        
        # Call the function with retry
        response = multithread_openai_chat_completions_call(
            client=mock_client,
            messages=message,
            model_name="test-model",
            max_retries=3,
            retry_delay=1.0,
            error_handler=mock_error_handler
        )
        
        # Check results
        self.assertEqual(response[0], mock_response)
        self.assertEqual(response[0].choices[0].message.content, "Success after retry")
        
        # Check that error handler was called for each failure
        self.assertEqual(mock_error_handler.call_count, 2)
        
        # Check that sleep was called with correct delays (exponential backoff)
        mock_sleep.assert_has_calls([call(1.0), call(2.0)])

    def test_default_error_handler(self):
        """Test the default error handler."""
        error = Exception("Test error")
        message = [{"role": "user", "content": "Test message"}]
        
        # This just makes sure it doesn't raise an exception
        default_error_handler(error, 0, message)
        default_error_handler(error, 1, message)


if __name__ == "__main__":
    unittest.main() 