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
    date = Column(Date, nullable=False, unique=False)
    room = Column(String, nullable=False, unique=False)
    organiser = db.relationship("Person", back_populates="events")
    organisation = db.relationship("Organisation", back_populates="events")

Organisation.events = db.relationship("Event", back_populates="organisation")
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
organisation {
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
    return {"organisation_id": organisation.id}

'''
PUT
event {
    organisation: "orgid",
    organiser: Person with Email,
    date: "yyyy-mm-dd",
    room: "roomid"
}
'''
@app.route('/event/<room>', methods=['GET'])
@app.route('/event', methods=['POST', 'PUT'])
def event(room=None):
    eventData = request.json
    if request.method == 'POST':
        event = Event(organisation_id=eventData["organisation"], organiser_id=eventData["organiser"], date=eventData["date"])
        db.session.add(event)
        db.session.commit()
        return {"event_id": event.id}
    elif request.method == 'PUT':
        event = Event(organisation_id=eventData["organisation"], date=eventData["date"])
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
        return {"event_id": event.id}
    elif request.method == 'GET':
        eventsQueryData = Event.query.filter_by(room=room).all()
        events = []
        for event in eventsQueryData:
            events.append({
                "organisation": event.organisation_id,
                "organiser": event.organiser_id,
                "date": event.date,
                "room": event.room
            })
        return events

