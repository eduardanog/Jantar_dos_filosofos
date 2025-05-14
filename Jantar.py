import threading
from enum import Enum, auto

class Estado(Enum):
    PENSANDO = auto()
    FAMINTO = auto()
    COMENDO = auto()

class JantarDosFilosofos:
    def __init__(self, num_filosofos=5):
        self.num_filosofos = num_filosofos
        self.estados = [Estado.PENSANDO for _ in range(num_filosofos)]
        self.mutex = threading.Lock()
        self.semaforos = [threading.Semaphore(0) for _ in range(num_filosofos)]
        self.observadores = []
    
    def registrar_observador(self, observador):
        self.observadores.append(observador)
    
    def atualizar_estado(self, id, estado_str):
        estado = Estado[estado_str]
        with self.mutex:
            self.estados[id] = estado
        self.notificar_observadores()
    
    def notificar_observadores(self):
        for obs in self.observadores:
            obs.atualizar(self.estados)
    
    def pegar_garfos(self, i):
        with self.mutex:
            self.estados[i] = Estado.FAMINTO
            self._testar(i)
        self.semaforos[i].acquire()
    
    def largar_garfos(self, i):
        with self.mutex:
            self.estados[i] = Estado.PENSANDO
            self._testar((i - 1) % self.num_filosofos)
            self._testar((i + 1) % self.num_filosofos)
        self.notificar_observadores()
    
    def _testar(self, i):
        esquerda = (i - 1) % self.num_filosofos
        direita = (i + 1) % self.num_filosofos
        
        if (self.estados[i] == Estado.FAMINTO and
            self.estados[esquerda] != Estado.COMENDO and
            self.estados[direita] != Estado.COMENDO):
            
            self.estados[i] = Estado.COMENDO
            self.semaforos[i].release()