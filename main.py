from flask import Flask, render_template, request, jsonify, session as ss
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

app = Flask(__name__)
app.secret_key = 'super secret key'
engine = create_engine('postgresql://postgres:1234@localhost/web')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == "" or request.form['password'] == "":
            return jsonify({'message': 'Invalid data'})
        try:
            temp = session.query(User).filter(User.username == request.form['username']).first()
            if temp.password == request.form['password']:
                ss['username'] = request.form['username']
                ss['password'] = request.form['password']
                ss['id'] = temp.id
                return jsonify({'message': 'Success'})
        except Exception as e:
            return jsonify({'message': 'User not found'})
        return jsonify({'message': 'Access denied'})
    return render_template('login.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        try:
            name = request.form['name']
            surname = request.form['surname']
            username = request.form['username']
            password1 = request.form['password1']
            password2 = request.form['password2']
            email = request.form['email']
            if name == '' or surname == '' or username == '' or password1 == '' or password2 == '' or email == '':
                return jsonify({'message': 'Invalid Data'})
            if password1 != password2:
                return jsonify({'message': 'Different passwords'})
            if session.query(User).filter(User.username == request.form['username']).first() != None:
                return jsonify({'message': 'Username Occupied'})
            temp_user = User(name=name, surname=surname, username=username, password=password1, email=email)
            session.add(temp_user)
            ss['id'] = session.query(User).filter(User.username == request.form['username']).first().id
            session.commit()
            return jsonify({'message': 'Success'})
        except Exception as e:
            return jsonify({'message': 'Error'})
    return render_template('sign_up.html')


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')


@app.route('/user', methods=['GET', 'POST'])
def user():
    check_user = session.query(User).filter(User.username == ss['username']).first()
    if request.method == 'POST':
        password = request.form['check']
        if password ==check_user.password:
            return jsonify({'message': 'Success'})
        else:
            return jsonify({'message': 'Error !'})
    return render_template('user.html',username=ss['username'], name=check_user.name, surname=check_user.surname, email=check_user.email)


@app.route('/change_user_data', methods=['POST', "GET"])
def change_user_data():
    if request.method == 'POST':
        try:
            name = request.form['name']
            surname = request.form['surname']
            username = request.form['username']
            password1 = request.form['password1']
            password2 = request.form['password2']
            email = request.form['email']
            if name == '' or surname == '' or username == '' or password1 == '' or password2 == '' or email == '':
                return jsonify({'message': 'Invalid Data'})
            if password1 != password2:
                return jsonify({'message': 'Different passwords'})
            meta = session.query(User).filter(User.username == request.form['username']).all()
            for us in meta:
                if us.password != ss['password']:
                    return jsonify({'message': 'Username Occupied'})
            temp_user = session.query(User).filter(User.username == ss['username']).first()
            temp_user.name = name
            temp_user.surname = surname
            temp_user.username = username
            ss['username']=username
            temp_user.password = password1
            temp_user.email = email
            session.commit()
            return jsonify({'message': 'Success'})
        except Exception as e:
            return jsonify({'message': 'Error'})
    return render_template('user.html')


@app.route('/add_event', methods=['POST'])
def add_event():
    try:
        name = request.form['name']
        time = request.form['time']
        date = request.form['date']
        desc = request.form['desc']
        owner_id = ss['id']
        if name == '' or time == '' or date == '' or desc == '':
            return jsonify({'message': 'Invalid data'})
        new_event = Event(name=name, time=time, date=date, description=desc, owner_id=owner_id)
        session.add(new_event)
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/update_event', methods=['POST'])
def update_event():
    try:
        name = request.form['name']
        time = request.form['time']
        date = request.form['date']
        desc = request.form['desc']
        get_name = request.form['get_name']
        get_time = request.form['get_time']
        get_desc = request.form['get_desc']
        if name == '' or time == '' or date == '' or desc == '':
            return jsonify({'message': 'Invalid data'})
        change_event = session.query(Event).filter(
            Event.name == get_name and Event.time == get_time and Event.desc == get_desc).first()
        change_event.name = name
        change_event.time = time
        change_event.date = date
        change_event.description = desc

        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/delete_event', methods=['POST'])
def delete_event():
    try:
        names = request.form.getlist('names[]')
        date = request.form['date']
        print(ss['id'],date)
        events = session.query(Event).filter(Event.owner_id == ss['id'] , Event.date == date).all()

        for event in events:
            for name in names:
                if event.name == name:
                    session.delete(event)
                    break
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})


@app.route('/get_events', methods=['POST'])
def get_events():
    try:
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']
        temp_events = []
        events = session.query(Event).filter(Event.owner_id == ss['id']).all()
        for event in events:
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
        user_ = session.query(User).filter(User.id== ss['id']).first()
        events = session.query(Event).filter(Event.owner_id == ss['id']).all()
        for event in events:
            session.delete(event)
        session.delete(user_)
        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'message': 'Error'})


def start():
    user1 = User(username="Warrior", surname="Marvel", name="steve", password="123")
    user2 = User(username="Wayward", surname="Winchester", name="Sam", password="1234")
    user3 = User(username="Angel", surname="Winchester", name="Castiel", password="123423")
    session.add(user1)
    session.add(user2)
    session.add(user3)
    ev1 = Event(name="swimming", time='14', date='23/11/21', description="should be in time")
    ev2 = Event(name="reading", time='18', date='13/11/21', description="lots of books")
    session.add(ev1)
    session.add(ev2)
    session.commit()


def destroy():
    Base.metadata.drop_all(engine)
    session.commit()


if __name__ == "__main__":
    app.run(debug=True)
