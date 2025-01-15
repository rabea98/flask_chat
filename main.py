from flask import Flask, request, send_from_directory
from datetime import datetime
from werkzeug.exceptions import BadRequestKeyError
from pathvalidate import ValidationError, validate_filename
from markupsafe import escape
import os
import sys

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
    
# Implemented by Ariel Fellous
@app.route('/api/chat/<room>', methods=['POST'])
def postchatmessage(room):
    status = 200
    messge = "success"
    try:
        validate_filename(room)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = escape(request.form["username"])
        msg = escape(request.form["msg"])
        with open(os.path.join(CHAT_LOGS_DIR, f"{room}.txt"), 'a') as roomfile:
            roomfile.write("[%s] %s: %s\n"%(date, username, msg))
            return "success"
    except IOError:
        status = 500
        message = "error opening room file for %s."%room
    except BadRequestKeyError:
        status = 400
        message = "missing form fields"
    except ValidationError:
        status = 400
        message = "invalid room name"
    return message, status
if __name__ == '__main__':
    app.run(debug=True)
