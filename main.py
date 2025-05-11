import socket
import re
import time
import threading
import requests

# Twitch IRC server details
SERVER = 'irc.chat.twitch.tv'
PORT = 6667

# Replace these with your bot's Twitch username and OAuth token (include 'oauth:' prefix)
BOT_NICK = 'hlaschatu'         # e.g. 'mybot'
BOT_OAUTH = 'oauth:afwy0f1cqdeenbfkni4l59nw24di1t'  # e.g. 'oauth:abcd1234...'

# The channel to join (your Twitch channel, with # prefix)
CHANNEL = '#itswojtys'         # e.g. '#mychannel'

def send_message(sock, message):
    """
    Send a message to the Twitch chat.
    """
    message_temp = f"PRIVMSG {CHANNEL} :{message}\r\n"
    print(f"Sending message: {message_temp.strip()}")
    sock.send(message_temp.encode('utf-8'))
    time.sleep(1)  # Sleep to avoid Twitch rate limits

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
                    say_text = message[4:].strip()
                    if say_text:
                        #send_message(sock, say_text)
                        requests.get("http://localhost:42069/say?message=" + say_text)
                    else:
                        send_message(sock, f"@{username}, you didn't provide a message to say.")

if __name__ == "__main__":
    main()

