# Tourism Bot using Mistral AI

## Overview
A secure, simple Python chatbot for tourism recommendations using Mistral AI.

## Setup
1. Create a virtual environment and activate it.
2. Copy `.env.example` to `.env` and add your Mistral API key.
3. Install dependencies: `pip install -r requirements.txt`
4. Run the bot: `python src/bot.py`

## Security Notes
- Never commit secrets or API keys to the repository.
- All configuration is managed via environment variables.
- User data is never logged or stored.

## Project Structure
- `src/`: Source code
- `config/`: Configuration (no secrets)
- `tests/`: Test scripts
