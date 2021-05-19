from flask import Response, request, jsonify
from flask_restful import Resource

from main import work_session

from models import *
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import json
from werkzeug.security import generate_password_hash, check_password_hash
from main import *
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class AddEvent(Resource):
    def post(self):
        data = request.json
        try:
            temp_event = Event(data["name"], data["status"])
            # temp_event = Event(name="hello", status={"i am groot", "great"})
            us_id = data["id"]
            session.add(temp_event)
            temp_event.users.append(us_id)
            us_id.my_events.append(temp_event)

            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class UpdateEvent(Resource):
    def put(self):
        data = request.json
        if "id_" in data:
            id_ = data['id_']
        else:
            return Response(
                response=json.dumps({"message": "No Id !"}),
                status=404,
                mimetype="application/json"
            )
        try:
            temp = session.query(Event).get(id_)
            # if "id_event" in data:
            #     course1.name = data["id_event"]
            if "name" in data:
                temp.name = data['name']
            else:
                temp.name = "test"
            # if "status" in data:
            #     course1.status = data["status"]
            session.commit()
            return Response(
                response=json.dumps({"message": "Hurray !"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Error !"}),
                status=405,
                mimetype="application/json"
            )


class DeleteEvent(Resource):
    def delete(self):
        try:
            data = request.json
            id_event = data["id_event"]
            # id_event=9
            course = session.query(Event).get(id_event)
            session.delete(course)
            session.commit()
            if course:
                return Response(
                    response=json.dumps({"message": "It works !"}),
                    status=200,
                    mimetype="application/json"
                )
            return Response(
                response=json.dumps({"message": "Error !"}),
                status=404,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Error !"}),
                status=404,
                mimetype="application/json"
            )


class GetAllEvents(Resource):
    def get(self):
        data = request.json
        if data['role'] == 'admin':
            temp = session.query(Event).all()
            if temp:
                return Response(
                    response=json.dumps(temp, cls=AlchemyEncoder),
                    status=200,
                    mimetype="application/json"
                )
            return Response(
                response=json.dumps({"message": "Not found"}),
                status=404,
                mimetype="application/json"
            )


class GetAllUserEvents(Resource):
    def get(self):
        data = request.json
        temp = session.query(User).get(data[id])
        if temp.my_events:
            return Response(
                response=json.dumps(temp.my_events, cls=AlchemyEncoder),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({"message": "No event for user"}),
            status=404,
            mimetype="application/json"
        )


class SignUpUser(Resource):
    def post(self):
        data = request.json
        try:
            user = User(data["username"], data["password"])
            if session.query(User).filter(User.email == user.email).all() \
                    and session.query(User).filter(User.username == user.username).all():
                return Response(
                    response=json.dumps({"message": "user already created"}),
                    status=405,
                    mimetype="application/json"
                )
            user.password = generate_password_hash(data["password"])
            session.add(user)
            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "wrong input"}),
                status=404,
                mimetype="application/json"
            )


class Test(Resource):
    def post(self):
        user1 = User(username="steve", surname="jared", name="fief", password="1234")
        session.add(user1)
        user2 = User(username="max", surname="red", name="tagger", password="12233")
        session.add(user2)
        user3 = User(username="oleg", surname="rect", name="aired", password="6575")
        session.add(user3)
        event1 = Event(name="7777", description="study hard")
        session.add(event1)
        event2 = Event(name="study", description="player")
        session.add(event2)
        event3 = Event(name="work", description="hello")
        session.add(event3)
        event3.users.append(user1)
        event3.users.append(user2)
        event1.users.append(user1)
        event2.users.append(user2)
        session.commit()


# class AddFriend(Resource):
#     def post(self):
#         try:
#             data = request.json
#             friend = session.query(User).get(data['fname'])
#             user = session.query(User).get(data['name'])
#             user.friends.append(friend.id)
#             friend.friends.append(user.id)
#             session.commit()
#             return Response(
#                 response=json.dumps({"message": "Success"}),
#                 status=200,
#                 mimetype="application/json"
#             )
#         except Exception as e:
#             return Response(
#                 response=json.dumps({"message": "Error"}),
#                 status=405,
#                 mimetype="application/json"
#             )
#
#
# class DeleteFriend(Resource):
#     def delete(self):
#         try:
#             data = request.json
#             friend = session.query(User).get(data['fname'])
#             user = session.query(User).get(data['name'])
#             user.friends.remove(friend.id)
#             friend.friends.remove(user.id)
#             session.commit()
#             return Response(
#                 response=json.dumps({"message": "Success"}),
#                 status=200,
#                 mimetype="application/json"
#             )
#         except Exception as e:
#             return Response(
#                 response=json.dumps({"message": "Error"}),
#                 status=405,
#                 mimetype="application/json"
#             )


# class ShareEvent(Resource):
#     def post(self):
#         try:
#             data = request.json
#             event = session.query(User).get(data['event_id'])
#             friend = session.query(User).get(data['friend'])
#             friend.shared_events.append(event)
#             session.commit()
#             return Response(
#                 response=json.dumps({"message": "Success"}),
#                 status=200,
#                 mimetype="application/json"
#             )
#         except Exception as e:
#             return Response(
#                 response=json.dumps({"message": "Error"}),
#                 status=405,
#                 mimetype="application/json"
#             )
#
#
# class StopShareEvent(Resource):
#     def post(self):
#         try:
#             data = request.json
#             event = session.query(User).get(data['event_id'])
#             friend = session.query(User).get(data['friend'])
#             friend.shared_events.remove(event)
#             session.commit()
#             return Response(
#                 response=json.dumps({"message": "Success"}),
#                 status=200,
#                 mimetype="application/json"
#             )
#         except Exception as e:
#             return Response(
#                 response=json.dumps({"message": "Error"}),
#                 status=405,
#                 mimetype="application/json"
#             )