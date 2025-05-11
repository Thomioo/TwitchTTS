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
- [Twitch Developer Account](https://dev.twitch.tv/) (to set up API credentials)

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
   - Create a `.env` file in the root directory of the project.
   - Add the following variables:
     ```env
     TWITCH_CLIENT_ID=your_twitch_client_id
     TWITCH_CLIENT_SECRET=your_twitch_client_secret
     TWITCH_BOT_TOKEN=your_twitch_bot_token
     TWITCH_CHANNEL=your_twitch_channel
     ```
   Replace `your_twitch_client_id`, `your_twitch_client_secret`, `your_twitch_bot_token`, and `your_twitch_channel` with your actual Twitch API credentials.

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
   !speak Hello, streamer!
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

Let me know if you'd like to customize or expand any section of this README!
