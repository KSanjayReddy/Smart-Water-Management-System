from flask import Flask, render_template, url_for
from flask import jsonify, request

app = Flask(__name__)
tank1data = 10
tank2data = 30
current =  "ON"
option = ""


@app.route('/',  methods=['GET'])
def index():

    global tank1_level
    return render_template('index_gauge.html')

@app.route('/deptho/<int:depth_cm1>', methods=['GET'])
def show_post1(depth_cm1):
    global tank1data
    tank1data = depth_cm1
    return 'ok'

@app.route('/change', methods=['GET','POST'])
def change():
    global option
    value = request.form['switch']
    option = value
    return value


@app.route('/stat', methods=['GET'])
def status():
    global tank1data
    global tank2data
    global current
    if tank1data<20 and tank2data>20 and option == "auto":
        current = "ON"
    elif option == "on":
        current = "ON"
    elif option == "off":
        current = "OFF"
    else :
        current = "OFF"
    return current

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
    return jsonify(tank1 = tank1data , tank2 = tank2data, stat = current)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
