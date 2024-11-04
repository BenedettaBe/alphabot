import sqlite3

#connessione al database
conn = sqlite3.connect('mio_databaseB.db')
cur = conn.cursor() # serve per far girare il database
query = '''INSERT INTO comandi("P_K", "str_mov") VALUES
            ("v", "w4,d1,s3"),
            ("x", "w3,a2"),
            ("y", "s4,d1,w3"),
            ("z", "s2,a2,s1");'''
print(query)
cur.execute(query)
conn.commit()
variabile_in_stampa = cur.fetchall()