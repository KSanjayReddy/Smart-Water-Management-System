from flask import Flask, render_template, url_for
from flask import jsonify, request
from flask import flash, redirect,abort
import datetime as d
lastOffTime = d.datetime.now()
netlitres = 0
prevtank1 = 10
diff = 0
x = 0

app = Flask(__name__)
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
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        return render_template('index_gauge.html')
    else:
        return home()


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

@app.route('/change', methods=['GET','POST'])
def change():
    global option
    value = request.form['switch']
    option = value
    return value


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
