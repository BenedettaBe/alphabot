from AlphaBot import AlphaBot
import socket
import time

MYADDRESS = ("192.168.1.130", 9090)
BUFFER_SIZE = 4096

def main():
    robot = AlphaBot()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MYADDRESS)
    s.listen()
    motor1 = 0
    motor2 = 0

    robot.setMotor(motor1, motor2)
    connection, client_address = s.accept()
    print(f"Il client {client_address} si è connesso")
    while True:
        message = connection.recv(BUFFER_SIZE).decode()
        print(message)
        motor1, motor2 = message.split('|')
        print(motor1, motor2)
        motor1 = int(motor1)
        motor2 = int(motor2)
        

        robot.setMotor(motor1, motor2)
        '''
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
             '''      

if __name__ == '__main__':
    main()
