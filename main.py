from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import uuid
import os
import threading
import importlib.util
import sys
import uvicorn

# Import and configure twitch-handler
def load_twitch_handler():
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to twitch-handler.py
    twitch_handler_path = os.path.join(current_dir, "twitch-handler.py")
    
    # Load the module
    spec = importlib.util.spec_from_file_location("twitch_handler", twitch_handler_path)
    twitch_handler = importlib.util.module_from_spec(spec)
    
    # Add the module to sys.modules
    sys.modules["twitch_handler"] = twitch_handler
    
    # Execute the module
    spec.loader.exec_module(twitch_handler)
    
    return twitch_handler

# Function to start the Twitch bot in a separate thread
def start_twitch_bot():
    twitch_handler = load_twitch_handler()
    print("Starting Twitch bot in a separate thread...")
    twitch_handler.main()

app = FastAPI()

# Static directory for HTML and audio files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Replace with your actual ElevenLabs API key and voice IDs
ELEVEN_API_KEY = ""
VOICE_IDS = [
    "uYFJyGaibp4N2VwYQshk", # Adam
    "OAAjJsQDvpg3sVjiLgyl", # Denisa
    "NHv5TpkohJlOhwlTCzJk"  # PawelTV
]

# Queues
QUEUE = []
HISTORY = []
AUTOPLAY = False

class Message(BaseModel):
    id: str
    msg: str
    filepath: str
    username: str

@app.get("/say")
def say(voice: int, stability: float, similarity_boost: float, msg: str, username: str):
    if voice < 0 or voice >= len(VOICE_IDS):
        return {"error": "Invalid voice index"}
    
    voice_id = VOICE_IDS[voice]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": msg,
        "model_id": "eleven_multilingual_v2",
        "language": "czech",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        return {"error": "TTS request failed"}
    
    uid = str(uuid.uuid4())
    os.makedirs("static/audio", exist_ok=True)
    path = f"static/audio/{uid}.mp3"
    with open(path, "wb") as f:
        f.write(response.content)
    
    message = Message(id=uid, msg=msg, filepath=path, username=username)
    QUEUE.append(message)
    return {"status": "queued", "id": uid}

@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse("static/index.html")

@app.get("/queue")
def get_queue():
    return QUEUE

@app.get("/history")
def get_history():
    return HISTORY

@app.post("/play/{msg_id}")
def play(msg_id: str):
    global QUEUE, HISTORY
    for i, msg in enumerate(QUEUE):
        if msg.id == msg_id:
            HISTORY.append(msg)
            del QUEUE[i]
            return {"played": msg.id}
    return {"error": "Message not found"}

@app.get("/toggle_autoplay")
def toggle_autoplay():
    global AUTOPLAY
    AUTOPLAY = not AUTOPLAY
    return {"autoplay": AUTOPLAY}

# Entry point for the application
if __name__ == "__main__":
    # Start the Twitch bot in a separate thread
    twitch_thread = threading.Thread(target=start_twitch_bot, daemon=True)
    twitch_thread.start()
    
    # Start the FastAPI server
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=42069)
