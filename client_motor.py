import socket
from pynput import keyboard

#SERVER_ADDRESS = ("192.168.1.130", 9090)
SERVER_ADDRESS = ("127.0.0.1", 9090)

BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)
key_comandi = {"w": "forward", "s" : "backward", "a" : "left", "d" : "right", "f" : "stop"}
statoKey = {"w": False, "s": False, "a": False, "d": False, "f": False}
message = "stop"

# funzione chiamata quando un tasto viene premuto
def on_press(key):
    print("pressione")
    if key.char in key_comandi:
        if statoKey[key.char] == False:
            statoKey[key.char] = True
        if statoKey[key.char] == True:
            print(f"{key.char} premuto")
            '''
            if statoKey[key.char] == "w":
                message = "50|50"
            elif statoKey[key.char] == "s":
                message = "-50|-50"
            elif statoKey[key.char] == "a":
                message = "-50|0"
            elif statoKey[key.char] == "d":
                message = "50|-50"
            print(message) '''
            s.sendall(f"{key_comandi[key.char]}".encode())
            print("Inviato")
    else:
        print("errore con il tasto")
    
def on_release(key):
    if key.char in key_comandi:
        if statoKey[key.char] == True:
            statoKey[key.char] = False
            print(f"{key.char} rilasciato")
            
            s.sendall(message.encode())
            print("inviato")

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    start_listener()
    
    while True:
        pass
        #message = s.recv(BUFFER_SIZE)
        #prwint(f"Ricevuto <{message.decode()}> dal server")

        
        
if __name__ == '__main__':
    main()