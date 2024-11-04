# Questo codice implementa un client che si connette a un robot tramite socket 
# invia la potenza dei motori per compiere il movimento al client

import socket
from pynput import keyboard

# indirizzo ip e porta del server
#SERVER_ADDRESS = ("192.168.1.130", 9090)
SERVER_ADDRESS = ("127.0.0.1", 9090) # Indirizzo di loopback per testare localmente

BUFFER_SIZE = 4096

# creazione socket e connessione
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)

# dizionario per associare i tasti ai comandi di movimento
key_comandi = {
    "w": (50, 50),     # Avanti
    "s": (-50, -50),   # Indietro
    "a": (-50, 50),    # Sinistra
    "d": (50, -50),    # Destra
    "f": (0, 0)        # Stop
}

# stato dei tasti: True se il tasto è premuto
statoKey = {"w": False, "s": False, "a": False, "d": False, "f": False}
# Potenza attuale dei motori
motor1 = 0
motor2 = 0

# funzione chiamata quando un tasto viene premuto
def on_press(key):
    global motor1, motor2  # Riferimento alle variabili motor1 e motor2

    print("pressione")
    if key.char in key_comandi: # controlla se il tasto premuto è in key_comandi
        print(f"{key.char} premuto")
        if statoKey[key.char] == False:
            statoKey[key.char] = True        
            
            print(f"Sinistro = {motor1}, Destro = {motor2}")

            # invio del comando per il movimento al server
            #for key in statoKey:
            # if statoKey[key]:
            left_power, right_power = key_comandi[key.char]
            motor1 += left_power
            motor2 += right_power
            if motor1 > 100:
                motor1 = 100
            elif motor1 < -100:
                motor1 = 0
            if motor2 > 100:
                motor2 = 100
            elif motor2 < -100:
                motor2 = 0
            
        s.sendall(f"{motor1}|{motor2}".encode())
        print(f"Inviato {motor1}|{motor2}")
    else:
        print("errore con il tasto")

# funzione chiamata quando un tasto viene rilasciato
def on_release(key):
    global motor1, motor2  # Riferimento alle variabili motor1 e motor2

    if key.char in key_comandi:
        # se il tasto non era rilasciatp aggiorna il suo stato
        if statoKey[key.char] == True:
            statoKey[key.char] = False
            print(f"{key.char} rilasciato")

            #for key in statoKey:
             #   if statoKey[key]:
            left_power, right_power = key_comandi[key.char]
            motor1 -= left_power
            motor2 -= right_power
            s.sendall(f"{motor1}|{motor2}".encode())
            print("Inviato")

# funzione per avviare il listener della tastiera
def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    start_listener()
        
if __name__ == '__main__':
    main()