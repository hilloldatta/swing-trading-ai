# Swing Trading AI

An AI-powered swing trading service that uses GPT to analyze and explain trading patterns.

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Development

Install the package in development mode:
```bash
pip install -e .
```

## Testing

Run the tests:
```bash
pytest -v tests/
```

Run integration tests:
```bash
pytest -v -m integration tests/
```
