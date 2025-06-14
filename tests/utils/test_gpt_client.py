import pytest
from unittest.mock import patch, MagicMock
from utils.gpt_client import ask_gpt

def test_ask_gpt_success():
    # Mock response from OpenAI
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message={"content": "This is a test response"}
        )
    ]

    # Mock the OpenAI API call
    with patch('openai.ChatCompletion.create', return_value=mock_response):
        response = ask_gpt("Test prompt")
        assert response == "This is a test response"

def test_ask_gpt_with_custom_model():
    # Mock response from OpenAI
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message={"content": "This is a test response"}
        )
    ]

    # Mock the OpenAI API call
    with patch('openai.ChatCompletion.create', return_value=mock_response) as mock_create:
        response = ask_gpt("Test prompt", model="gpt-3.5-turbo")
        
        # Verify the correct model was used
        mock_create.assert_called_once()
        call_args = mock_create.call_args[1]
        assert call_args['model'] == "gpt-3.5-turbo"
        assert response == "This is a test response"

def test_ask_gpt_api_error():
    # Mock an API error
    with patch('openai.ChatCompletion.create', side_effect=Exception("API Error")):
        with pytest.raises(Exception) as exc_info:
            ask_gpt("Test prompt")
        assert str(exc_info.value) == "API Error" 