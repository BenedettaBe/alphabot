from AlphaBot import AlphaBot # libreria per il robot AlphaBo
import socket
import sqlite3
import time
from threading import Thread


MYADDRESS = ("192.168.1.130", 9090)
HEART_BEAT_ADDRESS = ("192.168.1.130",9091)
BUFFER_SIZE = 4096

def heartbeat_recive(heartbeat, robot):
    
    #setta un timer di 2 secondi sul socket
    heartbeat.settimeout(2)
    
    #controlla che non ci siano problemi nella connessione
    try:
        while True:
            try:
                
                #riceve il messaggio dal client
                data = heartbeat.recv(BUFFER_SIZE).decode()
                
                #controlla che il messaggio non sia vuoto
                if data == "heartbeat":
                    #print("Heartbeat ricevuto.")
                    pass
                elif not data:
                    print("Heartbeat vuoto, terminazione.")
                    break
                
            #eccezione nel caso in cui il timer di 2 secondi sul socket scade prima che riceva un messaggio
            except socket.timeout:
                print("Timeout del heartbeat. Fermare il robot.")
                robot.stop()	#ferma i motori così si evita che continui ad andare avanti all'infinito
                
            #eccezione nel caso di un errore nella comunicazione
            except Exception as e:
                print(f"Errore nel ricevere heartbeat: {e}")
                break
    finally:
        heartbeat.close()
        print("Connessione heartbeat chiusa.")


def main():
    # mappatura dei tasti alle azioni (movimenti) del robot
    key_comandi = {
    "w": (25, 25),     # Avanti
    "s": (-25, -25),   # Indietro
    "a": (25, 0),    # Sinistra
    "d": (0, 25),    # Destra
    "f": (0, 0)        # Stop
    }
    listaPremuti = [] # lista per tenere traccia dei tasti premuti

    robot = AlphaBot()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()

    robot.stop() # ferma il robot per sicurezza

    #crea il collegamento tramite socket tra pc e alphabot per il controllo della connessione.
    heartbeat_recived = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    heartbeat_recived.bind(HEART_BEAT_ADDRESS)
    heartbeat_recived.listen(1)
    
    # connessione con il client
    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")
    
    # accetta la connessione per ricevere i messaggi di heartbeat
    recive_heartbeat, _ = heartbeat_recived.accept()

    # connessione al database
    conn = sqlite3.connect('mio_databaseB.db')
    cur = conn.cursor() # serve per eseguire le query sul database
    
    # crea il thread per il controllo della connessione tra pc e alphabot tramite la funzione heartbeat_recive
    thread_heartbeat = Thread(target=heartbeat_recive, args=(recive_heartbeat,robot))
    thread_heartbeat.start()

    # query per ottenere i comandi dal database
    query = '''SELECT *
        FROM comandi'''
    print(query)
    cur.execute(query)
    conn.commit()
    variabile_in_stampa = cur.fetchall()
    print(variabile_in_stampa)

    while True:
        messaggio = connection.recv(BUFFER_SIZE).decode()
        if not messaggio: # se il messaggio è vuoto, blocca la comunicazione
            break 

        stato, tasto = messaggio.split('|') # Divide il messaggio in stato (P o R) e tasto
        #print(f"Messaggio ricevuto: {stato} | {tasto}")
        
        # se il tasto è vuoto, interrompe l'esecuzione
        if tasto == "":
            break

        # aggiunge o rimuove il tasto dalla lista dei tasti premuti
        if stato == "P":
            listaPremuti.append(tasto)
        elif stato == "R":
            listaPremuti.remove(tasto)
                
        motor1, motor2 = 0,0
        for t in listaPremuti:
            if t == 'f':
                robot.setMotor(0, 0)

            elif t in key_comandi:
                potenzaMovimento = key_comandi[t]
                # se è premuto 's' e il robot deve andare obliquamente a destra e a sinistra la direzione è inversa
                if 's' in listaPremuti and (t == 'a' or t == 'd'):
                    motor1 -= potenzaMovimento[0]
                    motor2 -= potenzaMovimento[1]
                else:
                    motor1 += potenzaMovimento[0]
                    motor2 += potenzaMovimento[1]

                motor1 = int(motor1)
                motor2 = int(motor2)
                robot.setMotor(motor1, motor2) 

            # se esistono i comandi nel database fa la ricerca del tasto
            elif variabile_in_stampa:
                # query di ricerca
                query = f'''SELECT str_mov
                        FROM comandi
                        WHERE P_K = "{tasto}"'''
                # print(query)
                cur.execute(query)
                risposta = cur.fetchall()
                # print(f"risposta: {risposta}")
                if risposta:
                    comando = risposta[0][0]
                    # print(f"comando: {comando}")
                    list_comandi = comando.split(",") # divide i comandi con la virgola
                    # print(f"lista comandi: {list_comandi}")

                    for comando in list_comandi:
                        movimento = comando[0] # carattare wasdf
                        durata = float(comando[1:]) # durata del movimento
                        potenzaMovimento = key_comandi[movimento] # ottieni la potenza dei motori per il movimento
                        motor1 = int(potenzaMovimento[0])
                        motor2 = int(potenzaMovimento[1])
                        #print(motor1, motor2)
                        robot.setMotor(motor1, motor2) 
                        time.sleep(durata)
     

if __name__ == '__main__':
    main()
