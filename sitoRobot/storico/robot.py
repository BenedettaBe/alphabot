from AlphaBot import AlphaBot
from flask import Flask, render_template, request
app = Flask(__name__)

robot = AlphaBot()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('W') == 'W':
            print("avanti")
            robot.forward()
        elif  request.form.get('S') == 'S':
            robot.backward()
        elif request.form.get('A') == 'A':
            robot.left()
        elif  request.form.get('D') == 'D':
            robot.right()
        elif  request.form.get('STOP') == 'STOP':
            robot.stop()
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

def login():
    if request.method == 'POST':
        username = request.form['e-mail']

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.130')