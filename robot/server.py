from AlphaBot import AlphaBot
import socket
import time

MYADDRESS = ("192.168.1.130", 9090)
BUFFER_SIZE = 4096

def main():
    robot = AlphaBot()
    diz_command = {"forward" : "avanti", "backward" : "indietro", "left" : "sinistra", "right": "destra", "stop" : "fermo"} #lista di comandi possibili
    diz_funz = {"forward" : robot.forward, "backward" : robot.backward, "left" : robot.left, "right": robot.right, "stop" : robot.stop} #lista di comandi per il robot
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()

    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")
    while True:
        message = connection.recv(BUFFER_SIZE).decode()
        command, value = message.split('|')
        value = int(value)
        print(command,value)
        if command in diz_command:
            status = "okay"
            phrase = diz_command[command] 
            diz_funz[command]()
            time.sleep(value)
            robot.stop()
            
        else:
            status = "error"  
            phrase = "comando non trovato" 
        answer = f"{status}|{phrase}"
        connection.send(answer.encode())
                   

if __name__ == '__main__':
    main()
