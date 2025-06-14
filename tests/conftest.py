import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def load_env():
    """Automatically load environment variables for all tests."""
    load_dotenv() 