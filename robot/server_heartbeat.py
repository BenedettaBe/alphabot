from AlphaBot import AlphaBot
import socket
import time

MYADDRESS = ("192.168.1.130", 9090)
BUFFER_SIZE = 4096

# Dizionario di traduzione per i comandi di movimento
key_comandi = {"forward": "1|1", "backward": "-1|-1", "left": "-1|1", "right": "1|-1", "stop": "0|0"}

def main():
    robot = AlphaBot()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()
    motor1 = 0
    motor2 = 0
    robot.setMotor(motor1, motor2)

    #connessione con il client
    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")
    
    while True:
        message = connection.recv(BUFFER_SIZE).decode()
        if not message:
                print("Connessione persa")
                break
        print(f"Messaggio ricevuto: {message}")

        motor1, motor2 = key_comandi[message].split('|')
        print(motor1, motor2)
        motor1 = int(motor1)
        motor2 = int(motor2)
        

        robot.setMotor(motor1, motor2)     

if __name__ == '__main__':
    main()
