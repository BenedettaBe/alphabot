# Questo codice implementa un client che si connette a un robot tramite socket 
# invia comandi di movimento  per il robot in risposta alla pressione di tasti sulla tastiera
# w: avanti, s: indietro, a: sinistra, d:destra, f: stop

import socket
from pynput import keyboard
from threading import Thread
import time


# Indirizzo IP e porta del server per la comunicazione con il robot e l'heartbeat
SERVER_ADDRESS = ("192.168.1.130", 9090)
HEARTBEAT_ADDRESS = ("192.168.1.130", 9091) 

# Indirizzo IP e porta di loopback per testare localmente
#SERVER_ADDRESS = ("127.0.0.1", 9090) 
#HEARTBEAT_ADDRESS = ("127.0.0.1", 9091) 

BUFFER_SIZE = 4096

stop_heartbeat = False # Per gestire l'invio dei thread heartbeat

# creazione socket e connessione al server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)

# lista per tracciare lo stato dei tasti e i comandi corrispondenti
listaPremuti = []


def heartbeat_send():
    """
    Funzione che invia continuamente un messaggio di 'heartbeat' al server per 
    mantenere attiva la connessione. Se il server non riceve heartbeat chiude la connessione.
    """
    global stop_heartbeat
    send_heartbeat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_heartbeat.connect(HEARTBEAT_ADDRESS)
    
    while not stop_heartbeat:
        try:
            # invio continuo del messaggio per tenere la connessione attiva
            send_heartbeat.sendall("heartbeat".encode())
            #print("Heartbeat inviato.")    
            time.sleep(1) # attende 1 secondo prima di inviare il prossimo heartbeat
        except Exception as e:
            # se c'è un errore interrompe la comunicazione
            print(f"Errore nel thread heartbeat: {e}")
            break
    
    send_heartbeat.close() # chiusura del socket heartbeat
    print("Connessione heartbeat chiusa.")


def on_press(key):
    '''    
    funzione chiamata quando un tasto viene premuto
    Invia il tasto al server con un messaggio "P|{tasto}" 
    con 'P' il server comprende che il tasto è premuto
    '''    
    tasto = key.char
    # controllo che il tasto non sia ancora nella lista premuti
    # così da mandare al server il messaggio una singola volta
    if tasto not in listaPremuti:
        #print("pressione")
        listaPremuti.append(tasto) # aggiunta del tasto nella lista
        message = f"P|{tasto}" # creazione messaggio predefinito
        print(message)
        s.sendall(message.encode()) # invio messaggio al server

def on_release(key):
    '''    a
    funzione chiamata quando un tasto viene rilasciato
    Invia il tasto al server con un messaggio del tipo "R|{tasto}" 
    con 'R' il server comprende che il tasto è rilasciato
    ''' 
    tasto = key.char
    print(tasto)

    # controllo che il tasto sia ancora nella lista premuti
    # così da mandare al server il messaggio una singola volta
    if tasto in listaPremuti:
        listaPremuti.remove(tasto) # rimozione del tasto nella lista
    message = f"R|{tasto}" # creazione messaggio predefinito
    print(message)
    s.sendall(message.encode()) # invio messaggio al server
    time.sleep(0.001)

def start_listener():
    '''
    funzione per avviare il listener della tastiera
    '''
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    global stop_heartbeat 
    t = Thread(target=heartbeat_send) # thread per controllo sull'heartbeat
    t.start() # avvio thread heartbeat

    start_listener()  # avvio ascolto la tastiera
    
    stop_heartbeat = True # ferma l'invio di heartbeat
    t.join()  # attende la chiusura del thread
    s.close()  # chiusura della connessione del socket
    print("Client terminato.")
        
if __name__ == '__main__':
    main()