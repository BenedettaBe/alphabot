import socket
import time

MYADDRESS = ("127.0.0.1", 9090)  # Modifica con il tuo indirizzo IP locale
BUFFER_SIZE = 4096

# Funzioni simulate per comportarsi come il robot
def setMotor(left, right):
    # Simuliamo la gestione dei motori stampando i valori dei motori
    print(f"[SIMULAZIONE] Motore sinistro: {left}, Motore destro: {right}")
    if left > 0 and right > 0:
        print(f"[SIMULAZIONE] Robot va avanti")
    elif left < 0 and right < 0:
        print(f"[SIMULAZIONE] Robot va indietro")
    elif left < 0 and right > 0:
        print(f"[SIMULAZIONE] Robot gira a sinistra")
    elif left > 0 and right < 0:
        print(f"[SIMULAZIONE] Robot gira a destra")
    elif left == 0 and right == 0:
        print(f"[SIMULAZIONE] Robot fermo")
    else:
        print(f"[SIMULAZIONE] Comando sconosciuto")

def stop():
    # Simuliamo la fermata del robot
    print(f"[SIMULAZIONE] Robot fermato.")

def main():
    # Il server attende connessioni dal client
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()

    print(f"Server in ascolto su {MYADDRESS}")
    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")
    motor1 = 0
    motor2 = 0
    while True:
        
            # Ricezione messaggi dal client
        message = connection.recv(BUFFER_SIZE).decode()
        if not message:
            print("Connessione persa")
            break
        print(f"Messaggio ricevuto: {message}")

            
        motor1value, motor2value = message.split('|')
        print(f"Potenza ricevuta: Sinistro = {motor1value}, Destro = {motor2value}")
        motor1 = int(motor1value)
        motor2 = int(motor2value)
          

        # Simula l'azione sui motori
        setMotor(motor1, motor2)

            # Invia conferma al client
        connection.send(f"ok|Motori impostati a {motor1} e {motor2}".encode())


if __name__ == '__main__':
    main()
