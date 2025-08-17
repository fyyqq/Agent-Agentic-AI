# Learning AI Agent & Agentic AI with Python

This project is a hands-on exploration of building AI agents and agentic AI systems using Python. It demonstrates how to interact with various AI APIs (OpenAI GPT-4, Claude, etc.), manage environment variables securely, and structure agentic workflows.

## Features
- Example code for calling GPT-4 and Claude APIs
- Secure API key management using `.env` files
- Demonstrates agentic AI patterns in Python

## Folder Structure
- `main.py` — Main script for running AI agent examples
- `.env` — Stores API keys (never push this file to GitHub!)
- Other supporting files and scripts

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/fyyqq/Agent-Agentic-AI.git
   cd Agent-Agentic-AI
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add API keys:
   ```
   OPENAI_API_KEY=your_openai_key
   CLAUDE_API_KEY=your_claude_key
   GPT_4_API_KEY=your_gpt4_key
   ```

## Usage

Run the main script:
```
python main.py
```

## Notes
- **Do not commit your `.env` file to GitHub.** Add `.env` to `.gitignore`.
- Make sure you have valid API keys for the services you want to use.

## License
This project is for learning purposes.
