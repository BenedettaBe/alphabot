import sqlite3

#connessione al database
conn = sqlite3.connect('mio_database_Benny.db')
cur = conn.cursor() # serve per far girare il database
query = '''INSERT INTO comandi("P_K", "str_mov") VALUES
            ("v", "f40,l20,f20"),
            ("x", "f30,l40,f20"),
            ("y", "f40,l60,f20"),
            ("z", "f40,l80,f20");'''
print(query)
cur.execute(query)
conn.commit()
variabile_in_stampa = cur.fetchall()