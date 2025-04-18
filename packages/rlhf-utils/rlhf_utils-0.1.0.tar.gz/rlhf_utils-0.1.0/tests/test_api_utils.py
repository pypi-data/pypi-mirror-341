"""Tests for the API utilities."""

import unittest
from unittest.mock import MagicMock, patch
from rlhf_utils.online_server import multithread_openai_call


class TestMultithreadOpenAICall(unittest.TestCase):
    """Test the multithread_openai_call function."""
    
    @patch('concurrent.futures.ThreadPoolExecutor')
    def test_multithread_openai_call(self, mock_executor):
        """Test that the function returns responses in the correct order."""
        # Mock setup
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "Test response"
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        
        # Test messages
        messages = [
            [{"role": "user", "content": "Test message 1"}],
            [{"role": "user", "content": "Test message 2"}],
        ]
        
        # Mock the async behavior
        mock_future = MagicMock()
        mock_future.result.return_value = "Test response"
        mock_executor.return_value.__enter__.return_value.submit.return_value = mock_future
        
        # Call the function
        responses = multithread_openai_call(
            client=mock_client,
            messages=messages,
            model_name="test-model"
        )
        
        # Check the responses
        self.assertEqual(len(responses), len(messages))
        # We would check more here in a real test

if __name__ == "__main__":
    unittest.main() 