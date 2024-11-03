# alphabot
Questo repository contiene il progetto ALPHABOT dell'anno 2024/2025 del gruppo Baruffolo-Bergia

## server.py

Questo progetto implementa un server in Python che consente il controllo di un robot utilizzando la classe `AlphaBot`. Il server riceve comandi da un client e gestisce i movimenti del robot in base ai comandi ricevuti.

### Funzionalità

Il server è in grado di:
- Ricevere comandi nel formato `{command}|{inputValue}`.
- Eseguire i movimenti del robot per il numero di secondi specificato in `inputValue`.
- Fornire feedback al client riguardo lo stato di esecuzione del comando.

### Comandi Supportati

I seguenti comandi in italiano sono supportati:
- `avanti`: Muove il robot in avanti.
- `indietro`: Muove il robot all'indietro.
- `sinistra`: Gira il robot a sinistra.
- `destra`: Gira il robot a destra.
- `fermo`: Ferma il robot.

### Mappatura dei Comandi

I comandi in italiano sono mappati ai loro equivalenti in inglese e associati ai metodi della classe `AlphaBot`:

```python
diz_command = {
    "forward": "avanti",
    "backward": "indietro",
    "left": "sinistra",
    "right": "destra",
    "stop": "fermo"
}

diz_funz = {
    "forward": robot.forward,
    "backward": robot.backward,
    "left": robot.left,
    "right": robot.right,
    "stop": robot.stop
}