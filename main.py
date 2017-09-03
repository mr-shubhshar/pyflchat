from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)

class History(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    message = db.Column('message', db.String(200))

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)

    message = History(message=msg)
    db.session.add(message)
    db.session.commit()

    send(msg, broadcast=True)

@app.route('/')
def index():
    #messages = ['First message', 'Second message', 'Third message']
    messages = History.query.all() # returns a dict
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    socketio.run(app)

