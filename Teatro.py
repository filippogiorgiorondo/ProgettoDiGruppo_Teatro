import funzionidb as db
import time
conn = db.connetti_db()
db.crea_e_popola_tabelle(conn)
# ======================= PIANTINA TEATRO ============================================
def piantina():
    # Dimensioni della sala
    ROWS = 3       # Numero di file (B, M, V)
    COLS = 10      # Numero di posti per fila

    # Funzione per generare il countdown in sequenza
    def countdown(start, length):
        return [str(start - i) for i in range(length)]

    def mostra_piantina_teatro():
        cell_w = 10  # larghezza cella
        cell_h = 3   # altezza cella

        border = "+" + ("-" * cell_w + "+") * COLS

        print("\n🎭 Piantina dei posti del teatro 🎭\n")
        
        # Countdown per le righe
        countdown_bm = countdown(20, COLS)  # Countdown per la riga B e M
        countdown_v = countdown(10, COLS)  # Countdown per la riga V
        
        # Mappa dei posti con le lettere di riga (B, M, V)
        main_map = [
            ['B'] * COLS,  # Prima riga (B)
            ['M'] * COLS,  # Seconda riga (M)
            ['V'] * COLS,  # Terza riga (V)
        ]
        
        # Inizializziamo un indice per il countdown
        current_count = 20

        for i, row in enumerate(main_map):
            print(border)
            for line in range(cell_h):
                row_str = ""  # Inizializzo la stringa per la riga
                for j in range(COLS):
                    if i == 0:  # Per la riga B
                        if line == 1:
                            content = f" {row[j]} {current_count} ".center(cell_w)  # Aggiungi lettera e numero
                            current_count -= 1
                        else:
                            content = " " * cell_w
                    elif i == 1:  # Per la riga M (continua da 19 a 10)
                        if line == 1:
                            content = f" {row[j]} {current_count} ".center(cell_w)  # Aggiungi lettera e numero
                            current_count -= 1
                        else:
                            content = " " * cell_w
                    elif i == 2:  # Per la riga V (con countdown da 10)
                        if line == 1:
                            current_count = 10  # Resetta il countdown a 10 per la riga V
                            content = f" {row[j]} {current_count} ".center(cell_w)  # Aggiungi lettera e numero
                            current_count -= 1
                        else:
                            content = " " * cell_w
                    row_str += f"|{content}"
                row_str += "|"
                print(row_str)
        print(border)
    mostra_piantina_teatro()
    print("\n===============================================Il palco è qui===============================================\n")

# ===================================== CLASSE GENITORE ============================================
class Posto:
    def __init__(self, numero, fila, nome_prenotazione, occupato=False):
        self._numero = numero
        self._fila = fila
        self._occupato = occupato
        self.nome_prenotazione = nome_prenotazione

    def get_numero(self):
        return self._numero

    def set_numero(self, numero):
        self._numero = numero

    def get_fila(self):
        return self._fila

    def set_fila(self, fila):
        self._fila = fila

    def get_occupato(self):
        return self._occupato

    def set_occupato(self, occupato):
        if isinstance(occupato, bool):
            self._occupato = occupato
        else:
            print("Valore non valido per occupato. Deve essere True o False.")

    def prenota(self):
        if not self.get_occupato():
            self.set_occupato(True) 
            print("Posto prenotato")
            # nelle specializzazioni è presente la query per settare la prenotazione del posto
        else:
            print("Posto già prenotato")

    def libera(self):
        if self.get_occupato():
            self.set_occupato(False) 
            print("Posto liberato")
            # nelle specializzazioni è presente la query per settare la liberazione di un posto
        else:
            print("Il posto era già libero")

# ===================================== CLASSE POSTO VIP ===========================================
class PostoVip(Posto):
    # Costruttore: eredita gli attributi dalla superclasse Posto e inizializza i servizi VIP
    def __init__(self, numero, fila, nome_prenotazione, occupato=False):
        super().__init__(numero, fila, nome_prenotazione, occupato)
        self.servizi = ["accesso_lounge", "servizio_in_posto", "regalo_benvenuto"]

    # Metodo per prenotare un posto VIP e aggiungere eventuali servizi extra
    def prenota(self, id):
        self._occupato = True  # Segna il posto come occupato
        importo = 50.0  # Prezzo base per il posto VIP

        scelta = input("✨ Vuoi aggiungere servizi extra per 20$ ciascuno? (s/n): ").lower().strip()
        if scelta == "s":
            print("\n📋 --- Menu Servizi VIP ---")
            for i, servizio in enumerate(self.servizi, start=1):
                print(f"{i}. {servizio}")

            while True:
                try:
                    ch = int(input("👉 Inserisci il numero del servizio da aggiungere: "))

                    match ch:
                        case 1:
                            nome_servizio = self.servizi[0]
                        case 2:
                            nome_servizio = self.servizi[1]
                        case 3:
                            nome_servizio = self.servizi[2]
                        case _:
                            print("❌ Selezione non valida. Riprova.")
                            continue

                    # Verifica disponibilità del servizio prima di prenotarlo
                    disponibile = db.verifica_servizio_vip(conn, nome_servizio)
                    if disponibile:
                        importo += 20  # Aggiunge il costo del servizio all'importo totale
                        db.prenota_servizio_vip(conn, self.get_numero(), nome_servizio, importo)
                        print(f"✅ Servizio aggiunto: '{nome_servizio}'")
                    else:
                        print(f"⚠️ Il servizio '{nome_servizio}' non è disponibile al momento.")

                except ValueError:
                    print("⚠️ Inserisci un numero valido.")

                continua = input("➕ Vuoi aggiungere un altro servizio? (s/n): ").lower().strip()
                if continua != "s":
                    break

        # Mostra il totale al termine della prenotazione
        print(f"\n🎟️ Prenotazione completata. Totale da pagare: 💵 {importo:.2f}$")


# ===================================== CLASSE POSTO PLEBE =========================================
class PostoPlebe(Posto):
    # Costruttore: eredita gli attributi dalla classe madre Posto
    def __init__(self, numero, fila, nome_prenotazione, occupato=False):
        super().__init__(numero, fila, nome_prenotazione, occupato)

    # Metodo per prenotare un posto plebe
    def prenota(self, posto):
        try:
            if posto:
                costo = self.calcola_costo()  # Calcola il costo del posto in base alla posizione
                print(f"✅ Posto plebe prenotato con successo! Prezzo: 💰 {costo}$")
                self.set_occupato(True)  # Segna il posto come occupato
            else:
                print("❌ Il posto risulta già prenotato.")
        except Exception as e:
            print(f"⚠️ Errore durante la prenotazione del posto plebe: {e}")

    # Metodo per calcolare il costo del posto in base alla numerazione
    def calcola_costo(self):
        numero = self.get_numero()  # Ottiene il numero del posto
        if 1 <= numero <= 10:
            return 20.0  # Prezzo per i posti in fila M (centrali)
        elif 11 <= numero <= 20:
            return 10.0  # Prezzo ridotto per i posti in fila B (ultimi)
        else:
            print("❌ Numero posto non valido (deve essere tra 1 e 20).")
            return 0.0  # Ritorna 0 in caso di numero fuori range

    
# ======================================================= CLASSE TEATRO =================================================================
class Teatro:
    def __init__(self):
        # Dizionario privato per tenere traccia degli oggetti Posto associati agli ID
        self.__lista = {}
        
    def setter_aggiungi(self, id_posto, posto_obj):
        # Aggiunge un oggetto Posto alla lista in base all'ID
        self.__lista[id_posto] = type(posto_obj)
        
    def setter_togli(self, id_posto):
        # Rimuove un oggetto Posto dalla lista in base all'ID
        del self.__lista[id_posto]
        
    def getter_lista(self):
        # Stampa la lista attuale delle prenotazioni, se presente
        if self.__lista != {}:
            print("\n📋 Lista prenotazioni attuali:")
            for chiave, valore in self.__lista.items():
                print(f"🪑 Posto ID {chiave}: tipo {valore.__name__}")
        else:
            print("\n📭 Nessuna prenotazione attiva al momento.")

    def menu(self):
        # Menu interattivo per la gestione del teatro
        while True:
            print("\n🎭 MENU TEATRO")
            print("1️⃣  Visualizza posti plebe disponibili")
            print("2️⃣  Visualizza posti VIP disponibili")
            print("3️⃣  Prenota posto plebe")
            print("4️⃣  Prenota posto VIP")
            print("5️⃣  Cancella prenotazione plebe")
            print("6️⃣  Cancella prenotazione VIP")
            print("7️⃣  Verifica stato servizio VIP")
            print("8️⃣  Prenota servizio VIP")
            print("9️⃣  Rimuovi servizio VIP")
            print("🔟  Esci")

            scelta = input("👉 Seleziona un'opzione (1-10): ")
            
            match scelta:
                case "1":
                    # Visualizza i posti plebe disponibili
                    db.posti_disponibili_plebe(conn)

                case "2":
                    # Visualizza i posti VIP disponibili
                    db.posti_disponibili_vip(conn)

                case "3":
                    # Prenotazione posto plebe
                    try:
                        id_posto = int(input("🎫 Inserisci ID posto plebe da prenotare (1-20): "))
                        if 1 <= id_posto <= 10:
                            fila = "M"
                        elif 11 <= id_posto <= 20:
                            fila = "B"
                        else:
                            print("❌ Posto non disponibile.")
                            continue

                        nome_prenotazione = input("✍️ Nome per la prenotazione: ")
                        if not nome_prenotazione or not nome_prenotazione.isalpha():
                            print("❌ Inserisci un nome valido (solo lettere).")
                            continue

                        posto = db.prenota_posto_plebe(conn, id_posto, nome_prenotazione)
                        if posto:
                            posto_obj = PostoPlebe(id_posto, fila, nome_prenotazione)
                            self.setter_aggiungi(id_posto, posto_obj)
                            self.getter_lista()
                            posto_obj.prenota(posto)

                    except ValueError:
                        print("❌ Inserisci un numero valido.")

                case "4":
                    # Prenotazione posto VIP
                    try:
                        id_posto = int(input("🎫 Inserisci ID posto VIP da prenotare (1-10): "))
                        if 1 <= id_posto <= 10:
                            fila = "V"
                        else:
                            print("❌ Posto VIP non disponibile.")
                            continue

                        nome_prenotazione = input("✍️ Nome per la prenotazione: ")
                        if not nome_prenotazione or not nome_prenotazione.isalpha():
                            print("❌ Inserisci un nome valido (solo lettere).")
                            continue

                        posto = db.prenota_posto_vip(conn, id_posto, nome_prenotazione)
                        if posto:
                            posto_obj = PostoVip(id_posto, fila, nome_prenotazione)
                            self.setter_aggiungi(id_posto, posto_obj)
                            self.getter_lista()
                            posto_obj.prenota(id_posto)

                    except ValueError:
                        print("❌ Inserisci un numero valido.")

                case "5":
                    # Cancellazione prenotazione plebe
                    try:
                        id_posto = int(input("🗑️ Inserisci ID del posto plebe da cancellare: "))
                        nome = input("✍️ Nome della prenotazione: ")
                        successo = db.cancella_prenotazione_plebe(conn, id_posto, nome)
                        if successo:
                            try:
                                self.setter_togli(id_posto)
                                self.getter_lista()
                            except KeyError:
                                print("ℹ️ Il posto non era nella lista corrente.")
                    except ValueError:
                        print("❌ Inserisci un numero valido.")

                case "6":
                    # Cancellazione prenotazione VIP
                    try:
                        id_posto = int(input("🗑️ Inserisci ID del posto VIP da cancellare: "))
                        nome = input("✍️ Nome della prenotazione: ")
                        successo = db.cancella_prenotazione_vip(conn, id_posto, nome)
                        if successo:
                            try:
                                self.setter_togli(id_posto)
                                self.getter_lista()
                            except KeyError:
                                print("ℹ️ Il posto non era nella lista corrente.")
                    except ValueError:
                        print("❌ Inserisci un numero valido.")

                case "7":
                    # Verifica disponibilità di un servizio VIP
                    try:
                        servizio = input("🔍 Servizio da verificare (accesso_lounge, servizio_in_posto, regalo_benvenuto): ").strip()
                        disponibile = db.verifica_servizio_vip(conn, servizio)
                        if disponibile:
                            print("✅ Servizio disponibile!")
                        else:
                            print("⚠️ Servizio non disponibile o inesistente.")
                    except Exception as e:
                        print(f"⚠️ Errore: {e}")

                case "8":
                    # Prenota un servizio VIP
                    try:
                        id_posto = int(input("🎫 Inserisci ID posto VIP: "))
                        servizio = input("🧾 Servizio da prenotare: ").strip()
                        importo = db.ottieni_importo(conn, id_posto)
                        if importo is not None:
                            importo += 20  # Aggiunta costo servizio
                            db.prenota_servizio_vip(conn, id_posto, servizio, importo)
                            print("✅ Servizio aggiunto con successo.")
                        else:
                            print("❌ Impossibile prenotare il servizio.")
                    except ValueError:
                        print("❌ Inserisci un numero valido.")

                case "9":
                    # Rimuove un servizio VIP
                    try:
                        id_posto = int(input("🗑️ Inserisci ID posto VIP: "))
                        servizio = input("✂️ Servizio da rimuovere: ").strip()
                        db.disattiva_servizio_vip(conn, id_posto, servizio)
                        print("✅ Servizio rimosso correttamente.")
                    except ValueError:
                        print("❌ Inserisci un numero valido.")

                case "10":
                    # Uscita dal menu
                    print("👋 Arrivederci e grazie per aver gestito il Teatro con noi!")
                    return
                    
                case _:
                    # Scelta non valida
                    print("❌ Scelta non riconosciuta. Riprova.")


# ===================================================== INIZIALIZZO IL GESTORE TEATRO ==============================================================
teatro = Teatro()
piantina()
teatro.menu()

# =================================================== CLASSE SPETTACOLO TEATRALE ===================================================================
class Spettacolo:
    
    # Inizializza lo spettacolo con titolo, durata e connessione al DB
    def __init__(self, titolo, durata_minuti, conn):
        self.titolo = titolo
        self.durata_minuti = durata_minuti
        self.conn = conn
        print(f"\n🎭 Benvenuto a '{self.titolo}'! Durata: {self.durata_minuti} minuti.\n")

    # Ottiene e stampa le info del vicino di posto
    def chiacchiera_con_vicino(self, id_posto):
        vicini = db.get_posto_vicino(self.conn, id_posto)
        if vicini:
            for vicino in vicini:
                print(f"🗣️ Vicino al posto #{vicino['id']}: «{vicino['nome_prenotazione']}». Due chiacchiere volano via!")
        else:
            print("🤐 Nessun vicino accanto a te. Silenzio e concentrazione...")

    # Controlla se è disponibile il servizio in posto
    def usufruisci_servizio_in_posto(self, id_posto):
        if db.has_servizio_in_posto(self.conn, id_posto):
            print("🍷 Il cameriere arriva silenziosamente... ecco uno snack raffinato e una bevanda fresca!")
        else:
            print("🚫 Ops! Il servizio in posto non è disponibile per questo biglietto.")

    # Simula lo spettacolo e le interazioni con l'utente
    def simula_spettacolo(self, id_posto):
        print(f"\n🎬 Preparati... lo spettacolo '{self.titolo}' sta per iniziare!")
        momenti = {
            0: "✨ Le luci si abbassano... silenzio in sala.",
            30: "🛑 Intervallo! Un momento perfetto per socializzare.",
            60: "🍿 Snack time! Il servizio in posto prende vita.",
            self.durata_minuti: "🎉 Applausi! Lo spettacolo è giunto al termine."
        }

        for minuto in range(0, self.durata_minuti + 1, 30):
            print(f"\n⏱️ Minuto {minuto} - {momenti.get(minuto, '🎭 La scena continua...')}")
            
            if minuto == 30:
                input("👉 Premi Invio per parlare col vicino...")
                self.chiacchiera_con_vicino(id_posto)

            elif minuto == 60:
                input("👉 Premi Invio per usufruire del servizio in posto...")
                self.usufruisci_servizio_in_posto(id_posto)

            elif minuto == self.durata_minuti:
                print("👏 Grazie per averci accompagnato in questa avventura teatrale!")

            time.sleep(2)  # Simulazione del tempo (accorciato per test)


# ========================================================== MENU SPETTACOLO INTERATTIVO ============================================
def menu(spettacolo: Spettacolo):
    # Menu interattivo per l'utente
    while True:
        print("\n📜 MENU INTERATTIVO SPETTACOLO")
        print("1️⃣  Chiacchiera con il vicino")
        print("2️⃣  Usufruisci del servizio in posto")
        print("3️⃣  Simula spettacolo")
        print("4️⃣  Esci")
        scelta = input("👉 Scegli un'opzione (1-4): ")

        match scelta:
            # Opzione per parlare col vicino
            case "1":
                try:
                    id_posto = int(input("🔢 Inserisci il tuo ID posto VIP: "))
                    spettacolo.chiacchiera_con_vicino(id_posto)
                except ValueError:
                    print("⚠️ Inserisci un numero valido per l'ID posto.")

            # Opzione per usufruire del servizio in posto
            case "2":
                try:
                    id_posto = int(input("🔢 Inserisci il tuo ID posto VIP: "))
                    spettacolo.usufruisci_servizio_in_posto(id_posto)
                except ValueError:
                    print("⚠️ Inserisci un numero valido per l'ID posto.")

            # Opzione per simulare lo spettacolo
            case "3":
                try:
                    id_posto = int(input("🔢 Inserisci il tuo ID posto VIP: "))
                    spettacolo.simula_spettacolo(id_posto)
                except ValueError:
                    print("⚠️ Inserisci un numero valido per l'ID posto.")

            # Uscita dal programma
            case "4":
                print("👋 Grazie per essere stato con noi! A presto tra le poltrone rosse del teatro.")
                break

            case _:
                print("❌ Scelta non valida. Riprova con un numero da 1 a 4.")

                
if __name__ == "__main__":
    conn = db.connetti_db()
    if conn:
        spettacolo = Spettacolo("Romeo e Giulietta", 135, conn)
        menu(spettacolo)
        conn.close()


