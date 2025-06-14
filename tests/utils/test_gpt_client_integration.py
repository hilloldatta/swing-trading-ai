import pytest
from utils.gpt_client import ask_gpt

@pytest.mark.integration
def test_ask_gpt_real_api():
    """Test actual API connectivity with OpenAI."""
    prompt = "Write a Python function to calculate the moving average of a list."
    
    try:
        response = ask_gpt(prompt)
        
        # Basic validation of the response
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Check if the response contains Python code
        assert "def" in response.lower()
        assert "return" in response.lower()
        
        print("\nGPT Response:\n")
        print(response)
        
    except Exception as e:
        pytest.fail(f"API call failed: {str(e)}")

@pytest.mark.integration
def test_ask_gpt_real_api_with_custom_model():
    """Test actual API connectivity with a different model."""
    prompt = "Write a simple Python function to add two numbers."
    
    try:
        response = ask_gpt(prompt, model="gpt-3.5-turbo")
        
        # Basic validation of the response
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Check if the response contains Python code
        assert "def" in response.lower()
        assert "return" in response.lower()
        
        print("\nGPT Response (gpt-3.5-turbo):\n")
        print(response)
        
    except Exception as e:
        pytest.fail(f"API call failed: {str(e)}") 