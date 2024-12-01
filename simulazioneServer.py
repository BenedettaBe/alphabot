import socket
import sqlite3
import time
from threading import Thread

# Mappatura dei comandi
key_comandi = {
        "w": (25, 25),
        "s": (-25, -25),
        "a": (25, 0),
        "d": (0, 25),
        "f": (0, 0)
    }

# Classe per simulare il comportamento dell'AlphaBot
class AlphaBot:
    def setMotor(self, motor1, motor2):
        print(f"[SIMULAZIONE libreria alphabot] Motori impostati: motor1={motor1}, motor2={motor2}")

    def stop(self):
        print("[SIMULAZIONE] Robot fermato.")

# Configurazioni
MYADDRESS = ("127.0.0.1", 9090)
HEART_BEAT_ADDRESS = ("127.0.0.1", 9091)
BUFFER_SIZE = 4096



def heartbeat_receive(heartbeat, robot):
    heartbeat.settimeout(2)
    try:
        while True:
            try:
                data = heartbeat.recv(BUFFER_SIZE).decode()
                if data == "heartbeat":
                    pass
            except socket.timeout:
                print("[SIMULAZIONE] Timeout heartbeat. Fermare il robot.")
                robot.stop()
                break
    except Exception as e:
        print(f"[ERRORE] Heartbeat: {e}")
    finally:
        heartbeat.close()
        print("[SIMULAZIONE] Connessione heartbeat chiusa.")

'''
def calcoloSetMotor(listaComandi):
    global key_comandi
    motor1, motor2 = 0, 0
    for t in listaComandi:
            if t == 'f':
                motor1 = 0
                motor2 = 0

            elif t in key_comandi:
                potenzaMovimento = key_comandi[t]
                if "s" in listaComandi:
                    motor1 -= potenzaMovimento[0]
                    motor2 -= potenzaMovimento[1]
                else:
                    motor1 += potenzaMovimento[0]
                    motor2 += potenzaMovimento[1]
                motor1 = int(motor1)
                motor2 = int(motor2)

    return motor1, motor2'''


def main():
    global key_comandi
    listaPremuti = []
    motor1, motor2 = 0, 0

    robot = AlphaBot()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()

    robot.stop()

    heartbeat_recived = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    heartbeat_recived.bind(HEART_BEAT_ADDRESS)
    heartbeat_recived.listen(1)

    
    connection, client_address = s.accept()
    print(f"[SIMULAZIONE] Client connesso: {client_address}")
    
    recive_heartbeat, _ = heartbeat_recived.accept()

    conn = sqlite3.connect('mio_databaseB.db')
    cur = conn.cursor() 

    thread_heartbeat = Thread(target=heartbeat_receive, args=(recive_heartbeat, robot))
    thread_heartbeat.start()

    while True:
        print(f"[SIMULAZIONE while]motor1={motor1}, motor2={motor2}")

        messaggio = connection.recv(BUFFER_SIZE).decode()
        if not messaggio:
            break
        stato, tasto = messaggio.split('|')
        
        print(f"[SIMULAZIONE] Messaggio ricevuto: {stato} | {tasto}")

        if stato == "P":
            listaPremuti.append(tasto)
        elif stato == "R" and tasto in listaPremuti:
            listaPremuti.remove(tasto)
                
        motor1, motor2 = 0, 0
        for t in listaPremuti:
            if t == 'f':
                robot.setMotor(0, 0)

            elif t in key_comandi:
                potenzaMovimento = key_comandi[t]
                if 's' in listaPremuti and (t == 'a' or t == 'd'):
                    motor1 -= potenzaMovimento[0]
                    motor2 -= potenzaMovimento[1]
                else:
                    motor1 += potenzaMovimento[0]
                    motor2 += potenzaMovimento[1]
                motor1 = int(motor1)
                motor2 = int(motor2)
                robot.setMotor(motor1, motor2) 


            else:
                query = f'''SELECT str_mov
                        FROM comandi
                        WHERE P_K = "{tasto}"'''
                cur.execute(query)
                result = cur.fetchall()
                if result:
                    comando = result[0][0]
                    print(f"comando: {comando}")
                    list_comandi = comando.split(",")
                    print(f"lista comandi: {list_comandi}")
                    
                    for cmd in comando.split(','):
                        direzione, durata = cmd[0], float(cmd[1:])
                        potenzaMovimento = key_comandi[direzione]
                        motor1 = potenzaMovimento[0]
                        motor2 = potenzaMovimento[1]
                        motor1 = int(motor1)
                        motor2 = int(motor2)
                        print(motor1, motor2)
                        robot.setMotor(motor1, motor2) 
                        time.sleep(durata)
                    robot.stop()

    connection.close()
    recive_heartbeat.close()
    conn.close()
    print("[SIMULAZIONE] Connessioni chiuse.")

if __name__ == '__main__':
    main()
