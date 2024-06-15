import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from datetime import datetime
from gevent import monkey
monkey.patch_all()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, async_mode='gevent')

messages = []
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    user_id = 'Unknown'
    users[request.sid] = user_id
    emit('assign_user_id', user_id)
    emit('load_messages', messages, to=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        del users[request.sid]

@socketio.on('message')
def handle_message(msg):
    user_id = users.get(request.sid, 'Unknown')
    message = {
        'user': user_id,
        'text': msg,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    messages.append(message)
    send(message, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
