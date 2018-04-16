from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, make_response
import threading
import os

from tabledef import *
import Sensors

import time

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        s = Session()
        return render_template('show_entries.html', entries=s.query(Enviro))

@app.route('/picture')
def picture():
    if not session.get('logged_in'):
        flash('Error: not logged in')
        return home()
    path = Sensors.getPic()
    return images(path)

@app.route('/dynamic/<path:path>')
def images(path):
    if not session.get('logged_in'):
        flash('Error: not logged in')
        return home()
    fullpath = "./dynamic/" + path
    try:
        resp = make_response(open(fullpath).read())
        resp.content_type = "image/jpeg"
    except IOError:
        flash('Error: file not found.')
        return home()
    return resp

@app.route('/login', methods=['POST'])
def do_admin_login():
    post_username = str(request.form['username'])
    post_password = str(request.form['password'])

    s = Session()
    query = s.query(User).filter(User.username.in_([post_username]), User.password.in_([post_password]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('Error login')
    return home()

@app.route('/logout')
def logout():
    session['logged_in']=False
    return home()

def monitor():
    """
    Periodically adds sensor data to database.
    """
    s = Session()
    while True:
        temp, hum = Sensors.getTempHum()
        moi       = Sensors.getSoilMoisture()
        e = Enviro(temp, hum, moi)
        s.add(e)
        s.commit()
        print "Count is now %d" % s.query(Enviro).count()
        while (s.query(Enviro).count() > 288):
            s.delete(s.query(Enviro).order_by(Enviro.sdate).first())
            s.commit()
        time.sleep(300)


if __name__ == '__main__':
    thread = threading.Thread(target = monitor)
    thread.start()
    app.secret_key = os.urandom(12)
    app.run(debug=False,host='0.0.0.0', port=4000)
