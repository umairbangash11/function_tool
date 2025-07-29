# Function Tool Example

This project demonstrates how to use a function-calling agent with Gemini (Google AI) via an OpenAI-compatible API, using Python. It includes example function tools and a simple agent setup.

## Features
- Uses Gemini API with OpenAI-compatible endpoints
- Example function tools (`get_weather`, `piaic`)
- Agent that can answer questions using these tools

## Setup

1. **Clone the repository**
2. **Install dependencies** (using [uv](https://github.com/astral-sh/uv) or pip):
   ```sh
   uv pip install -r requirements.txt
   # or
   pip install -r requirements.txt
   ```
3. **Create a `.env` file** in the project root with your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

Run the main script:
```sh
uv run main.py
# or
python main.py
```

You should see output like:
```
umair is enrolled in PIAIC.
```

## Example Function Tools
- `get_weather(city: str)`: Returns simulated weather for a city.
- `piaic(student_name: str)`: Returns simulated PIAIC enrollment info for a student.

## Notes
- This is a template/example. Replace the function tools with your own logic as needed.
- Requires a valid Gemini API key.
