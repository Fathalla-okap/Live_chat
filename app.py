from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, emit
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

messages = []
users = {}
usernames = {}
user_counter = 0
total_visitors = set()
online_users = 0

@app.route('/')
def index():
    global total_visitors

    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        total_visitors.add(user_id)
    else:
        total_visitors.add(user_id)

    response = make_response(render_template('index.html'))
    response.set_cookie('user_id', user_id)
    return response

@socketio.on('connect')
def handle_connect():
    global user_counter, online_users
    online_users += 1
    user_counter += 1
    user_uuid = str(uuid.uuid4())
    users[request.sid] = user_uuid
    usernames[user_uuid] = f'Unknown '
    emit('assign_user_id', usernames[user_uuid])
    emit('load_messages', messages, to=request.sid)
    emit('update_online_users', online_users, broadcast=True)
    emit('update_total_visitors', len(total_visitors), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    global online_users
    online_users -= 1
    if request.sid in users:
        del users[request.sid]
    emit('update_online_users', online_users, broadcast=True)

@socketio.on('message')
def handle_message(msg):
    user_uuid = users.get(request.sid, 'Unknown')
    user_id = usernames.get(user_uuid, 'Unknown')
    message = {'user': user_id, 'text': msg}
    messages.append(message)
    emit('message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
