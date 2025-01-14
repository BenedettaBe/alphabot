import socket
from pynput import keyboard
from threading import Thread
import time


SERVER_ADDRESS = ("192.168.1.130", 9090)
HEARTBEAT_ADDRESS = ("192.168.1.130", 9091)

BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)
key_comandi = {"w": "forward", "s" : "backward", "a" : "left", "d" : "right", "f" : "stop"}
statoKey = {"w": False, "s": False, "a": False, "d": False, "f": False}

def heartbeat_sender():
    send_heartbeat= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_heartbeat.connect(HEARTBEAT_ADDRESS)
    while True:
        try:
            send_heartbeat.sendall("a".encode())
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            break
    send_heartbeat.close()

# funzione chiamata quando un tasto viene premuto
def on_press(key):
    print("pressione")
    #if key in key_comandi:
    if statoKey[key.char] == False:
        statoKey[key.char] = True
        print("premuto")
    if statoKey[key.char] == True:
        message = key.char
        #message = f"{key_comandi[key.char]}|{1}"
        s.sendall(message.encode())
        print("Inviato")
    #else:
        #print("errore con il tasto")
    
def on_release(key):
    print("rilasciando")
    #if key in key_comandi:
    if statoKey[key.char] == True:
        statoKey[key.char] = False
        print("rilasciato")
        message = 'f'

        #message = f"{'stop'}|{1}"
        s.sendall(message.encode())
        print("inviato")
    #else:
        #print("errore con il tasto")

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    t = Thread(target=heartbeat_sender)
    t.start()
    start_listener()
    
    while True:
        message = s.recv(BUFFER_SIZE)
        print(f"Ricevuto <{message.decode()}> dal server")

        
        
if __name__ == '__main__':
    main()