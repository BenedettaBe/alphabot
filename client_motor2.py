# Questo codice implementa un client che si connette a un robot tramite socket 
# invia il tasto premuto
import socket
from pynput import keyboard

# indirizzo ip e porta del server
#SERVER_ADDRESS = ("192.168.1.130", 9090)
SERVER_ADDRESS = ("127.0.0.1", 9090) # Indirizzo di loopback per testare localmente

BUFFER_SIZE = 4096

# creazione socket e connessione
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)

# funzione chiamata quando un tasto viene premuto
def on_press(key):
    print("pressione")
    s.sendall(f"{key.char}".encode())
    print(f"Inviato {key.char}")
    

# funzione chiamata quando un tasto viene rilasciato
def on_release(key):
    s.sendall(f"{key.char}".encode())
    print("Inviato")

# funzione per avviare il listener della tastiera
def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    start_listener()
        
if __name__ == '__main__':
    main()