#Questo codice implementa un server-robot che a cui si connette un client tramite socket 
#riceve comandi di movimento e a ogni comando che riceve attribuisce 
#il valore dei motori per poter svolgere il movimento
from AlphaBot import AlphaBot
import socket
import threading
import time

# indirizzo ip e porta del server
MYADDRESS = ("192.168.1.130", 9090)
BUFFER_SIZE = 4096

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

def main():
    global motor1, motor2

    robot = AlphaBot()
    
    # creazione socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()
    robot.setMotor(motor1, motor2)

    # connessione con il client
    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")
    
    while True:
        message = connection.recv(BUFFER_SIZE).decode()
        print(f"Messaggio ricevuto: {message}")

        # estraggo i valori per i motori dal dizionario key_comandi
        if message in key_comandi: # controlla se il tasto premuto è in key_comandi
            print(f"{message} premuto")    
            print(f"Sinistro = {motor1}, Destro = {motor2}")
            if message == 'f':
                motor1 = 0
                motor2 = 0
            else:
                left_power, right_power = key_comandi[message]
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
        
        # Imposto i motori del robot secondo i comandi ricevuti
        robot.setMotor(motor1, motor2)     

if __name__ == '__main__':
    main()
