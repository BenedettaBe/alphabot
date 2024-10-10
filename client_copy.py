import socket

SERVER_ADDRESS = ("192.168.1.130", 9090)
BUFFER_SIZE = 4096

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    comandi = {"1": "forward", "2" : "backward", "3" : "left", "4" : "right", "5" : "stop"}

    while True:
        inputCommand = input("Inserisci il numero corrispondente al comando: (1.forward 2.indietro 3. sinistra 4.destra 5.stop) ")
        
        if inputCommand in comandi:
            command = comandi[inputCommand]

            inputValue = input("Inserisci il valore: ")
            message = f"{command}|{inputValue}"
    
            message = f"{command}|{inputValue}"
            s.sendall(message.encode())
            message = s.recv(BUFFER_SIZE)
            print(f"Ricevuto <{message.decode()}> dal server")

        else:
            print("error")
            
    s.close()
if __name__ == '__main__':
    main()