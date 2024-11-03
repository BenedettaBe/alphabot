#Questo codice implementa un server-robot che a cui si connette un client tramite socket 
#riceve comandi di movimento e a ogni comando che riceve attribuisce 
#il valore dei motori per poter svolgere il movimento
from AlphaBot import AlphaBot
import socket
import sqlite3

# indirizzo ip e porta del server
MYADDRESS = ("192.168.1.130", 9090)
BUFFER_SIZE = 4096

# dizionario per associare i comandi di movimento al valore dei motori
key_comandi = {"w": "forward", "s" : "backward", "a" : "left", "d" : "right", "f" : "stop"}

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

    #connessione al database
    conn = sqlite3.connect('mio_database_Benny.db')
    cur = conn.cursor() # serve per far girare il database
    query = '''SELECT *
        FROM comandi'''
    print(query)
    cur.execute(query)
    conn.commit()
    variabile_in_stampa = cur.fetchall()
    print(variabile_in_stampa)
    
    while True:
        message = connection.recv(BUFFER_SIZE).decode()
        print(f"Messaggio ricevuto: {message}")

        if variabile_in_stampa:
            query = f'''SELECT str_mov
            FROM comandi
            WHERE comandi.P_K = "{message}"'''
            print(query) #debug

            cur.execute(query)
            risposta = cur.fetchall()
            risp = risposta[0]
            comando = risp[0]
            print(comando) #debug

            list_comandi = comando.split(",")
            print(list_comandi)

            for c in list_comandi:
                print(c[0])#debug lettera
                if c[0] in key_comandi:
                    print(c[1:])#debug movimento
                else:
                    print("Errore! Il tasto del comando selezionato non esiste")

        # estraggo i valori per i motori dal dizionario key_comandi
        #motor1, motor2 = key_comandi[message].split('|')
        #print(motor1, motor2)
        #motor1 = int(motor1)
        #motor2 = int(motor2)
        # Imposto i motori del robot secondo i comandi ricevuti
        #robot.setMotor(motor1, motor2)     

if __name__ == '__main__':
    main()
