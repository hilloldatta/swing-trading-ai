from setuptools import setup, find_packages

setup(
    name="swing-trading-ai",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "openai>=1.12.0",
        "python-dotenv>=1.0.0",
        "pytest>=8.0.0",
        "pytest-mock>=3.12.0",
        "yfinance>=0.2.18",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
    ],
)