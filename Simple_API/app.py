from flask import Flask, jsonify, request
#import requests # Per fare richieste CURL
import sqlite3

app = Flask(__name__)


# Dizionario di studenti
'''studenti = {
    1: {"nome": "Mario", "cognome": "Rossi", "eta": 18},
    2: {"nome": "Luca", "cognome": "Bianchi", "eta": 19},
    3: {"nome": "Giulia", "cognome": "Verdi", "eta": 17}
}'''

# CREATE - Aggiungi un nuovo studente
@app.route("/studenti", methods=["POST"])
def create_studente():
       
    conn = sqlite3.connect("./databaseB.db")
    cur = conn.cursor()
    cur.execute('''INSERT INTO studenti("nome", "cognome", "eta") VALUES
            ("Mario", "Rossi", "18");''')
    conn.commit()

    return jsonify({"messaggio": "Studente aggiunto"}), 201

# READ - Ottieni tutti gli studenti
@app.route("/studenti", methods=["GET"])
def get_studenti():
    conn = sqlite3.connect("./databaseB.db")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM studenti''')
    var = cur.fetchall()
    conn.commit()
    conn.close()

    return jsonify(var)

# READ - Ottieni un singolo studente per ID
@app.route("/studenti/<int:id>", methods=["GET"])
def get_studente(id):
    conn = sqlite3.connect("./databaseB.db")
    cur = conn.cursor()
    cur.execute('SELECT * FROM studenti WHERE id = ?', (id,))
    var = cur.fetchone()
    conn.close()
    if var:
        return jsonify(var)
    return jsonify({"errore": "Studente non trovato"}), 404

# UPDATE - Modifica i dati di uno studente
@app.route("/studenti/<int:id>", methods=["PUT"])
def update_studente(id):
    data = request.get_json()
    
    nome = data.get('nome')
    cognome = data.get('cognome')
    eta = data.get('eta')
    
    conn = sqlite3.connect("./databaseB.db")
    cur = conn.cursor()
    cur.execute('SELECT * FROM studenti WHERE id = ?', (id,))
    studente = cur.fetchone()
    
    if studente:  
        cur.execute("UPDATE studenti SET nome = ?, cognome = ?, eta = ? WHERE id = ?", (nome, cognome, eta, id))
        conn.commit()
        conn.close()
        return jsonify({"messaggio": "Studente aggiornato"})
    
    conn.close()
    return jsonify({"errore": "Studente non trovato"}), 404


# DELETE - Elimina uno studente
@app.route("/studenti/<int:id>", methods=["DELETE"])
def delete_studente(id):
    conn = sqlite3.connect("./databaseB.db")
    cur = conn.cursor()
    cur.execute('''DELETE FROM studenti WHERE id=?''', id)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    app.run(debug=True)

