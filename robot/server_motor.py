#Questo codice implementa un server-robot che a cui si connette un client tramite socket 
#riceve comandi di movimento e a ogni comando che riceve attribuisce 
#il valore dei motori per poter svolgere il movimento
from AlphaBot import AlphaBot
import socket

# indirizzo ip e porta del server
MYADDRESS = ("192.168.1.130", 9090)
BUFFER_SIZE = 4096

# dizionario per associare i comandi di movimento al valore dei motori
key_comandi = {"forward": "50|50", "backward": "-50|-50", "left": "-50|50", "right": "50|-50", "stop": "0|0"}

def main():
    robot = AlphaBot()
    
    # creazione socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()

    # imposto i motori a robot fermo
    motor1 = 0
    motor2 = 0
    robot.setMotor(motor1, motor2)

    # connessione con il client
    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")
    
    while True:
        message = connection.recv(BUFFER_SIZE).decode()
        print(f"Messaggio ricevuto: {message}")

        # estraggo i valori per i motori dal dizionario key_comandi
        motor1, motor2 = key_comandi[message].split('|')
        print(motor1, motor2)
        motor1 = int(motor1)
        motor2 = int(motor2)
        # Imposto i motori del robot secondo i comandi ricevuti
        robot.setMotor(motor1, motor2)     

if __name__ == '__main__':
    main()
