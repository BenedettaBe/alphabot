import socket
import threading
import sqlite3
from ipaddress import ip_network

PORTE = [20, 22,43,80]
NETWORK = ip_network("192.168.0.0/27")

class Scan(threading.Thread):
    def __init__(self, ip, file):
        super().__init__()
        self.ip = ip
        self.file = file

    def run(self):
        conn = sqlite3.connect('ip_list.db')
        cur = conn.cursor() 
        port = []
        
        try:
            nome_host = socket.gethostbyaddr(self.ip)[0]
        except socket.herror:
            nome_host = ""
        
        for porta in PORTE:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((self.ip, porta)):
                port.append(porta)

        insertQuery = f'''INSERT INTO portScanner("ip_host", "nome_host", "port_list") VALUES
    ("{self.ip}", "{nome_host}", "{port}")'''
        cur.execute(insertQuery)
    

def main():
    conn = sqlite3.connect('ip_list.db')
    cur = conn.cursor() 
    createQuery = '''CREATE TABLE portScanner(
        "ip_host" VARCHAR(15) NOT NULL,
        "nome_host" VARCHAR(20),
        "port_list" VARCHAR(100) NOT NULL);'''


    for ip in NETWORK.hosts():
        thread = Scan(str(ip), 'ip_list.db')
        thread.start()
    
    
    selectQuery = '''SELECT * FROM portScanner'''
    cur.execute(selectQuery)
    risposta = cur.fetchall()
    print(risposta)

if __name__ == "__main__":
    main()