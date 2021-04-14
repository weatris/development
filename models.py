from datetime import timedelta
from flask import Flask, render_template, request, jsonify ,session as ss ,json
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Time, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, DeclarativeMeta

Base = declarative_base()
events_users = Table('events_users', Base.metadata,
                     Column('user_id', Integer, ForeignKey('users.id')),
                     Column('event_id', Integer, ForeignKey('events.id_event'))
                     )

# shared_events = Table('shared_events', Base.metadata,
#                      Column('user_id', Integer, ForeignKey('users.id')),
#                      Column('event_id', Integer, ForeignKey('events.id_event'))
#                      )


class User(Base):
    __tablename__ = "users"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    surname = Column('surname', String)
    username = Column('username', String)
    email = Column('email', String)
    password = Column('password', String)
    role = Column('role', String)
    my_events = relationship("Event", secondary=events_users)

    def __init__(self, name=None, username=None, surname=None, email=None, password=None, role="user"):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password
        self.email = email
        self.role = role


class Event(Base):
    __tablename__ = "events"

    id_event = Column('id_event', Integer, primary_key=True)
    name = Column('name', String)
    description = Column('description', String)
    time = Column('time', String)
    date = Column('date', String)
    owner_id = Column('owner_id', Integer)

    def __init__(self, name="My Event", description="My description", time=None, date=None,owner_id=None):
        self.name = name
        self.time = time
        self.date = date
        self.description = description
        self.owner_id=owner_id

    def serialize(self):
        return {
            'name': self.name,
            'time': self.time,
            'description': self.description
        }
# class AlchemyEncoder(json.JSONEncoder):
#
#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             # an SQLAlchemy class
#             fields = {}
#             for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 try:
#                     json.dumps(data)  # this will fail on non-encodable values, like other classes
#                     fields[field] = data
#                 except TypeError:
#                     fields[field] = None
#             # a json-encodable dict
#             return fields
#
#         return json.JSONEncoder.default(self, obj)