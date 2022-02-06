from urllib import response
from flask import Flask, Response, request, json
from os import environ
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()

class Person(db.Model):
    id = db.Column(db.String, primary_key=True)
    personal_email = db.Column(db.String(320), nullable=False)


@app.route('/webex/callback', methods=['GET','POST'])
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