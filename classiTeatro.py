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
                                #queri controllo servizio prenotato
                                #queri setta servizio prenotato
                                costa += 20
                            case 2:
                                pass
                                #queri controllo servizio prenotato
                                #queri setta servizio prenotato
                                costa += 20
                            case 3:
                                pass
                                #queri controllo servizio prenotato
                                #queri setta servizio prenotato
                                costa += 20
                        if input("Vuoi prenotare un altro servizo? s/n ---> ").lower().strip() != "s":
                            break
                    except:
                        print("Errore di inserimento")
            print(f"Posto prenotato ")
        else:
            print("Posto già prenotato")
            
class PostoPlebe(Posto):
    def __init__(self, numero, fila, occupato=False):
        super().__init__(numero, fila, occupato)

    def prenota(self):
        if not self.get_occupato():
            self.set_occupato(True)
            costo = self.calcola_costo()
            print(f"Posto plebe prenotato. Prezzo: {costo}$")
            # qui puoi aggiungere una "query" per segnare il posto come occupato nel database
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
