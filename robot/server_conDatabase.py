#INCOMPLETO: manca heart beat
from AlphaBot import AlphaBot
import socket
import sqlite3
import time
from threading import Thread


MYADDRESS = ("192.168.1.130", 9090)
HEART_BEAT_ADDRESS = ("192.168.1.130",9091)
BUFFER_SIZE = 4096

# Dizionario di traduzione per i comandi di movimento
#key_comandi = {"w": "50|50", "s": "-50|-50", "d": "-50|50", "a": "50|-50", "f": "0|0"}
#key_comandi = {"w": "forward", "s" : "backward", "a" : "left", "d" : "right", "f" : "stop"}
key_comandi = {
    "w": (25, 25),     # Avanti
    "s": (-25, -25),   # Indietro
    "a": (25, 0),    # Sinistra
    "d": (0, 25),    # Destra
    "f": (0, 0)        # Stop
}
statoKey = {"w": False, "s": False, "a": False, "d": False, "f": False}
listaPremuti = []

def heartbeat_recive(heartbeat, robot):
    
    #setta un timer di 2 secondi sul socket
    heartbeat.settimeout(2)
    
    #controlla che non ci siano problemi nella connessione
    try:
        while True:
            try:
                
                #riceve il messaggio dal client
                data = heartbeat.recv(BUFFER_SIZE).decode()
                
                #controlla che il messaggio non sia vuoto
                if data == "heartbeat":
                    #print("Heartbeat ricevuto.")
                    pass
                elif not data:
                    print("Heartbeat vuoto, terminazione.")
                    break
                
            #eccezione nel caso in cui il timer di 2 secondi sul socket scade prima che riceva un messaggio
            except socket.timeout:
                print("Timeout del heartbeat. Fermare il robot.")
                robot.stop()	#ferma i motori così si evita che continui ad andare avanti all'infinito
                
            #eccezione nel caso di un errore nella comunicazione
            except Exception as e:
                print(f"Errore nel ricevere heartbeat: {e}")
                break
    finally:
        heartbeat.close()
        print("Connessione heartbeat chiusa.")



def main():
    robot = AlphaBot()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()
    robot.stop()
     #crea il collegamento tramite socket tra pc e alphabot per il controllo della connessione.
    #se la connessione si interrompe e l'alphabot si stava muovendo si blocca e non continua il muovimento
    heartbeat_recived = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    heartbeat_recived.bind(HEART_BEAT_ADDRESS)
    heartbeat_recived.listen(1)
    motor1, motor2 = 0,0
    
    #connessione con il client
    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")
    
    #accetta entrambe le connessioni
    recive_heartbeat, _ = heartbeat_recived.accept() #bloccante

    #connessione al database
    conn = sqlite3.connect('mio_databaseB.db')
    cur = conn.cursor() # serve per far girare il database
    
    #crea il thread per il controllo della connessione tra pc e alphabot tramite la funzione heartbeat_recive
    thread_heartbeat = Thread(target=heartbeat_recive, args=(recive_heartbeat,robot))
    thread_heartbeat.start()

    query = '''SELECT *
        FROM comandi'''
    print(query)
    cur.execute(query)
    conn.commit()
    variabile_in_stampa = cur.fetchall()
    print(variabile_in_stampa)

    while True:
        messaggio = connection.recv(BUFFER_SIZE).decode()
        if not messaggio:
            break
        stato, tasto = messaggio.split('|')
        
        print(f"Messaggio ricevuto: {tasto}")
        if tasto == "":
            break

        elif tasto in statoKey:
            if stato == "P":
                listaPremuti.append(tasto)
            elif stato == "R":
                listaPremuti.remove(tasto)
                
            motor1, motor2 = 0,0
            for t in listaPremuti:
                if t == 'f':
                    motor1 = 0
                    motor2 = 0

                else:
                    '''if tasto == 'w':
                        print("w")
                        robot.forward()
                    elif tasto == 's':
                        print("s")
                        robot.backward()
                    elif tasto == 'a':
                        print("a")
                        robot.left()
                    elif tasto == 'd':
                        print("d")
                        robot.right()
                    elif tasto == 'f':
                        print("f")
                        robot.stop()'''
                    potenzaMovimento = key_comandi[t]
                    motor1 += potenzaMovimento[0]
                    motor2 += potenzaMovimento[1]
                
                motor1 = int(motor1)
                motor2 = int(motor2)
                print(motor1, motor2)
                robot.setMotor(motor1, motor2) 
            

        elif variabile_in_stampa:
            query = f'''SELECT str_mov
                    FROM comandi
                    WHERE P_K = "{tasto}"'''
            print(query)
            cur.execute(query)
            risposta = cur.fetchall()
            print(f"risposta: {risposta}")
            if risposta:
                #risp = risposta[0]
                #print(f"risp: {risp}")
                comando = risposta[0][0]
                print(f"comando: {comando}")
                list_comandi = comando.split(",")
                print(f"lista comandi: {list_comandi}")

                for comando in list_comandi:
                    #print("for")
                    movimento = comando[0]
                    durata = float(comando[1:])
                    if movimento == 'w':
                        robot.forward()
                    elif movimento == 's':
                        robot.backward()
                    elif movimento == 'a':
                        robot.left()
                    elif movimento == 'd':
                        robot.right()
                    time.sleep(durata)
                    robot.stop()

        #motor1, motor2 = key_comandi[message]    

        #motor1, motor2 = key_comandi[message].split('|')
        #print(motor1, motor2)
        #motor1 = int(motor1)
        #motor2 = int(motor2)
        

        #robot.setMotor(motor1, motor2)     

if __name__ == '__main__':
    main()
