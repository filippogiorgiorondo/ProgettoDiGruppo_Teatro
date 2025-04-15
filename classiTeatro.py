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
        else:
            print("Posto già prenotato")

    def libera(self):
        if self.get_occupato():
            self.set_occupato(False) 
            print("Posto liberato")
        else:
            print("Il posto era già libero")

class PostoVip(Posto):
    def __init__(self, numero, fila, occupato=False):
        super().__init__(numero, fila, occupato)
        self.servizi = None #query per raccogliere servizi
        
    def prenota(self):
        if not self.get_occupato():
            self.set_occupato(True) 
            print("Posto prenotato")
            if input("Vuoi aggiungere servizi extra? s/n ---> ").lower().strip():
                print("--- Menu Servizi ---")# 3/4/5
                for r in self.servizi:
                    print(r[3])
        else:
            print("Posto già prenotato")