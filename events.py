import email
from flask import Flask, Response, request
from sqlalchemy import String, Column, ForeignKey, Date
from os import environ
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL_1')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'person'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)

class Email(db.Model):
    __tablenmae__ = 'email'
    email = Column(String(320), primary_key=True)
    person_id = Column(String, ForeignKey('person.id'), unique=False)
    person = db.relationship("User", back_populates="emails")

Person.emails = db.relationship("Email", back_populates="person")

class Organisation(db.Model):
    __tablename__ = 'organisation'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    organisation_email = Column(String(320), nullable=False, unique=True)
    friendly_name = Column(String, nullable=True)

class Event(db.Model):
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    organisation = Column(UUID, ForeignKey('organisation.id'), nullable=False, unique=False)
    organiser = Column(String, ForeignKey('person.id'), nullable=False, unique=False)
    date = Column(Date, nullable=False)


db.create_all()

'''
person {
    id: "webexid",
    emails: [
        "email1",
        "email2"
    ],
    name: "name"
}
'''
@app.route('/person', methods=['POST'])
def webex_callback():
    personData = request.json
    person = Person(id=personData["id"], name=personData["name"])
    person.emails = []
    for email_address in personData["emails"]:
        email = Email(email=email_address)
        person.emails.append(email)
    db.session.add(person)
    db.session.commit()
    return Response('OK', 200)