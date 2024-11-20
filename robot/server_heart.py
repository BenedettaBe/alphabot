from AlphaBot import AlphaBot
import socket
from threading import Thread
import time

MYADDRESS = ("192.168.1.130", 9090)
HEARTBEAT_ADDRESS = ("192.168.1.130", 9091)

BUFFER_SIZE = 4096

key_comandi = {"w": "forward", "s" : "backward", "a" : "left", "d" : "right", "f" : "stop"}


def heartbeat_reciver(heartbeat, robot):
    heartbeat.settimeout(2)
    try:
        while True:
            try:

                data = heartbeat.recv(BUFFER_SIZE).decode()
                print(data)

            except socket.timeout:
                print("FERMA TUTTO")
                robot.stop()
            except Exception as e:
                print(f"Errore {e}")
    finally:
        heartbeat.close()

def main():
    robot = AlphaBot()
    diz_command = {"forward" : "avanti", "backward" : "indietro", "left" : "sinistra", "right": "destra", "stop" : "fermo"} #lista di comandi possibili
    diz_funz = {"forward" : robot.forward, "backward" : robot.backward, "left" : robot.left, "right": robot.right, "stop" : robot.stop} #lista di comandi per il robot
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen(1)
    robot.stop()

    rec_heartbeat= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rec_heartbeat.bind(HEARTBEAT_ADDRESS)
    rec_heartbeat.listen(1)

    rec_connection, rec_address = rec_heartbeat.accept()

    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")

    rec_heartbeat = Thread(target=heartbeat_reciver, arg=(rec_connection, robot))
    rec_heartbeat.start()
    while True:
        message = connection.recv(BUFFER_SIZE).decode()
        tasto = message
        if tasto in key_comandi:
            print("c")
            if tasto == 'w':
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
                robot.stop()
            time.sleep(0.25)
           

if __name__ == '__main__':
    main()
