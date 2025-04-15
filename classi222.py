import funzionidb as db
conn = db.connetti_db()
class Posto:
    def __init__(self, numero, fila, occupato=False):
        self._numero = numero
        self._fila = fila
        self._occupato = occupato

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
            #queri per il posto a true
        else:
            print("Posto già prenotato")

    def libera(self):
        if self.get_occupato():
            self.set_occupato(False) 
            print("Posto liberato")
            #queri per liberare il posto
        else:
            print("Il posto era già libero")

class PostoVip(Posto):
    def __init__(self, numero, fila, occupato=False):
        super().__init__(numero, fila, occupato)
        self.servizi = ["acesso_loung","servizio_in_posto","regalo_benvenuto"]
        
    def prenota(self):
        if not self.get_occupato():
            costa = 50.0
            self.set_occupato(True) 
            print("Posto prenotato")
            db.prenota_posto_vip(conn,self.get_numero())
            if input("Vuoi aggiungere servizi extra? (ogni servizio costa 20$) s/n ---> ").lower().strip():
                print("--- Menu Servizi ---")
                for i, r in enumerate(self.servizi, start=1):
                    print(f"{i}. {r[0]}")
                while True:
                    try:
                        ch = int(input("Inserisci il servizio che vuoi prenotare (ogni servizio costa 20$) ---> "))
                        match ch:
                            case 1:
                                pass
                                db.verifica_servizio_vip(conn,self.servizi[1])
                                db.prenota_servizio_vip(conn,self.get_numero(),self.servizi[1])
                                costa += 20
                            case 2:
                                pass
                                db.verifica_servizio_vip(conn,self.servizi[2])
                                db.prenota_servizio_vip(conn,self.get_numero(),self.servizi[2])
                                costa += 20
                            case 3:
                                pass
                                db.verifica_servizio_vip(conn,self.servizi[3])
                                db.prenota_servizio_vip(conn,self.get_numero(),self.servizi[3])
                                costa += 20
                        print("Servizio prenotato")
                        if input("Vuoi prenotare un altro servizo? s/n ---> ").lower().strip() != "s":
                            break
                    except:
                        print("Errore di inserimento")
            
        else:
            print("Posto già prenotato")
    
    def libera(self):
        if self.get_occupato():
            self.set_occupato(False) 
            print("Posto liberato")
            db.cancella_prenotazione_vip(conn,self.get_numero())
        else:
            print("Il posto era già libero")

class PostoPlebe(Posto):
    def __init__(self, numero, fila, occupato=False):
        super().__init__(numero, fila, occupato)

    def prenota(self):
        if not self.get_occupato():
            self.set_occupato(True)
            costo = self.calcola_costo()
            print(f"Posto plebe prenotato. Prezzo: {costo}$")
            db.prenota_posto_plebe(conn,self.get_numero())
        else:
            print("Posto già prenotato")

    def calcola_costo(self):
        numero = self.get_numero()
        if 150 <= numero <= 250:
            return 30.0  # prezzo alto per i posti centrali
        elif 1 <= numero <= 149:
            return 20.0  # prezzo medio
        elif 251 <= numero <= 300:
            return 10.0  # prezzo basso
        else:
            print("Numero posto non valido (fuori dal range 1-300)")
            return 0.0
    
    def libera(self):
        if self.get_occupato():
            self.set_occupato(False) 
            print("Posto liberato")
            db.cancella_prenotazione_plebe(conn,self.get_numero())
        else:
            print("Il posto era già libero")
            
class Teatro:
    def menu(self):
        while True:
            print("\n🎭 MENU TEATRO")
            print("1. Visualizza posti plebe disponibili")
            print("2. Visualizza posti VIP disponibili")
            print("3. Prenota posto plebe")
            print("4. Prenota posto VIP")
            print("5. Cancella prenotazione plebe")
            print("6. Cancella prenotazione VIP")
            print("7. Verifica stato servizio VIP")
            print("8. Prenota servizio VIP")
            print("9. Esci")

            scelta = input("Seleziona un'opzione: ")

            match scelta:
                case "1":
                    db.posti_disponibili_plebe(conn)
                case "2":
                    db.posti_disponibili_vip(conn)
                case "3":
                    try:
                        id_posto = int(input("Inserisci ID posto plebe da prenotare: "))
                        db.prenota_posto_plebe(conn, id_posto)
                    except ValueError:
                        print("❌ Inserisci un ID valido.")
                case "4":
                    try:
                        id_posto = int(input("Inserisci ID posto VIP da prenotare: "))
                        db.prenota_posto_vip(conn, id_posto)
                    except ValueError:
                        print("❌ Inserisci un ID valido.")
                case "5":
                    try:
                        id_posto = int(input("Inserisci ID posto plebe da cancellare: "))
                        db.cancella_prenotazione_plebe(conn, id_posto)
                    except ValueError:
                        print("❌ Inserisci un ID valido.")
                case "6":
                    try:
                        id_posto = int(input("Inserisci ID posto VIP da cancellare: "))
                        db.cancella_prenotazione_vip(conn, id_posto)
                    except ValueError:
                        print("❌ Inserisci un ID valido.")
                case "7":
                    servizio = input("Inserisci servizio (accesso_lounge, servizio_in_posto, regalo_benvenuto): ").strip()
                    db.verifica_servizio_vip(conn, servizio)
                case "8":
                    try:
                        id_posto = int(input("Inserisci ID posto VIP: "))
                        servizio = input("Inserisci servizio da prenotare (accesso_lounge, servizio_in_posto, regalo_benvenuto): ").strip()
                        db.prenota_servizio_vip(conn, id_posto, servizio)
                    except ValueError:
                        print("❌ Inserisci un ID valido.")
                case "9":
                    print("👋 Uscita dal programma.")
                    break
                case _:
                    print("❌ Scelta non valida. Riprova.")