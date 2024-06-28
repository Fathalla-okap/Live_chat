from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

# إعداد التطبيق
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'

# إعداد قاعدة البيانات وسوكيت
db = SQLAlchemy(app)
socketio = SocketIO(app)

# تعريف نموذج الرسالة
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

# مسارات التطبيق
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages')
def get_messages():
    messages = Message.query.all()
    return jsonify([{'text': msg.text} for msg in messages])

# معالجة الرسائل عبر سوكيت
@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    new_message = Message(text=msg)
    db.session.add(new_message)
    db.session.commit()
    emit('message', msg, broadcast=True)

# بدء تشغيل التطبيق
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app)
