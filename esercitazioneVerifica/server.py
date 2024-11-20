#SERVER FILE SHARING
#server riceve costantemente le interrogazioni da tutti i client connessi, tramite protocollo TCP.
#questo server può gerstire più client con i thread e cerca le informazioni all'interno di un database sqlite3
#POSSIBILI RICHIESTE (messaggio ricevuto) 'numeroIstruzione|datiNecessari:
#                      '1|nomeFile'
#                      '2|nomeFile'
#                      '3|nomeFile,numFrammento'
#                      '4|nomeFile'

#POSSIBILI RISPOSTE (messaggio inviati):
#                      'File presente nel database' o 'File non presente nel database'
#                      'Numero di frammenti: numero intero di frammenti del file'
#                      'Host Frammento: indirizzo IP dell'host del frsammento richiesto'
#                      'HOST: elenco degli indirizzo IP degli host con un frammento del file'
#                      'ERRORE'


import socket
import threading
import sqlite3

MY_ADDRESS = ("127.0.0.1", 9000) #indirizzo e porta server
BUFFER_SIZE = 4096 
DATABASE = 'file.db' #nome file database


class Client(threading.Thread):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address
        self.running = True

    def run(self):
        while self.running:
            message = self.connection.recv(BUFFER_SIZE).decode()
            if message == "": #se il messaggio è vuoto il client si è disconnesso
                self.running = False
                self.connection.close()
                break
            else:
                conn = sqlite3.connect(DATABASE) # connessione al database
                cur = conn.cursor() # serve per far girare il database

                message = message.split('|') # divido il messaggio per creare una lista con la richiesta e i dati necessari
                istruzione = int(message[0]) # valore della richiesta del client
                #print(istruzione)
                #print(message[1])
                if istruzione == 1:
                    if self.isFileHere(message[1], cur):
                        risp = "File presente nel database"
                    else:
                        risp = "File non presente nel database"
                elif istruzione == 2:
                    risp = 'Numero di frammenti: ' + str(self.numeroFrammenti(message[1], cur))
                elif istruzione == 3:
                    nomeFile, numFrammento = message[1].split(',')
                    risp = 'Host Frammento: ' + self.ipHostFrammento(nomeFile, int(numFrammento), cur)
                elif istruzione == 4:
                    risp = self.ipHostFile(message[1], cur)
                else:
                    risp = 'ERRORE'

                self.connection.send(risp.encode())
                #print(query)
                #self.connection.send(query.encode())
                #cur.execute(query)
                #risposta = cur.fetchall()


    def isFileHere(self, nomeFile, cur):
        # ritorna true se il file è presente nel database
        # ritorna false se il file non è presente nel database
        query = f'''SELECT nome
                FROM files
                WHERE nome = "{nomeFile}" '''
        cur.execute(query)
        risposta = cur.fetchall()
        if risposta:
            return True
        else:
            return False


    def numeroFrammenti(self, nomeFile, cur):
        query = f'''SELECT tot_frammenti
                FROM files
                WHERE nome = "{nomeFile}" '''
        cur.execute(query)
        risposta = cur.fetchall() #lista con il risultato della query
        # controllo che il risultato della query non sia vuoto(se lo è non sono stati trovati valori nel file o il file non esiste nel database)
        if risposta:
            risp = risposta[0] #tupla con il valore richiesto
            return risp[0]
        else:
            return "ERRORE"
        
    
    def ipHostFrammento(self, nomeFile, numFrammento, cur):
        query = f'''SELECT host
                FROM frammenti, files
                WHERE frammenti.id_file = files.id_file
                AND files.nome = "{nomeFile}" 
                AND n_frammento = "{numFrammento}"'''
        cur.execute(query)
        risposta = cur.fetchall()
        # controllo che il risultato della query non sia vuoto(se lo è non sono stati trovati valori nel file o il file non esiste nel database)
        if risposta:
            risp = risposta[0]
            return risp[0]
        else:
            return "ERRORE"

    def ipHostFile(self, nomeFile, cur):
        query = f'''SELECT DISTINCT host
                FROM frammenti, files
                WHERE frammenti.id_file = files.id_file
                AND files.nome = "{nomeFile}"'''
        cur.execute(query)
        risposta = cur.fetchall()
        # controllo che il risultato della query non sia vuoto(se lo è non sono stati trovati valori nel file o il file non esiste nel database)
        if risposta:
            messaggio = "HOST: "
            for host in risposta:
                messaggio += host[0] + ' \n'
            return messaggio
        else:
            return "ERRORE"



def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()

    while True:
        connection, client_address = s.accept()
        print(f"Il client {client_address} si è connesso")
        thread = Client(connection, client_address)
        thread.start()

if __name__ == "__main__":
    main()