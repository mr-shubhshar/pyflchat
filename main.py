from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app)

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

@app.route('/')
def index():
    messages = ['First message', 'Second message', 'Third message']
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    socketio.run(app)

