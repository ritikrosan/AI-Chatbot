# Voice Assistant (Python)

This project is a simple voice-activated personal assistant built with Python. It can perform tasks such as web search, weather updates, telling jokes, reading the news, setting reminders, and more using voice commands.

## Features

- **Voice Recognition:** Listens and converts speech to text using Google Speech Recognition.
- **Text-to-Speech:** Speaks responses using `pyttsx3`.
- **Wikipedia Search:** Summarizes information from Wikipedia.
- **Web Operations:** Opens Google, YouTube, performs web searches.
- **Weather Updates:** Scrapes Google to provide current weather.
- **News Headlines:** Fetches top news from Google News RSS.
- **Reminders:** Sets time-based reminders.
- **Jokes:** Tells random jokes using `pyjokes`.
- **System Control:** Supports commands like taking screenshots, locking, shutting down, and restarting the system.
- **Note Taking:** Can take and read back notes.
- **Basic Calculator:** Evaluates simple arithmetic expressions.
- **Dictionary Support:** Fetches word definitions from Merriam-Webster.

## Dependencies

Make sure to install the following Python packages before running:

```bash
pip install pyttsx3 SpeechRecognition wikipedia pyjokes pyautogui beautifulsoup4 requests
```

Also, `PyAudio` is required for microphone access:

```bash
pip install pyaudio
```

*Note: On some systems (like Windows), you might need to install `PyAudio` using a prebuilt binary or package manager.*

## Usage

1. Run the assistant using:

```bash
python assistant.py
```

2. Speak your command when prompted.

3. Say "exit" or "bye" to close the assistant.

## Example Commands

- "Search Wikipedia for Python"
- "Open YouTube"
- "What is the weather in New York?"
- "Tell me a joke"
- "Take a screenshot"
- "Set a reminder"
- "Calculate 23 + 7"

## Disclaimer

This assistant uses `eval()` for simple math evaluation. Avoid passing untrusted input to it.

## License

This project is open-source and free to use for educational purposes.
