# File: app.py
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# In-memory storage for messages (for demonstration purposes)
messages = []

# List of random names for "unknown" users
names = ['Unknown']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    if message:
        # Generate a random name from the list
        name = random.choice(names)
        # Format message as "name: message"
        formatted_message = f"{name}: {message}"
        messages.append(formatted_message)
        return jsonify({'status': 'OK', 'message': 'Message sent successfully'})
    else:
        return jsonify({'status': 'ERROR', 'message': 'Message cannot be empty'})

@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)
