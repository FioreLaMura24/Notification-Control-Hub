NOTIFICATION CONTROL HUB by 
Gli inimitabili (La Mura, Graziuso, Cafiero, Di Maio)

REQUISITI
- PYTHON 3.13.2
- PYGAME (pip install pygame)

COME AVVIARE IL PROGRAMMA
Avviare il file main.py con Python
Aprire un terminale nella cartella dove si trova il file ed eseguire il comando
"python main.py" per avviare il programma

DESCRIZIONE DEL PROGRAMMA

"Notification Control Hub" è un simulatore interattivo sviluppato in Python con Pygame, progettato per allenare riflessi, memoria e capacità di gestione delle emergenze in un contesto militare simulato.
Il programma genera notifiche in tempo reale che rappresentano guasti, attacchi o malfunzionamenti dei sistemi militari. 
L’utente deve risolvere ogni emergenza cliccando sul pulsante “Ripara”, che apre un mini-gioco specifico assegnato al problema.

Funzionalità principali:
Generazione dinamica delle notifiche
Messaggi casuali che descrivono guasti o emergenze.
Ogni notifica ha un ID unico, timestamp, messaggio e tipo di mini-gioco associato.
Le notifiche vecchie vengono rimosse automaticamente, mentre quella attiva rimane fino a completamento.

Mini-giochi integrati:
Click Target: colpisci il bersaglio rosso 3 volte nel minor tempo possibile.
Simon Digitale: memorizza e digita una sequenza numerica crescente in lunghezza in base al punteggio.

Difficoltà scalabile: Simon aumenta la sequenza ogni 500 punti, garantendo progressione e sfida crescente.
Gestione dello stato e salvataggio

Tempo e punteggio persistono tra le sessioni tramite file JSON (repairs_log.json).

Registro dettagliato delle riparazioni completate: ID notifica, tipo di mini-gioco, tempo impiegato, punteggio guadagnato, data e ora della riparazione.

Interfaccia
Colori e layout coerenti con un contesto militare (verde scuro, rosso alert, grigio tattico).
Pulsanti e informazioni chiaramente leggibili, feedback immediato per le azioni dell’utente.
Popup dei mini-giochi chiaro e centrale.

Protezione da crash durante l’interazione con notifiche attive.
Pulsante RESET per azzerare completamente tempo, punteggio e dati salvati.
Il programma carica i dati precedenti da un file esterno (save.json) per maggiore scalabilità.

Obiettivo del programma
Il gioco è progettato per combinare simulazione realistica, interattività e progressione scalabile, offrendo un ambiente di allenamento virtuale dove il giocatore deve reagire rapidamente, gestire risorse temporali e prendere decisioni efficaci sotto pressione.

Fatto da:
Graziuso Giuseppe;
La Mura Fiore;
Di Maio Luigi;
Cafiero Liberato.

