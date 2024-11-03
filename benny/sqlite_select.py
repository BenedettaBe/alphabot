import sqlite3

#connessione al database
conn = sqlite3.connect('mio_database_Benny.db')
cur = conn.cursor() # serve per far girare il database
query = '''SELECT *
    FROM comandi'''
print(query)
cur.execute(query)
conn.commit()
variabile_in_stampa = cur.fetchall()
print(variabile_in_stampa)
tasto = 'v'
if variabile_in_stampa:
    query = f'''SELECT str_mov
    FROM comandi
    WHERE comandi.P_K = "{tasto}"'''
    print(query)
    cur.execute(query)
    risposta = cur.fetchall()
    risp = risposta[0]
    comando = risp[0]
    print(comando)
    list_comandi = comando.split(",")
    print(list_comandi)
    for c in list_comandi:
        print(c[0])#lettera
        print(c[1:]) #movimento