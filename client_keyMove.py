import socket
import libreriaPynput

SERVER_ADDRESS = ("192.168.1.130", 9090)
BUFFER_SIZE = 4096

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    key_comandi = {"w": "forward"}
    statoKey = {"w": False}

    key = 'w'

    while True:

        if libreriaPynput.on_press(key): 
            statoKey[key] = True
         
        elif libreriaPynput.on_release(key): 
            statoKey[key] = False

        if statoKey[key] == True: 
            message = f"{key_comandi[key]}|{1}"
        else:
            message = f"{"stop"}|{1}"
            
        s.sendall(message.encode())
        message = s.recv(BUFFER_SIZE)
        print(f"Ricevuto <{message.decode()}> dal server")

        
        
if __name__ == '__main__':
    main()