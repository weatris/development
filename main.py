import smtplib
from flask import Flask, render_template, request, jsonify, session as ss
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from email.message import EmailMessage

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
        return jsonify({'message': 'Enter correct name/password'})
    return render_template('login.html')

@app.route('/log_out',methods=['POST'])
def log_out():
    ss['username'] = None
    ss['password'] = None
    ss['id'] = None
    return jsonify({'message': 'Success'})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('login.html')


@app.errorhandler(405)
def page_not_found(e):
    return render_template('login.html')


@app.route('/menu')
def menu():
    if ss['username']:
        temp = session.query(User).filter(User.username == ss['username']).first()
        return render_template('menu.html', role=temp.role, username=temp.username)
    else:
        return render_template('login.html')


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
            if sum(c.isdigit() for c in password1) < 3:
                return jsonify({'message': 'Should be at least 3 numbers in password'})
            if len(password1) < 8:
                return jsonify({'message': 'Should be at least 8 signs in password'})
            if password1.islower():
                return jsonify({'message': 'No upper character in password!'})
            if not email.find('@'):
                return jsonify({'message': 'Invalid email'})

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


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":
        msg = EmailMessage()
        msg.set_content('repair password on Calendar')
        s = smtplib.SMTP(host='smtp.ethereal.email', port=587)
        s.starttls()
        s.login('raegan.donnelly@ethereal.email', 'FArjwYKxt97XMYYHD9')
        msg['Subject'] = 'repair password'
        msg['From'] = 'taras.salanchii.knm.2019@lpnu.ua'
        msg['To'] = 'kvuserasuszenpad@gmail.com'
        s.send_message(msg)
        s.quit()
    return render_template('forgot_password.html')


@app.route('/user', methods=['POST'])
def user():
    check_user = session.query(User).filter(User.username == ss['username']).first()
    password = request.form['check']
    if password == check_user.password:
        return jsonify({'message': 'Success',
                        'username': ss['username'],
                        'name': check_user.name,
                        'surname': check_user.surname,
                        'email': check_user.email})
    else:
        return jsonify({'message': 'Error !'})


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
            ss['username'] = username
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
        owner = session.query(User).filter(User.id == ss['id']).first()

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
        if change_event.owner_id == ss['id']:
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
        chosen_events = request.form.getlist('chosen_events[]')
        chosen_friends = request.form.getlist('chosen_friends[]')
        date = request.form['date']
        for fr in chosen_friends:
            friend = session.query(User).filter(User.username == fr).first()
            for ev in chosen_events:
                event = session.query(Event).filter(Event.date == date,
                                                    Event.name == ev).first()
                if event.owner_id == ss['id']:
                    if friend.id not in event.shared_with:
                        friend.my_events.append(event)
                        event.shared_with.append(friend.id)

        session.commit()
        return jsonify({'message': 'Success'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error'})


@app.route('/delete_event', methods=['POST'])
def delete_event():
    try:
        names = request.form.getlist('names[]')
        date = request.form['date']
        usr = session.query(User).filter(User.id == ss['id']).first()
        for event in usr.my_events:
            for name in names:
                if event.name == name and event.date == date:
                    usr.my_events.remove(event)
                    if event.owner_id == ss['id']:
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
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']
        temp_events = []
        usr = session.query(User).filter(User.id == ss['id']).first()
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
        user_ = session.query(User).filter(User.id == ss['id']).first()
        events = session.query(Event).filter(Event.owner_id == ss['id']).all()
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
        friend_list = []
        usr = session.query(User).filter(User.id == ss['id']).first()
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
        usr = session.query(User).filter(User.id == ss['id']).first()
        friend = session.query(User).filter(User.username == request.form['name']).first()
        if not friend in usr.friends:
            usr.friends.append(friend)
            friend.friends.append(usr)
            session.flush()
            session.commit()
            return jsonify({'message': 'Success'})
        return jsonify({'message': 'Already friends'})
    except Exception as e:
        return jsonify({'message': 'Error'})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
