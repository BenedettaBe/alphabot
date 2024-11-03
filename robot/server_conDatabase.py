#INCOMPLETO: manca heart beat
from AlphaBot import AlphaBot
import socket
import sqlite3
import time

MYADDRESS = ("192.168.1.130", 9090)
BUFFER_SIZE = 4096

# Dizionario di traduzione per i comandi di movimento
#key_comandi = {"w": "50|50", "s": "-50|-50", "d": "-50|50", "a": "50|-50", "f": "0|0"}
key_comandi = {"w": "forward", "s" : "backward", "a" : "left", "d" : "right", "f" : "stop"}


def main():
    robot = AlphaBot()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()
    motor1 = 0
    motor2 = 0
    robot.setMotor(motor1, motor2)

    #connessione al database
    conn = sqlite3.connect('mio_database_Benny.db')
    cur = conn.cursor() # serve per far girare il database
    #connessione con il client
    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")
    
    query = '''SELECT *
        FROM comandi'''
    print(query)
    cur.execute(query)
    conn.commit()
    variabile_in_stampa = cur.fetchall()
    print(variabile_in_stampa)

    while True:
        tasto = connection.recv(BUFFER_SIZE).decode()
        print(f"Messaggio ricevuto: {tasto}")

        if variabile_in_stampa:
            cur.execute(query)
            risposta = cur.fetchall()
            print(f"risposta: {risposta}")
            risp = risposta[0]
            print(f"risp: {risp}")
            comando = risp[0]
            print(f"comando: {comando}")
            list_comandi = comando.split(",")
            print(f"lista comandi: {list_comandi}")
            for c in list_comandi:
                movimento = key_comandi[c[0]]
                robot.movimento
                time.sleep(c[1:])
                print(c[0])#lettera
                print(c[1:]) #movimento
            

        #motor1, motor2 = key_comandi[message].split('|')
        #print(motor1, motor2)
        #motor1 = int(motor1)
        #motor2 = int(motor2)
        

        #robot.setMotor(motor1, motor2)     

if __name__ == '__main__':
    main()
