from urllib import response
from flask import Flask, Response, request, json
from sqlalchemy.dialects.postgresql import UUID
from os import environ
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    personal_email = db.Column(db.String(320), nullable=False)


@app.route('/webex/callback', methods=['GET','POST'])
def webex_callback():
    if request.method == 'POST':
        reqData = request.json
        print(reqData['data']['id'])
        print(reqData['data']['personEmail'])
        return Response('OK', 200)
    else:
        return Response("I'm alive", 200)