from Filosofo import Filosofo
from Jantar import JantarDosFilosofos
from Interface import InterfaceJantar

def main():
    # Configuração do jantar
    num_filosofos = 5
    jantar = JantarDosFilosofos(num_filosofos)
    
    # Configuração da interface
    interface = InterfaceJantar(jantar)
    jantar.registrar_observador(interface)
    
    # Criação dos filósofos
    filosofos = [Filosofo(i, jantar) for i in range(num_filosofos)]
    
    # Inicia os filósofos
    for f in filosofos:
        f.start()
    
    # Inicia a interface
    interface.executar()

if __name__ == "__main__":
    main()