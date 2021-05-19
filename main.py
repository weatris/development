import smtplib
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from email.message import EmailMessage
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['SECRET_KEY'] = "super secret key"
engine = create_engine('postgresql://postgres:1234@localhost/web')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/', methods=['GET', 'POST'])
def login():
    try:
        data = request.json
        if data['username'] == "" or data['password'] == "":
            return jsonify({'message': 'Invalid data'})
        temp = session.query(User).filter(User.username == data['username']).first()
        if temp.password == data['password']:
            return jsonify({'message': 'Success', 'id': temp.id, 'role': temp.role, 'username': temp.username})
    except Exception as e:
        return jsonify({'message': 'User not found'})
    return jsonify({'message': 'Enter correct name/password'})


@app.route('/log_out', methods=['POST'])
def log_out():
    return jsonify({'message': 'Success'})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('login.html')


@app.errorhandler(405)
def page_not_found(e):
    return render_template('login.html')


@app.route('/menu')
def menu():
    try:
        data = request.json
        if data['username']:
            temp = session.query(User).filter(User.username == data['username']).first()
            return jsonify({'message': 'Success', 'role': temp.role, 'username': temp.username})
        else:
            return jsonify({'message': 'Error !'})
    except Exception as e:
        return jsonify({'message': 'Error !'})


@app.route('/sign_up', methods=['POST'])
def sign_up():
    try:
        data = request.json
        name = data['name']
        surname = data['surname']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        email = data['email']
        if name == '' or surname == '' or username == '' or password1 == '' or password2 == '' or email == '':
            return jsonify({'message': 'Invalid Data'})
        if password1 != password2:
            return jsonify({'message': 'Different passwords'})
        # if sum(c.isdigit() for c in password1) < 3:
        #     return jsonify({'message': 'Should be at least 3 numbers in password'})
        # if len(password1) < 8:
        #     return jsonify({'message': 'Should be at least 8 signs in password'})
        # if password1.islower():
        #     return jsonify({'message': 'No upper character in password!'})
        # if not email.find('@'):
        #     return jsonify({'message': 'Invalid email'})

        if session.query(User).filter(User.username == data['username']).first() != None:
            return jsonify({'message': 'Username Occupied'})
        temp_user = User(name=name, surname=surname, username=username, password=password1, email=email)
        session.add(temp_user)
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/user', methods=['POST'])
def user():
    try:
        data = request.json
        check_user = session.query(User).filter(User.id == data['id']).first()
        password = data['check']
        if password == check_user.password:
            return jsonify({'message': 'Success',
                            'username': check_user.username,
                            'name': check_user.name,
                            'surname': check_user.surname,
                            'email': check_user.email})
        else:
            return jsonify({'message': 'Error !'})
    except Exception as e:
        return jsonify({'message': 'Error !'})


@app.route('/change_user_data', methods=['POST', "GET"])
def change_user_data():
    try:
        data = request.json
        name = data['name']
        surname = data['surname']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        email = data['email']
        if name == '' or surname == '' or username == '' or password1 == '' or password2 == '' or email == '':
            return jsonify({'message': 'Invalid Data'})
        if password1 != password2:
            return jsonify({'message': 'Different passwords'})
        meta = session.query(User).filter(User.username == data['username']).first()
        if meta is not None:
            if meta.id != data['id']:
                return jsonify({'message': 'Username Occupied'})
        temp_user = session.query(User).filter(User.id == data['id']).first()
        temp_user.name = name
        temp_user.surname = surname
        temp_user.username = username
        temp_user.password = password1
        temp_user.email = email
        session.commit()
        return jsonify({'message': 'Success', 'username': username})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/add_event', methods=['POST'])
def add_event():
    try:
        data = request.json
        name = data['name']
        time = data['time']
        date = data['date']
        desc = data['desc']
        print(data['id'], type(data['id']))
        owner_id = int(data['id'])
        owner = session.query(User).filter(User.id == owner_id).first()

        if name == '' or time == '' or date == '' or desc == '':
            return jsonify({'message': 'Invalid data'})
        new_event = Event(name=name, time=time, date=date, description=desc, owner_id=owner_id)
        session.add(new_event)
        owner.my_events.append(new_event)
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/update_event', methods=['POST'])
def update_event():
    try:
        data = request.json
        name = data['name']
        time = data['time']
        date = data['date']
        desc = data['desc']
        get_name = data['get_name']
        get_time = data['get_time']
        get_desc = data['get_desc']
        if name == '' or time == '' or date == '' or desc == '':
            return jsonify({'message': 'Invalid data'})
        change_event = session.query(Event).filter(
            Event.name == get_name and Event.time == get_time and Event.desc == get_desc).first()
        if change_event.owner_id == data['id']:
            change_event.name = name
            change_event.time = time
            change_event.date = date
            change_event.description = desc
            session.commit()
            return jsonify({'message': 'Success'})
        return jsonify({'message': 'Access denied'})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/share_event', methods=['POST'])
def share_event():
    try:
        data = request.json
        chosen_events = data['chosen_events']
        chosen_friends = data['chosen_friends']
        date = data['date']
        for fr in chosen_friends:
            friend = session.query(User).filter(User.username == fr).first()
            for ev in chosen_events:
                event = session.query(Event).filter(Event.date == date,
                                                    Event.name == ev).first()
                if event.owner_id == data['id']:
                    if friend.id not in event.shared_with:
                        friend.my_events.append(event)
                        event.shared_with.append(friend.id)

        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/delete_event', methods=['POST'])
def delete_event():
    try:
        data = request.json
        names = data['names']
        date = data['date']
        usr = session.query(User).filter(User.id == data['id']).first()
        for event in usr.my_events:
            for name in names:
                if event.name == name and event.date == date:
                    usr.my_events.remove(event)
                    if event.owner_id == data['id']:
                        for id in event.shared_with:
                            t = session.query(User).filter(User.id == id).first()
                            t.my_events.remove(event)
                        session.delete(event)
                    else:
                        event.shared_with.remove(usr.id)
                    break
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/get_events', methods=['POST'])
def get_events():
    try:
        data = request.json
        day = data['day']
        month = data['month']
        year = data['year']
        ss_id = data['id']
        temp_events = []
        usr = session.query(User).filter(User.id == ss_id).first()
        for event in usr.my_events:
            t = event.date.split(sep='/')
            if str(day) == t[0] and str(month) == t[1] and str(year) == t[2]:
                temp_events.append(event)
        if len(temp_events) >= 1:
            return jsonify(user_list=[e.serialize() for e in temp_events])
        return jsonify({'message': 'Error'})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/delete_account', methods=['POST'])
def delete_account():
    try:
        data = request.json
        user_ = session.query(User).filter(User.id == data['id']).first()
        events = session.query(Event).filter(Event.owner_id == data['id']).all()
        for event in events:
            session.delete(event)
        session.delete(user_)
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/get_friends', methods=['POST'])
def get_friends():
    try:
        data = request.json
        friend_list = []
        usr = session.query(User).filter(User.id == data['id']).first()
        for tmp in usr.friends:
            friend = session.query(User).filter(User.id == tmp.id).first()
            friend_list.append(friend.username)
        if friend_list:
            return jsonify({'friend_list': friend_list, 'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'No friend found'})


@app.route('/add_friend', methods=['POST'])
def add_friend():
    try:
        data = request.json
        usr = session.query(User).filter(User.id == data['id']).first()
        friend = session.query(User).filter(User.username == data['name']).first()
        if friend is None:
            return jsonify({'message': 'Friend not found'})
        if friend not in usr.friends:
            usr.friends.append(friend)
            friend.friends.append(usr)
            session.flush()
            session.commit()
            return jsonify({'message': 'Success'})
        return jsonify({'message': 'Already friends'})
    except Exception as e:
        return jsonify({'message': 'Error'})


if __name__ == "__main__":
    app.run(debug=True)
