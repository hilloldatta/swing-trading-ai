from setuptools import setup, find_packages

setup(
    name="swing-trading-ai",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai>=1.12.0",
        "python-dotenv>=1.0.0",
        "pytest>=8.0.0",
        "pytest-mock>=3.12.0",
    ],
) 