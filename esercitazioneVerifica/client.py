#CLIENT FILE SHARING
#client comunica con il server tramite protocollo TCP.
#questo client richiede informazioni al server che sono presenti all'interno di un database
#POSSIBILI RICHIESTE (messaggio inviato) 'numeroIstruzione|datiNecessari':
#                      '1|nomeFile'
#                      '2|nomeFile'
#                      '3|nomeFile,numFrammento'
#                      '4|nomeFile'

#POSSIBILI RISPOSTE (messaggio ricevuti):
#                      'File presente nel database' o 'File non presente nel database'
#                      'Numero di frammenti: numero intero di frammenti del file'
#                      'Host Frammento: indirizzo IP dell'host del frsammento richiesto'
#                      'HOST: elenco degli indirizzo IP degli host con un frammento del file'
#                      'ERRORE'

import socket

SERVER_ADDRESS = ("127.0.0.1", 9000) #indirizzo e porta server
BUFFER_SIZE = 4096 

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)

    while True:
        #richiedo l'istruzione in input tramite un menù per limitare possibili errori
        print("1. file presente \n2. numero di frammenti di un file \n3. IP dell'host di un frammento \n4. tutti IP degli host con frammenti di un file \n5. fine\n")
        istruzione = input(f"INSERIRE ISTRUZIONE: ")
        if istruzione == '1' or istruzione == '2' or istruzione == '3' or istruzione == '4':
            valore = input(f"INSERIRE NOME FILE: ")
            #l'istruzione 3 richiede un dato in più che viene richiesto all'utente
            if istruzione == '3': 
                valore += ','+ input(f"INSERIRE NUMERO FRAMMENTO: ")
            message = f"{istruzione}|{valore}"
            s.sendall(message.encode())
            message = s.recv(BUFFER_SIZE)
            print(f"{message.decode()}\n")
        else:
            #se l'istruzione non viene riconosciuta o equivale alla fine della richiesta il socket viene chiuso
            s.sendall("".encode())
            s.close()
            break

if __name__ == "__main__":
    main()