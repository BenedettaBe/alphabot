from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import sqlite3
import datetime

app = Flask(__name__)

def data():
    con = sqlite3.connect('./databaseLogin.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM utenti")
    variabili = cur.fetchall()  
    diz = {r[0]: r[1] for r in variabili}
    con.close()
    return diz

def initialize_db():
    con = sqlite3.connect('./databaseSemafori.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS utenti (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    con.commit()
    con.close()
    
def check_account(username, password):
    acc = data()  
    if username in acc:
        psw = acc[username]  
        if psw == password:
            return True
    return False

@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        if check_account(username,password):
            return redirect(url_for('centroControllo'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    initialize_db()
    app.run(debug=True, host = 'localhost')