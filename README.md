# Practice: OpenAI Agents Example

This project demonstrates the use of the `openai-agents` library to build AI-powered agents with Python. It includes two main scripts:

- `main.py`: An interactive assistant that answers user questions and demonstrates tool usage.
- `guardrails.py`: An example of using input guardrails to restrict agent behavior (e.g., only answer math homework questions).

## Features

- **Agent-based architecture** using the `openai-agents` library
- **Custom tools** for agent augmentation
- **Input guardrails** to control agent responses
- **Streaming responses** for interactive user experience

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (for dependency and environment management)
- [openai-agents](https://pypi.org/project/openai-agents/) >= 0.0.16
- An API key for [GROQ](https://groq.com/) (for Llama model access)

## Setup

> **Note:** This project uses [uv](https://github.com/astral-sh/uv) as the package manager. If you don't have it installed, follow the [uv installation guide](https://github.com/astral-sh/uv#installation).

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd practice
   ```
2. **Install dependencies and create virtual environment**
   ```sh
   uv venv
   uv sync
   ```
   Activate the virtual environment:
   - On Unix/macOS:
     ```sh
     source .venv/bin/activate
     ```
   - On Windows:
     ```sh
     .venv\Scripts\activate
     ```
3. **Set up environment variables**
   Create a `.env` file in the project root with the following content:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

### Run the Interactive Assistant

```sh
uv run main.py
```

- Enter your questions at the prompt.
- Type `exit` to quit.

### Run the Guardrails Example

```sh
uv run guardrails.py
```

- Demonstrates input guardrails for math homework questions.

## Project Structure

- `main.py` – Interactive assistant with tool usage
- `guardrails.py` – Guardrails and input validation example
- `pyproject.toml` – Project metadata and dependencies
- `LICENCE` – MIT License

## License

This project is licensed under the MIT License. See the [LICENCE](LICENCE) file for details.
