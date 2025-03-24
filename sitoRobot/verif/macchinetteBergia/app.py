from VendingMachine import VendingMachine
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, make_response
from datetime import datetime
import time

app = Flask(__name__)

# Crea un'istanza della classe VendingMachine
vm = VendingMachine()

def create_db():
    conn = sqlite3.connect("./database.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS utenti(
                username VARCHAR(20) PRIMARY KEY,
                psw VARCHAR(20) NOT NULL,
                tipo VARCHAR(10) NOT NULL
                )''')
    conn.commit()
    conn.close()

def data():
    conn = sqlite3.connect("./database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM utenti")
    var = cur.fetchall()
    utenti = {r[0]: [r[1], r[2]] for r in var}

    return utenti

def check_account(username,psw):
    account = data()
    if psw == account[username][0]:
        return True
    else:
        print(f"errore u:{username} pI:{psw} pD:{account[username][0]}")
        return False
    
@app.route('/')
def index():
    return redirect(url_for("login"))
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    account = data()
    if request.method == 'POST':
        username = request.form['username']
        psw = request.form['psw']
        tipo = account[username][1]
        if check_account(username,psw):
            if tipo == "user":
                return redirect(url_for("user"))
            return redirect(url_for("home"))
        else:
            print("login fallito")
    return render_template("accesso.html")

@app.route("/user", methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
            soldi_caricati = float(request.form['soldi_caricati'])
            id = request.form["product_id"]
            resto = vm.vend(id, soldi_caricati)
    return render_template('products.html', products=vm.products)
        
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'add_product' in request.form:
            id = int(request.form['product_id'])
            nome = request.form['nome']
            prezzo = float(request.form['prezzo'])
            stock = int(request.form['stock'])
            vm.add_product(id, nome, prezzo, stock)
            return render_template('admin.html', products=vm.products)

        elif 'remove_product' in request.form:
            id = int(request.form['product_id'])
            vm.remove_product(id)
            return render_template('admin.html', products=vm.products)

        elif 'modify_stock' in request.form:
            # Modifica la quantità di un prodotto
            id = int(request.form['id'])
            new_stock = int(request.form['new_stock'])
            vm.restock(id, new_stock)
            return render_template('admin.html', products=vm.products)
            
    return render_template('admin.html', products=vm.products)


           
    

if __name__ == '__main__':
    app.run(debug=True, host="localhost")