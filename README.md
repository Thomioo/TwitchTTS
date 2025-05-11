# TwitchTTS

TwitchTTS is a simple web application that allows Twitch chat to interact with the streamer using text-to-speech (TTS) commands. This tool creates a fun and engaging way for streamers to communicate with their audience.

## Features

- **Twitch Chat Integration**: Listens to chat messages in real-time.
- **Text-to-Speech (TTS)**: Converts chat messages into speech that the streamer can hear.
- **Custom Commands**: Supports specific commands to control the behavior of the application.

---

## Installation

To get started with TwitchTTS, follow these steps:

### Prerequisites

Make sure you have the following installed on your system:
- **Python 3.8 or higher**
- **pip** (Python package manager)
- Twitch account for the bot

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ToranProjects/TwitchTTS.git
   cd TwitchTTS
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration**:
   - edit config.json with your own credentials twitch token and stuff you can get at https://twitchtokengenerator.com and elevenlabs api key at https://elevenlabs.io/
   ---
   ```bash
   nvim config.json
   ```
   
---

## Usage

Once the installation is complete, you can start the application:

1. **Run the app**:
   ```bash
   python app.py
   ```

2. **Interact through Twitch chat**:
   - Open your Twitch channel.
   - Send commands in chat to test the TTS functionality. 
   
   Example:
   ```
   !say voice=1 Hello There!
   ```

3. **Stop the application**:
   Press `Ctrl+C` in the terminal to stop the server.

---

## Contribution

Contributions are welcome! If you want to improve this project, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Made by Tomesh, inspired by https://www.twitch.tv/theprimeagen
