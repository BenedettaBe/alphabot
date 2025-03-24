import requests

def richiesta():
    try:
        nome = input("Inserisci nome: ")
        cognome = input("Inserisci cognome: ")
        
        # Input validation for age
        while True:
            try:
                eta = int(input("Inserisci eta: "))
                if eta <= 0:
                    print("L'età deve essere un numero positivo.")
                    continue
                break
            except ValueError:
                print("Per favore, inserisci un numero valido per l'età.")
        
        url = "http://127.0.0.1:5000/studenti"  # Endpoint dell'API
        dati_studente = {
            "nome": nome,
            "cognome": cognome,
            "eta": eta
        }

        # Invia la richiesta POST con i dati JSON
        response = requests.post(url, json=dati_studente)

        # Verifica la risposta del server
        if response.status_code == 201:
            print("Studente aggiunto con successo!")
            print(response.json())  # Mostra il messaggio di conferma e i dettagli dello studente
        else:
            print(f"Errore: {response.status_code}")
            print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta HTTP: {e}")

if __name__ == "__main__":
    richiesta()
