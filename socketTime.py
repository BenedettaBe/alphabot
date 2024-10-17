socket_heartbeat.settimeout(6.5)

while True:
    try:
        data.socket_heartbeat.recv(BUFFER)
    except socket.timeout: 
        print("FERMA TUTTO")
        break