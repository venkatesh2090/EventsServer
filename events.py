from flask import Flask, Response, request
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL_1')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)

class Person(db.Model):
    id = db.Column(db.String, primary_key=True)
    personal_email = db.Column(db.String(320), nullable=False)

db.create_all()

@app.route('/', methods=['GET','POST'])
def webex_callback():
    if request.method == 'POST':
        reqData = request.json
        id = reqData['data']['id']
        personal_email = reqData['data']['personEmail']
        person = Person(id=id, personal_email=personal_email)
        db.session.add(person)
        db.session.commit()
        return Response('OK', 200)
    else:
        return Response("I'm alive", 200)

@socketio.on('message')
def handle_message(data):
    print('received message' + data)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + json)

if __name__ == '__main__':
    socketio.run()