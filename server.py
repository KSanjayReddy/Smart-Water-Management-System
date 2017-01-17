# In every route which requires login , just put if logged_in:
# Logout button that send request to /logout





from flask import Flask, render_template, url_for
from flask import jsonify, request
from flask import flash, redirect,abort

import datetime as d
app = Flask(__name__)
lastOffTime = d.datetime.now()
netlitres = 0
prevtank1 = 10
diff = 0
x = 0
logged_in = False

tank1data = 40
tank2data = 40
current =  "OFF"
option = ""
ontime = 0

'''@app.route('/',  methods=['GET'])
def index():

    global tank1_level
    return render_template('index_gauge.html')  '''


@app.route('/')
def home():
    lastOffTime = d.datetime.now()
    return render_template('home.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')
@app.route('/logout', methods=['GET'])
def logout():
    global logged_in
    logged_in = False
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def check_login():
    global logged_in
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        logged_in = True
        return redirect('/water')
    else:
        return render_template('login.html')
@app.route('/water', methods=['GET'])
def water():
    if logged_in:
        return render_template('index_gauge.html')
    else:
        return redirect('/login')
@app.route('/energy', methods=['GET'])
def energy():
    if logged_in:
        return render_template('energy.html')
    else:
        return redirect('/login')
@app.route('/deptho/<int:depth_cm1>', methods=['GET'])
def show_post1(depth_cm1):
    global tank1data
    global netlitres
    global prevtank1
    global diff
    if depth_cm1 < prevtank1:
        diff = (prevtank1 - depth_cm1)
    tank1data = depth_cm1
    prevtank1 = depth_cm1
    netlitres = netlitres + diff
    return 'ok'

@app.route('/change/<string:switch>', methods=['GET','POST'])
def change(switch):
    global option
    option = switch
    return option


@app.route('/stat', methods=['GET'])
def status():
    global ontime
    global tank1data
    global tank2data
    global current

    if tank1data<20 and tank2data>20 and option == "auto":
        current = "On"
    elif option == "on":
        current = "On"
    elif option == "off":
        current = "OFF"
    else:
        current = "OFF"
    if current == "On":
        return 'abc$'
    else:
        return 'xyz$'


@app.route('/depths/<int:depth_cm2>', methods=['GET'])
def show_post2(depth_cm2):
    global tank2data
    tank2data = depth_cm2
    return 'ok'

@app.route('/return_global', methods=['GET'])
def return_global():
    global tank1data
    global tank2data
    global current
    global ontime
    global lastOffTime
    global netlitres
    global x
    x = x+ 1
    if current == "OFF":
        lastOffTime = d.datetime.now()
    elif current == "On":
        if  0==0:
            f= 0
            diff = d.datetime.now() - lastOffTime
            lastOffTime = d.datetime.now()
            f = diff.microseconds
            ontime = ontime + f

    return jsonify(tank1 = tank1data , tank2 = tank2data, stat = current, time = ontime/1000000, net= netlitres)


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8080, debug=True)
