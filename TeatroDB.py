import mysql.connector
from mysql.connector import Error

# === CONNESSIONE AL DATABASE ===
def connetti_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Teatro"
        )
        if conn.is_connected():
            print("✅ Connessione al database riuscita.")
            return conn
    except Error as e:
        print(f"❌ Errore di connessione al database: {e}")
    return None


# === CREAZIONE E POPOLAMENTO DELLE TABELLE ===
def crea_e_popola_tabelle(conn):
    cursor = conn.cursor()

    # Creazione database se non esiste
    cursor.execute("CREATE DATABASE IF NOT EXISTS Teatro")
    cursor.execute("USE Teatro")

    # Tabella PostiPlebe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PostiPlebe (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fila CHAR(1) NOT NULL,
            occupato BOOLEAN DEFAULT FALSE,
            nome_prenotazione VARCHAR(255) DEFAULT NULL,
            importo FLOAT DEFAULT NULL
        )
    """)

    lettere_fila_plebe = ['M', 'B']
    for i in range(20):
        fila = lettere_fila_plebe[i // 10]
        cursor.execute("INSERT INTO PostiPlebe (fila) VALUES (%s)", (fila,))

    # Tabella PostiVIP
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PostiVIP (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fila CHAR(1) NOT NULL,
            occupato BOOLEAN DEFAULT FALSE,
            accesso_lounge BOOLEAN DEFAULT FALSE,
            servizio_in_posto BOOLEAN DEFAULT FALSE,
            regalo_benvenuto BOOLEAN DEFAULT FALSE,
            nome_prenotazione VARCHAR(255) DEFAULT NULL,
            importo FLOAT DEFAULT NULL
        )
    """)

    for _ in range(10):
        cursor.execute("""
            INSERT INTO PostiVIP (fila, accesso_lounge, servizio_in_posto, regalo_benvenuto)
            VALUES (%s, %s, %s, %s)
        """, ('V', False, False, False))

    conn.commit()
    cursor.close()
    print("✅ Tabelle create e popolate con successo.")


# === POSTI DISPONIBILI ===
def posti_disponibili_plebe(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM PostiPlebe WHERE occupato = FALSE")
    risultato = cursor.fetchone()
    cursor.close()
    print(f"🎟️ Posti plebe disponibili: {risultato[0]}")

def posti_disponibili_vip(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM PostiVIP WHERE occupato = FALSE")
    risultato = cursor.fetchone()
    cursor.close()
    print(f"🎟️ Posti VIP disponibili: {risultato[0]}")


# === PRENOTAZIONI ===
def prenota_posto_plebe(conn, posto_id, nome_prenotazione):
    try:
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT id, occupato, fila FROM PostiPlebe 
            WHERE id = %s AND occupato = FALSE
        """, (posto_id,))
        posto = cursor.fetchone()

        if posto:
            fila = posto[2]
            importo = 20.0 if fila == "M" else 10.0
            cursor.execute(""" 
                UPDATE PostiPlebe 
                SET occupato = TRUE, nome_prenotazione = %s, importo = %s
                WHERE id = %s
            """, (nome_prenotazione, importo, posto_id))
            conn.commit()
            print(f"🎟️ Posto plebe prenotato: Fila {fila}, ID {posto_id}, a nome di {nome_prenotazione}")
            cursor.close()
            return True
        else:
            print("❌ Il posto plebe richiesto non è disponibile.")
            cursor.close()
            return None
    except mysql.connector.Error as e:
        print(f"⚠️ Errore durante la prenotazione del posto plebe: {e}")
        cursor.close()
        return None

def prenota_posto_vip(conn, posto_id, nome_prenotazione, importo=50):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM PostiVIP
            WHERE id = %s AND occupato = FALSE
        """, (posto_id,))
        posto = cursor.fetchone()

        if posto:
            cursor.execute("""
                UPDATE PostiVIP
                SET occupato = TRUE, nome_prenotazione = %s, importo = %s
                WHERE id = %s
            """, (nome_prenotazione, importo, posto_id))
            conn.commit()
            print(f"🎟️ Posto VIP prenotato: ID {posto[0]} a nome di {nome_prenotazione} con importo €{importo}")
            cursor.close()
            return True
        else:
            print("❌ Il posto VIP richiesto non è disponibile.")
            cursor.close()
            return False
    except Exception as e:
        print(f"⚠️ Errore durante la prenotazione del posto VIP: {e}")
        return False


# === CANCELLAZIONI ===
def cancella_prenotazione_plebe(conn, id_posto, nome_prenotazione):
    cursor = conn.cursor()
    cursor.execute("SELECT occupato, nome_prenotazione, importo FROM PostiPlebe WHERE id = %s", (id_posto,))
    risultato = cursor.fetchone()

    if risultato is None:
        print(f"❌ Nessun posto plebe trovato con ID {id_posto}.")
    elif not risultato[0]:
        print(f"ℹ️ Il posto plebe con ID {id_posto} è già libero.")
    elif risultato[1] != nome_prenotazione:
        print("❌ Il nome fornito non corrisponde alla prenotazione.")
    else:
        importo = risultato[2]
        cursor.execute("""
            UPDATE PostiPlebe
            SET occupato = FALSE, nome_prenotazione = NULL, importo = NULL
            WHERE id = %s
        """, (id_posto,))
        conn.commit()
        print(f"✅ Prenotazione plebe cancellata per ID {id_posto}. Importo restituito: €{importo} a {nome_prenotazione}")
        cursor.close()
        return True
    cursor.close()
    return False

def cancella_prenotazione_vip(conn, id_posto, nome_prenotazione):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT occupato FROM PostiVIP 
            WHERE id = %s AND nome_prenotazione = %s
        """, (id_posto, nome_prenotazione))
        risultato = cursor.fetchone()

        if risultato is None:
            print(f"❌ Nessun posto VIP trovato con ID {id_posto} per il nome '{nome_prenotazione}'.")
            return False
        elif not risultato[0]:
            print(f"ℹ️ Il posto VIP con ID {id_posto} è già libero.")
            return False
        else:
            cursor.execute("""
                UPDATE PostiVIP
                SET occupato = FALSE, nome_prenotazione = NULL,
                    accesso_lounge = FALSE,
                    servizio_in_posto = FALSE,
                    regalo_benvenuto = FALSE
                WHERE id = %s
            """, (id_posto,))
            conn.commit()
            print(f"✅ Prenotazione VIP cancellata per ID {id_posto} e nome '{nome_prenotazione}'.")
            return True
    except Exception as e:
        print(f"⚠️ Errore durante la cancellazione della prenotazione VIP: {e}")
        return False
    finally:
        cursor.close()


# === SERVIZI VIP ===
def verifica_servizio_vip(conn, servizio):
    cursor = conn.cursor()
    servizi_validi = ["accesso_lounge", "servizio_in_posto", "regalo_benvenuto"]

    if servizio not in servizi_validi:
        print(f"❌ Servizio non valido. Scegli tra: {', '.join(servizi_validi)}")
        return False

    query = f"""
        SELECT COUNT(*) AS totale, 
               SUM(CASE WHEN {servizio} = TRUE THEN 1 ELSE 0 END) AS prenotati,
               SUM(CASE WHEN {servizio} = FALSE THEN 1 ELSE 0 END) AS liberi 
        FROM PostiVIP
    """
    cursor.execute(query)
    _, _, liberi = cursor.fetchone()
    cursor.close()
    return liberi > 0

def prenota_servizio_vip(conn, id_posto, servizio, importo=None):
    cursor = conn.cursor()
    if importo is None:
        importo = ottieni_importo(conn, id_posto) or 50.0
        importo += 20.0

    query = f"""
        UPDATE PostiVIP
        SET {servizio} = TRUE, occupato = TRUE, importo = %s
        WHERE id = %s AND {servizio} = FALSE;
    """
    cursor.execute(query, (importo, id_posto))
    conn.commit()

    if cursor.rowcount > 0:
        print(f"✅ Servizio '{servizio}' prenotato per il posto VIP con ID {id_posto}. Importo: €{importo}")
    else:
        print(f"⚠️ Servizio '{servizio}' già prenotato o il posto non esiste.")

    cursor.close()

def disattiva_servizio_vip(conn, id_posto, servizio):
    cursor = conn.cursor()
    servizi_validi = ["accesso_lounge", "servizio_in_posto", "regalo_benvenuto"]

    if servizio not in servizi_validi:
        print(f"❌ Servizio non valido. Scegli tra: {', '.join(servizi_validi)}")
        return False

    query = f"""
        UPDATE PostiVIP 
        SET {servizio} = FALSE 
        WHERE id = %s
    """
    try:
        cursor.execute(query, (id_posto,))
        conn.commit()
        print(f"✅ Servizio '{servizio}' disattivato per il posto VIP #{id_posto}.")
        return True
    except Exception as e:
        conn.rollback()
        print(f"❌ Errore durante la disattivazione del servizio: {e}")
        return False
    finally:
        cursor.close()


def ottieni_importo(conn, id_posto):
    cursor = conn.cursor()
    query = "SELECT importo FROM PostiVIP WHERE id = %s"
    try:
        cursor.execute(query, (id_posto,))
        result = cursor.fetchone()
        if result:
            print(f"✅ Importo trovato per il posto VIP #{id_posto}: ${result[0]:.2f}")
            return result[0]
        else:
            print(f"❌ Nessun posto VIP trovato con ID #{id_posto}")
            return None
    except Exception as e:
        print(f"❌ Errore durante la ricerca dell'importo: {e}")
        return None
    finally:
        cursor.close()


# === FUNZIONI EXTRA ===
def get_posto_vicino(conn, posto_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, nome_prenotazione FROM PostiVIP 
        WHERE (id = %s - 1 OR id = %s + 1) AND occupato = TRUE
    """, (posto_id, posto_id))
    vicini = cursor.fetchall()
    cursor.close()
    return vicini

def has_servizio_in_posto(conn, posto_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT servizio_in_posto FROM PostiVIP 
        WHERE id = %s AND occupato = TRUE
    """, (posto_id,))
    risultato = cursor.fetchone()
    cursor.close()
    return risultato and risultato[0] == 1
