from flask import Flask, request, send_from_directory
from datetime import datetime
import os

app = Flask(__name__)

# Create chat_logs directory if it doesn't exist
CHAT_LOGS_DIR = 'chat_logs'
if not os.path.exists(CHAT_LOGS_DIR):
    os.makedirs(CHAT_LOGS_DIR)


@app.route('/')
def home():
    return send_from_directory('static', 'index.html')


@app.route('/<room>')
def room(room):
    return send_from_directory('static', 'index.html')


@app.route('/api/chat/<room>', methods=['GET'])
def get_chat(room):
    try:
        with open(os.path.join(CHAT_LOGS_DIR, f"{room}.txt"), 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""

if __name__ == '__main__':
    app.run(debug=True)
