import socket
import libreriaPynput

SERVER_ADDRESS = ("192.168.1.130", 9090)
BUFFER_SIZE = 4096

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    key_comandi = {"w": "forward"}
    statoKey = {"w": True}

    pressed = False

    while True:

        if libreriaPynput.on_press(): 
            pressed = True
         
        elif libreriaPynput.on_release('w'): 
            pressed = False

            #message = f"{command}|{inputValue}"
            
        s.sendall(message.encode())
        message = s.recv(BUFFER_SIZE)
        print(f"Ricevuto <{message.decode()}> dal server")

            
    s.close()
if __name__ == '__main__':
    main()