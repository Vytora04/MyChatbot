# MyChatbot

A simple Python-based chatbot project.

## Features
- Plain Python implementation (100% Python)
- Uses local LLMs via Ollama
- Supports multiple models: `mistral`, `phi3.5`, and `qwen3:4b`
- Easy to run locally and extend with your own intents/handlers

## Prerequisites
- Python 3.10+ installed
- Ollama installed and running

## Setup

```bash
# Clone the repository
git clone https://github.com/Vytora04/MyChatbot.git
cd MyChatbot

# (Optional) Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies (if a requirements.txt exists)
pip install -r requirements.txt
```

## Ollama Setup

- Install Ollama:
  - macOS/Linux:
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```
  - Windows:
    - Install via Winget:
      ```powershell
      winget install Ollama.Ollama
      ```
    - Or download from the official site: https://ollama.com/download

- Ensure the Ollama service is running:
  - macOS/Windows: starts automatically after install (or open the Ollama app)
  - Linux:
    ```bash
    ollama serve
    ```

- Pull the required models:
  ```bash
  ollama pull mistral
  ollama pull phi3.5
  ollama pull qwen3:4b
  ```

Note: Model tags can change over time. If a tag isn’t found, check the latest names in the Ollama library and adjust accordingly.

## Running

```bash
# Adjust the entry point if your file is named differently (e.g., app.py)
python main.py
```

- Make sure Ollama is running before starting the app.
- If the app supports choosing a model (e.g., via environment variable or config), set it accordingly, for example:
  ```bash
  # Example; update to match the app’s actual configuration
  export OLLAMA_MODEL=mistral
  # or
  export OLLAMA_MODEL=phi3.5
  # or
  export OLLAMA_MODEL=qwen3:4b
  ```

## Configuration
- If your bot uses environment variables, create a `.env` file and load it (e.g., with `python-dotenv`).
- Update intents, responses, or model settings in the relevant Python modules.

## Project Structure (example)
```
MyChatbot/
├─ main.py           # Application entry point (may be app.py or similar)
├─ requirements.txt  # Dependencies (optional)
```

## Contributing
- Fork the repo and create a feature branch
- Submit a pull request with a clear description

## License
This project is provided as-is. Add a LICENSE file to specify terms.
