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
    person = db.relationship("Person", back_populates="emails")

Person.emails = db.relationship("Email", back_populates="person")

class Organisation(db.Model):
    __tablename__ = 'organisation'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(320), nullable=False, unique=True)
    name = Column(String, nullable=True)

class Event(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_id = Column(UUID(as_uuid=True), ForeignKey('organisation.id'), nullable=False, unique=False)
    organiser_id = Column(String, ForeignKey('person.id'), nullable=False, unique=False)
    date = Column(Date, nullable=False)
    organiser = db.relationship("Person", back_populates="events")

Person.events = db.relationship("Event", back_populates="organiser")

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
def person():
    personData = request.json
    person = Person(id=personData["id"], name=personData["name"])
    person.emails = []
    for email_address in personData["emails"]:
        email = Email(email=email_address)
        person.emails.append(email)
    db.session.add(person)
    db.session.commit()
    return {"msg": "ok"}

'''
event {
    name: "Org Name"
    email: "email"
}
'''
@app.route('/organisation', methods=['POST'])
def organisation():
    orgData = request.json
    org = Organisation(name=orgData["name"], email=orgData["email"])
    db.session.add(org)
    db.session.commit()
    return {"msg": "ok"}

'''
PUT
event {
    organisation: "orgid",
    organiser: Person with Email,
    date: "yyyy-mm-dd"
}
'''

@app.route('/event', methods=['POST', 'PUT'])
def event():
    if request.method == 'POST':
        eventData = request.json
        event = Event(organisation=eventData["organisation"], organiser=eventData["organiser"], date=eventData["date"])
        db.session.add(event)
        db.session.commit()
        return {"msg", "ok"}
    elif request.method == 'PUT':
        eventData = request.json
        event = Event(organisation=eventData["organisation"], date=eventData["date"])
        if (type(eventData["organiser"]) == 'str'):
            event.organiser = eventData["organiser"]
        else:
            personData = eventData["organiser"]
            person = Person(id=personData["id"], name=personData["name"])
            person.emails = []
            for email_address in personData["emails"]:
                email = Email(email=email_address)
                person.emails.append(email)
            event.organiser = person
        db.session.add(event)
        db.session.commit()
        return {"msg": "ok"}
