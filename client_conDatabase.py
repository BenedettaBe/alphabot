# Questo codice implementa un client che si connette a un robot tramite socket 
# invia comandi di movimento  per il robot in risposta alla pressione di tasti sulla tastiera
# w: avanti, s: indietro, a: sinistra, d:destra, f: stop

import socket
from pynput import keyboard
from threading import Thread
import time



# indirizzo ip e porta del server
SERVER_ADDRESS = ("192.168.1.130", 9090)
HEARTBEAT_ADDRESS = ("192.168.1.130", 9091) 
stop_heartbeat = False
#SERVER_ADDRESS = ("127.0.0.1", 9090) # Indirizzo di loopback per testare localmente

BUFFER_SIZE = 4096

# creazione socket e connessione
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)

# dizionario per associare i tasti ai comandi di movimento
key_comandi = {"w": "forward", "s" : "backward", "a" : "left", "d" : "right", "f" : "stop"}

# stato dei tasti: True se il tasto è premuto
#statoKey = {"w": False, "s": False, "a": False, "d": False, "f": False}
message = "stop" # messaggio predefinito per fermare il robot
statoKey = {}


def heartbeat_send(): #funzione per il controllo della comunicazione con il server
    global stop_heartbeat
    send_heartbeat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_heartbeat.connect(HEARTBEAT_ADDRESS)
    while not stop_heartbeat:
        try:
            #invio continuo del messaggio per tenere la connessione attiva
            send_heartbeat.sendall("heartbeat".encode())
            #print("Heartbeat inviato.")    
            time.sleep(1)
        except Exception as e:
            #se c'è un errore blocca tutto
            print(f"Errore nel thread heartbeat: {e}")
            break
    
    send_heartbeat.close()
    print("Connessione heartbeat chiusa.")


# funzione chiamata quando un tasto viene premuto
def on_press(key):
    tasto = key.char
    if tasto not in statoKey:
        statoKey[tasto] = True
        print("pressione")
        message = f"P|{tasto}"
        s.sendall(message.encode())
    elif statoKey[tasto] == False:
        statoKey[tasto] = True
        message = f"P|{tasto}"
        s.sendall(message.encode())

       

    '''
    if tasto in key_comandi: # controlla se il tasto premuto è in key_comandi
        # se il tasto non era premuto aggiorna il suo stato
        if statoKey[tasto] == False:
            statoKey[tasto] = True

        if statoKey[tasto] == True:
            print(f"{tasto} premuto")
            # invio del comando per il movimento al server
            s.sendall(f"{tastoencode())
            print("Inviato")
    else:
        print("errore con il tasto")
'''
# funzione chiamata quando un tasto viene rilasciato
def on_release(key):
    tasto = key.char
    print(tasto)
    if tasto in statoKey and statoKey[tasto]:
        statoKey[tasto] = False
        message = f"R|{tasto}"
        s.sendall(message.encode())

    '''if tasto in key_comandi:
        # se il tasto non era rilasciatp aggiorna il suo stato
        if statoKey[tasto] == True:x
            statoKey[tasto] = False
            print(f"{tasto} rilasciato")
            # invio del comando di stop al server
            s.sendall(message.encode())
            print("inviato")
'''
# funzione per avviare il listener della tastiera
def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    global stop_heartbeat 
    t = Thread(target=heartbeat_send) #thread per controllo temporaneo sull'heartbeat
    t.start()   #parte il thread
    try:
        start_listener()  # Ascolta la tastiera
    except KeyboardInterrupt:
        print("Interruzione del client.")
    finally:
        # Quando il client termina, ferma l'heartbeat e chiudi la connessione
        stop_heartbeat = True
        t.join()
        s.close()  # Chiudi la connessione del socket
        print("Client terminato.")
        
if __name__ == '__main__':
    main()