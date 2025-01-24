#from AlphaBot import AlphaBot
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
#robot = AlphaBot()

def data():
    con = sqlite3.connect('./databaseLogin.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM utenti")
    variabili = cur.fetchall()  
    diz = {r[0]: r[1] for r in variabili}
    con.close()
    return diz
    
def check_account(username, password):
    acc = data()  
    if username in acc:
        stored_hash = acc[username]  
        print(f"stored: {stored_hash} password: {password}")
        if check_password_hash(stored_hash, password):
            return True
    return False

    
def aggiungi_utente(username, password):
    hashed_password = generate_password_hash(password)
    acc = data()
    if username not in acc:
        con = sqlite3.connect('./databaseLogin.db')
        cur = con.cursor()
        cur.execute("INSERT INTO utenti (username, password) VALUES (?, ?)", (username, hashed_password))
        con.commit()
        con.close()
    

@app.route("/")
def index():
    return redirect(url_for('login'))



@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        print("Username ricevuto:", username)
        print("Password ricevuta:", password)

        if check_account(username, password):
            print("Login riuscito")
            return redirect(url_for('home'))
        else:
            print("Login fallito - Credenziali errate")
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        
        aggiungi_utente(username, password)
        return redirect(url_for('login'))
    
    return render_template("create_account.html")

@app.route("/home", methods=['GET', 'POST'])
def home():

    return redirect(url_for('movimenti'))

@app.route("/movimenti", methods=['GET', 'POST'])
def movimenti():
    if request.method == 'POST':
        if request.form.get('W') == 'W':
            print("avanti")
            #robot.forward()
        elif  request.form.get('S') == 'S':
            print("indietro")
            #robot.backward()
        elif request.form.get('A') == 'A':
            print("sinistra")
            #robot.left()
        elif  request.form.get('D') == 'D':
            print("destra")
            #robot.right()
        elif  request.form.get('STOP') == 'STOP':
            print("stop")
            #robot.stop()
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('movimenti.html')
    
    return render_template("movimenti.html")

if __name__ == '__main__':
    app.run(debug=True, host = '192.168.1.130')

    