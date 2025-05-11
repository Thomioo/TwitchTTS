import socket
import re
import time
import threading
import requests
import urllib.parse

# Twitch IRC server details
SERVER = 'irc.chat.twitch.tv'
PORT = 6667

# Replace these with your bot's Twitch username and OAuth token (include 'oauth:' prefix)
BOT_NICK = ''         # e.g. 'mybot'
BOT_OAUTH = 'oauth:'  # e.g. 'oauth:abcd1234...'

# The channel to join (your Twitch channel, with # prefix)
CHANNEL = ''         # e.g. '#mychannel'

# TTS API settings (default values)
TTS_SERVER = "http://localhost:42069"  # Update with your server address and port
DEFAULT_VOICE = 0  # 0=Adam, 1=Denisa, 2=PawelTV
DEFAULT_STABILITY = 0.5
DEFAULT_SIMILARITY = 0.75
# Czech language is set in the main.py server

def send_message(sock, message):
    """
    Send a message to the Twitch chat.
    """
    message_temp = f"PRIVMSG {CHANNEL} :{message}\r\n"
    print(f"Sending message: {message_temp.strip()}")
    sock.send(message_temp.encode('utf-8'))
    time.sleep(1)  # Sleep to avoid Twitch rate limits

def process_say_command(username, message):
    """
    Process the !say command and its parameters.
    Format: !say [voice:0-2] [stability:0.0-1.0] [similarity:0.0-1.0] message
    Or just: !say message (uses default voice and settings)
    
    Special command format: !say voice=N stability=X similarity=Y message
    Example: !say voice=2 similarity=0.8 This is my message
    """
    # Default values
    voice = DEFAULT_VOICE
    stability = DEFAULT_STABILITY
    similarity = DEFAULT_SIMILARITY
    
    # Strip the !say part to get just the message and parameters
    command_text = message[4:].strip()
    
    # Check for key=value style parameters
    params = {}
    words = command_text.split()
    text_to_say_parts = []
    for word in words:
        if "=" in word and not word.startswith('"') and not word.startswith("'"):
            key, value = word.split("=", 1)
            key = key.lower()
            if key in ['voice', 'stability', 'similarity']:
                try:
                    params[key] = float(value) if key != 'voice' else int(value)
                except ValueError:
                    # If conversion fails, treat it as part of the message
                    text_to_say_parts.append(word)
        else:
            text_to_say_parts.append(word)
    
    # Apply key=value style parameters if found
    if 'voice' in params and 0 <= params['voice'] <= 2:
        voice = params['voice']
    if 'stability' in params and 0 <= params['stability'] <= 1:
        stability = params['stability']
    if 'similarity' in params and 0 <= params['similarity'] <= 1:
        similarity = params['similarity']
    
    # Check if we have a positional style command instead
    if not params and command_text:
        # Extract parameters if provided in positional format
        parts = command_text.split(maxsplit=3)
        
        try:
            # Check if first parameter is voice
            if parts and parts[0].isdigit() and 0 <= int(parts[0]) <= 2:
                voice = int(parts[0])
                parts = parts[1:]  # Remove processed part
            
            # Check if next parameter is stability
            if parts and parts[0].replace('.', '', 1).isdigit():
                stab_val = float(parts[0])
                if 0 <= stab_val <= 1:
                    stability = stab_val
                    parts = parts[1:]  # Remove processed part
            
            # Check if next parameter is similarity
            if parts and parts[0].replace('.', '', 1).isdigit():
                sim_val = float(parts[0])
                if 0 <= sim_val <= 1:
                    similarity = sim_val
                    parts = parts[1:]  # Remove processed part
            
            # The remaining text is the message to say
            text_to_say_parts = parts
        except (ValueError, IndexError):
            # If parsing fails, use the entire text after !say
            text_to_say_parts = [command_text]
    
    # Join any remaining parts as the message
    text_to_say = " ".join(text_to_say_parts).strip()
    
    # Make sure we actually have a message
    if not text_to_say:
        return None  # No message to say
    
    # URL encode the message
    encoded_msg = urllib.parse.quote(text_to_say)
    encoded_username = urllib.parse.quote(username)
    
    # Construct and send the request to the TTS server
    url = f"{TTS_SERVER}/say?voice={voice}&stability={stability}&similarity_boost={similarity}&msg={encoded_msg}&username={encoded_username}"
    
    print(f"Sending TTS request: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"TTS request successful: {response.json()}")
            return True
        else:
            print(f"TTS request failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error sending TTS request: {e}")
        return False

def main():
    # Connect to Twitch IRC server
    sock = socket.socket()
    sock.connect((SERVER, PORT))
    
    # Authenticate with OAuth token and join the channel
    sock.send(f"PASS {BOT_OAUTH}\r\n".encode('utf-8'))
    sock.send(f"NICK {BOT_NICK}\r\n".encode('utf-8'))
    sock.send(f"JOIN {CHANNEL}\r\n".encode('utf-8'))
    
    print(f"Connected to {CHANNEL} as {BOT_NICK}")
    
    while True:
        resp = sock.recv(2048).decode('utf-8')
        
        # Twitch may send multiple messages at once, split by \r\n
        for line in resp.split('\r\n'):
            if not line:
                continue
                
            # Respond to PINGs to avoid disconnect
            if 'PING' in line:
                sock.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
                print("PONG sent")
                continue
                
            # Parse chat messages
            # Format: :username!username@username.tmi.twitch.tv PRIVMSG #channel :message
            match = re.match(r'^:(\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :(.+)', line)
            if match:
                username = match.group(1)
                message = match.group(2).strip()
                print(f"{username}: {message}")
                
                # Check for !say command
                if message.lower().startswith('!say'):
                    result = process_say_command(username, message)
                    if result is None:
                        send_message(sock, f"@{username}, you didn't provide a message to say.")

if __name__ == "__main__":
    main()
