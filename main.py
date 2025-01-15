from flask import Flask, request
from datetime import datetime
import os
#os is needed file operations when we implement the chat storage
#datetime is needed for timestamp handling in the chat messages
app = Flask(__name__)

# Ensure chat logs directory exists
CHAT_LOGS_DIR = 'chat_logs'
os.makedirs(CHAT_LOGS_DIR, exist_ok=True)

# Person A: Implement basic Flask app for static HTML
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

# Person B: Implement room-specific routes
@app.route('/<room>')
def room(room):
    return send_from_directory('static', 'index.html')

# Person A: Implement GET chat API
@app.route('/api/chat/<room>', methods=['GET'])
def get_chat(room):
    # TODO: Implement getting chat messages
    pass

# Person B: Implement POST chat API
@app.route('/api/chat/<room>', methods=['POST'])
def post_chat(room):
    # TODO: Implement posting chat messages
    pass

if __name__ == '__main__':
    app.run(debug=True)
