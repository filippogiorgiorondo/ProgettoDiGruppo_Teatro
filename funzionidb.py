import mysql.connector
from mysql.connector import Error

# === CONNESSIONE AL DB ===
def connetti_db():
    try:

        return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="esercito"
    )
        if conn.is_connected():
            print("✅ Connessione al database riuscita.")
            return conn
    except Error as e:
        print(f"❌ Errore di connessione: {e}")
        return None

# === CREA E POPOLA TABELLE ===
def crea_e_popola_tabelle(conn):
    cursor = conn.cursor()

    # Creazione database se non esiste
    cursor.execute("CREATE DATABASE IF NOT EXISTS Teatro")
    cursor.execute("USE Teatro")

    # Creazione tabella PostiPlebe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PostiPlebe (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fila CHAR(1) NOT NULL,
            occupato BOOLEAN DEFAULT FALSE
        )
    """)

    # Popolamento PostiPlebe
    lettere_fila_plebe = ['A', 'B', 'C', 'D']
    for i in range(70):
        fila = lettere_fila_plebe[i // 20] if i < 60 else 'D'
        cursor.execute("INSERT INTO PostiPlebe (fila) VALUES (%s)", (fila,))

    # Creazione tabella PostiVIP
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PostiVIP (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fila CHAR(1) NOT NULL,
            occupato BOOLEAN DEFAULT FALSE,
            accesso_lounge BOOLEAN DEFAULT FALSE,
            servizio_in_posto BOOLEAN DEFAULT FALSE,
            regalo_benvenuto BOOLEAN DEFAULT FALSE
        )
    """)

    # Popolamento PostiVIP con tutti i servizi su FALSE
    for i in range(30):
        fila = 'V' if i < 15 else 'W'
        cursor.execute("""
            INSERT INTO PostiVIP (fila, accesso_lounge, servizio_in_posto, regalo_benvenuto)
            VALUES (%s, %s, %s, %s)
        """, (fila, False, False, False))

    conn.commit()
    print("✅ Tabelle create e popolate con successo.")
    cursor.close()
    
# === FUNZIONE PER PRENDERE I POSTI DISPONIBILI PLEBE ===
def posti_disponibili_plebe(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM PostiPlebe WHERE occupato = FALSE
    """)
    risultato = cursor.fetchone()
    print(f"🎟️ Posti plebe disponibili: {risultato[0]}")
    cursor.close()

# === FUNZIONE PER PRENDERE I POSTI DISPONIBILI VIP ===
def posti_disponibili_vip(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM Postivip WHERE occupato = FALSE
    """)
    risultato = cursor.fetchone()
    print(f"🎟️ Posti plebe disponibili: {risultato[0]}")
    cursor.close()

# === FUNZIONE PER PRENOTARE UN POSTO PLEBE ===
def prenota_posto_plebe(conn, posto_id):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM PostiPlebe
        WHERE id = %s AND occupato = FALSE
    """, (posto_id,))
    posto = cursor.fetchone()

    if posto:
        cursor.execute("UPDATE PostiPlebe SET occupato = TRUE WHERE id = %s", (posto[0],))
        conn.commit()
        print(f"🎟️ Posto plebe prenotato: ID {posto[0]}")
        cursor.close()
        return posto
    else:
        print("❌ Il posto plebe richiesto non è disponibile.")
        cursor.close()
        return None


# === FUNZIONE PER PRENOTARE UN POSTO VIPs
def prenota_posto_vip(conn, posto_id):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM Postivip
        WHERE id = %s AND occupato = FALSE
    """, (posto_id,))
    posto = cursor.fetchone()

    if posto:
        cursor.execute("UPDATE Postivip SET occupato = TRUE WHERE id = %s", (posto[0],))
        conn.commit()
        print(f"🎟️ Posto vip prenotato: ID {posto[0]}")
        cursor.close()
        return posto
    else:
        print("❌ Il posto vip richiesto non è disponibile.")
        cursor.close()
        return None

    
# ===  CANCELLA POSTI PLEBE ===
def cancella_prenotazione_plebe(conn, id_posto):
    cursor = conn.cursor()

    cursor.execute("SELECT occupato FROM PostiPlebe WHERE id = %s", (id_posto,))
    risultato = cursor.fetchone()

    if risultato is None:
        print(f"❌ Nessun posto plebe trovato con ID {id_posto}.")
    elif not risultato[0]:
        print(f"ℹ️ Il posto plebe con ID {id_posto} è già libero.")
    else:
        cursor.execute("""
            UPDATE PostiPlebe
            SET occupato = FALSE
            WHERE id = %s
        """, (id_posto,))
        conn.commit()
        print(f"✅ Prenotazione plebe cancellata per ID {id_posto}.")

    cursor.close()

# === CANCELLA POSTI VIP ===
def cancella_prenotazione_vip(conn, id_posto):
    cursor = conn.cursor()

    cursor.execute("SELECT occupato FROM Postivip WHERE id = %s", (id_posto,))
    risultato = cursor.fetchone()

    if risultato is None:
        print(f"❌ Nessun posto vip trovato con id {id_posto}.")
    elif not risultato[0]:
        print(f"ℹ️ Il posto vipcon ID {id_posto} è già libero.")
    else:
        cursor.execute("""
            UPDATE Postivip
            SET occupato = FALSE
            WHERE id = %s
        """, (id_posto,))
        conn.commit()
        print(f"✅ Prenotazione vipcancellata per ID {id_posto}.")

    cursor.close()

# === VERIFICA SE IL SERVIZIO è PRENOTATO ===
def verifica_servizio_vip(conn, servizio):
    cursor = conn.cursor()

    servizi_validi = ["accesso_lounge", "servizio_in_posto", "regalo_benvenuto"]
    if servizio not in servizi_validi:
        print(f"❌ Servizio non valido. Scegli tra: {', '.join(servizi_validi)}")
        return

    query = f"""
        SELECT 
            COUNT(*) AS totale,
            SUM(CASE WHEN {servizio} = TRUE THEN 1 ELSE 0 END) AS prenotati,
            SUM(CASE WHEN {servizio} = FALSE THEN 1 ELSE 0 END) AS liberi
        FROM PostiVIP
    """

    cursor.execute(query)
    totale, prenotati, liberi = cursor.fetchone()
    print(f"🔍 Stato del servizio '{servizio}':")
    print(f"   Totale posti VIP: {totale}")
    print(f"   ✅ Servizio attivo in: {prenotati}")
    print(f"   🟢 Servizio ancora disponibile in: {liberi}")

    cursor.close()
 
# === PRENOTAZIONE SERVIZIO ===
def prenota_servizio_vip(conn, id_posto, servizio):
    cursor = conn.cursor()

    # Lista dei servizi validi
    servizi_validi = ["accesso_lounge", "servizio_in_posto", "regalo_benvenuto"]
    if servizio not in servizi_validi:
        print(f"❌ Servizio non valido. Scegli tra: {', '.join(servizi_validi)}")
        cursor.close()
        return

    # Query per prenotare il servizio (se non è già prenotato)
    query = f"""
        UPDATE PostiVIP
        SET {servizio} = TRUE, occupato = TRUE
        WHERE id = %s AND {servizio} = FALSE;
    """

    cursor.execute(query, (id_posto,))
    conn.commit()

    if cursor.rowcount > 0:
        print(f"✅ Servizio '{servizio}' prenotato per il posto VIP con ID {id_posto}.")
    else:
        print(f"⚠️ Servizio '{servizio}' già prenotato o il posto non esiste.")

    cursor.close()

conn=  connetti_db()

def menu(conn):
    while True:
        print("\n--- MENU ---")
        print("1. Visualizza posti disponibili plebe")
        print("2. Visualizza posti disponibili VIP")
        print("3. Prenota posto plebe")
        print("4. Prenota posto VIP")
        print("5. Cancella prenotazione posto plebe")
        print("6. Cancella prenotazione posto VIP")
        print("7. Verifica stato di un servizio VIP")
        print("8. Prenota un servizio VIP")
        print("9. Esci")

        scelta = input("Scegli un'opzione: ")

        match scelta:
            case "1":
                posti_disponibili_plebe(conn)

            case "2":
                posti_disponibili_vip(conn)

            case "3":
                prenota_posto_plebe(conn)

            case "4":
                prenota_posto_vip(conn)

            case "5":
                id_posto = int(input("Inserisci l'ID del posto plebe da cancellare: "))
                cancella_prenotazione_plebe(conn, id_posto)

            case "6":
                id_posto = int(input("Inserisci l'ID del posto VIP da cancellare: "))
                cancella_prenotazione_vip(conn, id_posto)

            case "7":
                servizio = input("Inserisci il servizio da verificare (accesso_lounge, servizio_in_posto, regalo_benvenuto): ")
                verifica_servizio_vip(conn, servizio)

            case "8":
                id_posto = int(input("Inserisci l'ID del posto VIP per prenotare il servizio: "))
                servizio = input("Inserisci il servizio da prenotare (accesso_lounge, servizio_in_posto, regalo_benvenuto): ")
                prenota_servizio_vip(conn, id_posto, servizio)

            case "9":
                print("Arrivederci!")
                break

            case _:
                print("❌ Opzione non valida. Riprova.")

