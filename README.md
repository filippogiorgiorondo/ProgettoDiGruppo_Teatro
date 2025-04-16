# 🎭 Sistema Prenotazione Teatro
*Un’esperienza teatrale a portata di CLI*

Benvenuto nel Sistema di Prenotazione Teatro, una piattaforma Python con MySQL progettata per offrire una gestione moderna, efficiente e interattiva dei posti a teatro.
Grazie a un menu guidato e semplice da usare, il sistema consente agli utenti di prenotare, cancellare o arricchire l’esperienza dei posti VIP con servizi esclusivi.

Questo progetto è pensato per simulare in tempo reale la gestione di un teatro tramite interfaccia testuale. È sviluppato in Python 3.x e utilizza un database relazionale MySQL per la gestione persistente dei dati.

## 🧩 Funzionalità in evidenza
### 🎟 Prenotazione interattiva via menu CLI
- ✅ Scelta tra posti Plebe e VIP
- ✅ Conferma automatica della disponibilità
- ✅ Messaggi visivi, simboli emoji e flusso guidato
- ✅ Inserimento dati dell'utente, conferme, feedback in tempo reale
  
### 🧠 Intelligenza “di sala”
- 👀 Verifica dei posti adiacenti: scopri chi è seduto accanto a te e chiacchieraci, proprio come in teatro! — Funzione utilissima per sapere con chi stai condividendo lo spettacolo.

- 🍾 Servizi attivabili durante lo spettacolo: puoi aggiungere accesso lounge, servizio in posto o regali in qualunque momento — proprio come un upgrade in tempo reale.

## 📂 Struttura del progetto
├── Teatro.py                
├── TeatroDB.py    
- In Teatro.py è presente il programma che viene eseguito
- TeatroDB.py è un modulo che viene importato, all'interno del quale sono inserite tutte le funzioni per gestire e manipolare il DB

## 🔧 Tecnologie e Librerie
- Python 3.x:	Linguaggio principale
- MySQL:	Database relazionale per la gestione dei posti
- XAMPP:	Server locale per il DB MySQL
- mysql-connector-python:	Libreria per la connessione tra Python e MySQL
- time:	Per gestire temporizzazioni e simulazioni
- Programmazione ad oggetti (OOP)	
