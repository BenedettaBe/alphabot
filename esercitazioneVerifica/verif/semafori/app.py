import semaforo
from flask import Flask, url_for, redirect, render_template, make_response, request
import time
import sqlite3

app = Flask(__name__)

s = semaforo.semaforo()
STATO = "ATTIVO" #"SPENTO"

temp_sem_rosso = 2
temp_sem_verde = 2
temp_sem_giallo = 1        

def data():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM utenti")
    var = cur.fetchall()
    utenti = {r[0]:r[1] for r in var}
    conn.commit()
    conn.close()
    return utenti

def salva_operazione(operazione, username):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username =?", (username,))
    id_user = cur.fetchone()[0]
    cur.execute("INSERT INTO operazioni (id_u, operazione, data) VALUES (?, ?, ?)", (id_user, operazione, datetime.now()))
    conn.commit()
    conn.close()
    print("salvato sul db l'azione: " + operazione + " dell'utente: " + username)


@app.route('/')
def index():
    username = request.cookies.get("username")
    if username:
        return redirect(url_for('login'))
    return redirect(url_for('test'))

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = data()
        user = request.form["username"]
        psw = request.form["psw"]
        if account[user] == psw:
            response = make_response(redirect(url_for('controllo')))
            response.set_cookie("username", user, max_age=60*60*24)
            return response
    return render_template('login.html')

@app.route('/controllo', methods=['POST', ' GET'])
def controllo():
    username = request.cookie.get("username")
    if username:
        if request.method == 'POST':
            global STATO
            global temp_sem_rosso, temp_sem_verde, temp_sem_giallo
            if request.form['buttone'] == 'salva':
                temp_sem_rosso = int(request.form['rosso'])
                temp_sem_verde = int(request.form['verde'])
                temp_sem_giallo = int(request.form['giallo'])
            elif request.form['buttone'] == 'spegni':
                if STATO == "ATTIVO":
                    STATO = "SPENTO"
                    salva_operazione("SPEGNIMENTO", request.cookies.get('username'))
            elif request.form['buttone'] == 'attiva':
                if STATO == "SPENTO":
                    STATO = "ATTIVO"
                    salva_operazione("ATTIVO", request.cookies.get('username'))
    return render_template('controllo.html')


#ESEMPIO di pagina di test
@app.route('/test')
def test():
    username = request.cookie.get("username")
    if username:
        if STATO == "ATTIVO":
            #Esempio di sequenza con semaforo attivo. I tempi devono essere
            #modificabili dalla pagina di configurazione!
            s.rosso(2)
            s.verde(2)
            s.giallo(1)
        else:
            #Esempio di sequenza con semaforo spento. I tempi devono essere
            #modificabili dalla pagina di configurazione!
            for _ in range(3):
                s.giallo(1)
                s.luci_spente(1)
        return 'TEST ESEGUITO!'
    else:
       return redirect(url_for('login')) 

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
