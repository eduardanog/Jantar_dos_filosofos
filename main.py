from Filosofo import Filosofo
from Jantar import JantarDosFilosofos
from Interface import InterfaceJantar

def main():
    #configuração do jantar
    num_filosofos = 5
    jantar = JantarDosFilosofos(num_filosofos)
    
    #configuração da interface
    interface = InterfaceJantar(jantar)
    jantar.registrar_observador(interface)
    
    #criação dos filósofos
    filosofos = [Filosofo(i, jantar) for i in range(num_filosofos)]
    
    for f in filosofos:
        f.start()
    
    interface.executar()

if __name__ == "__main__":
    main()