import sqlite3

#connessione al database
conn = sqlite3.connect('mio_databaseB.db')
cur = conn.cursor() # serve per far girare il database

cur.execute('''CREATE TABLE comandi(
            "P_K" VARCHAR(1) NOT NULL UNIQUE,
            "str_mov" TEXT NOT NULL,
            PRIMARY KEY("P_K")
            );''')
conn.commit()
variabile_in_stampa = cur.fetchall()