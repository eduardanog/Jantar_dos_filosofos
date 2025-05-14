import threading
import time
import random

class Filosofo(threading.Thread):
    def __init__(self, id, jantar):
        super().__init__(daemon=True)
        self.id = id
        self.jantar = jantar
        
    def run(self):
        while True:
            self.pensar()
            self.comer()
    
    def pensar(self):
        self.jantar.atualizar_estado(self.id, "PENSANDO")
        time.sleep(random.uniform(1, 3))
    
    def comer(self):
        self.jantar.atualizar_estado(self.id, "FAMINTO")
        self.jantar.pegar_garfos(self.id)
        
        self.jantar.atualizar_estado(self.id, "COMENDO")
        time.sleep(random.uniform(1, 3))
        
        self.jantar.largar_garfos(self.id)