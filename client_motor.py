# Questo codice implementa un client che si connette a un robot tramite socket 
# invia comandi di movimento  per il robot in risposta alla pressione di tasti sulla tastiera
# w: avanti, s: indietro, a: sinistra, d:destra, f: stop

import socket
from pynput import keyboard

# indirizzo ip e porta del server
SERVER_ADDRESS = ("192.168.1.130", 9090)
#SERVER_ADDRESS = ("127.0.0.1", 9090) # Indirizzo di loopback per testare localmente

BUFFER_SIZE = 4096

# creazione socket e connessione
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)

# dizionario per associare i tasti ai comandi di movimento
key_comandi = {"w": "forward", "s" : "backward", "a" : "left", "d" : "right", "f" : "stop"}

# stato dei tasti: True se il tasto è premuto
statoKey = {"w": False, "s": False, "a": False, "d": False, "f": False}
message = "stop" # messaggio predefinito per fermare il robot

# funzione chiamata quando un tasto viene premuto
def on_press(key):
    print("pressione")
    if key.char in key_comandi: # controlla se il tasto premuto è in key_comandi
        # se il tasto non era premuto aggiorna il suo stato
        if statoKey[key.char] == False:
            statoKey[key.char] = True

        if statoKey[key.char] == True:
            print(f"{key.char} premuto")
            # invio del comando per il movimento al server
            s.sendall(f"{key_comandi[key.char]}".encode())
            print("Inviato")
    else:
        print("errore con il tasto")

# funzione chiamata quando un tasto viene rilasciato
def on_release(key):
    if key.char in key_comandi:
        # se il tasto non era rilasciatp aggiorna il suo stato
        if statoKey[key.char] == True:
            statoKey[key.char] = False
            print(f"{key.char} rilasciato")
            # invio del comando di stop al server
            s.sendall(message.encode())
            print("inviato")

# funzione per avviare il listener della tastiera
def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    start_listener()
        
if __name__ == '__main__':
    main()