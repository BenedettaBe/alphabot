#from AlphaBot import AlphaBot
from flask import Flask, render_template, request, redirect, url_for, make_response
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

def initialize_db():
    con = sqlite3.connect('./databaseLogin.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS utenti (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    con.commit()
    con.close()

def debug_db():
    con = sqlite3.connect('databaseLogin.db')
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tabelle presenti:", cur.fetchall())

    try:
        cur.execute("PRAGMA table_info(utenti);")
        print("Schema della tabella utenti:", cur.fetchall())
    except sqlite3.OperationalError as e:
        print("Errore:", e)

    con.close()
    
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
    print(acc)
    if username not in acc:
        con = sqlite3.connect('./databaseLogin.db')
        cur = con.cursor()
        cur.execute("INSERT INTO utenti (username, password) VALUES (?, ?)", (username, hashed_password))
        con.commit()
        con.close()
        return True
    return False

    

@app.route("/")
def index():
    username = request.cookies.get("username")
    if username:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        #print("Username ricevuto:", username)
        #print("Password ricevuta:", password)

        if check_account(username, password):
            print("Login riuscito")
            response = make_response(redirect(url_for('home')))
            response.set_cookie("username", username, max_age=60*60*24)
            return response
        else:
            print("Login fallito - Credenziali errate")
            return render_template("login.html", alert="Invalid username or password")
    return render_template("login.html")


@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        
        if aggiungi_utente(username, password):
            return redirect(url_for('login'))

        else:
            return render_template("create_account.html", alert="username presente")

    return render_template("create_account.html")


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("movimenti.html")


@app.route("/logout")
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie("username")
    return response


@app.route("/movimenti", methods=['POST'])
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
    return render_template("movimenti.html")

if __name__ == '__main__':
    app.run(debug=True, host = 'localhost')

    