import pygame
import sys
import threading
import time
import random
from pygame.locals import *

# Configurações iniciais
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jantar dos Filósofos")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)

# Fontes
font = pygame.font.SysFont('Arial', 20)

# Número de filósofos
N = 5

# Estado dos filósofos
PENSANDO, FAMINTO, COMENDO = 0, 1, 2
estados = [PENSANDO] * N
estados_cores = {PENSANDO: BLUE, FAMINTO: RED, COMENDO: GREEN}

# Semáforos para cada filósofo e para o mutex
mutex = threading.Semaphore(1)
semaforos = [threading.Semaphore(0) for _ in range(N)]

# Posições dos filósofos e garfos na mesa
centro = (WIDTH // 2, HEIGHT // 2)
raio_mesa = 200
raio_filosofos = 150
raio_garfos = 180

def calcular_posicao(i, raio):
    angulo = 2 * 3.14159 * i / N
    x = centro[0] + raio * pygame.math.Vector2(1, 0).rotate(angulo * 180 / 3.14159).x
    y = centro[1] + raio * pygame.math.Vector2(1, 0).rotate(angulo * 180 / 3.14159).y
    return (int(x), int(y))

def filosofo(i):
    while True: 
        pensar(i)
        pegar_garfos(i)
        comer(i)
        largar_garfos(i)

def pensar(i):
    estados[i] = PENSANDO
    time.sleep(random.uniform(1, 3))

def comer(i):
    estados[i] = COMENDO
    time.sleep(random.uniform(1, 3))

def pegar_garfos(i):
    mutex.acquire()
    estados[i] = FAMINTO
    testar(i)
    mutex.release()
    semaforos[i].acquire()

def largar_garfos(i):
    mutex.acquire()
    estados[i] = PENSANDO
    testar((i + N - 1) % N)
    testar((i + 1) % N)
    mutex.release()

def testar(i):
    if estados[i] == FAMINTO and \
       estados[(i + N - 1) % N] != COMENDO and \
       estados[(i + 1) % N] != COMENDO:
        estados[i] = COMENDO
        semaforos[i].release()

def desenhar_mesa():
    # Desenha a mesa
    pygame.draw.circle(screen, GRAY, centro, raio_mesa)
    
    # Desenha os filósofos
    for i in range(N):
        pos = calcular_posicao(i, raio_filosofos)
        cor = estados_cores[estados[i]]
        pygame.draw.circle(screen, cor, pos, 30)
        texto = font.render(f"F{i}", True, BLACK)
        screen.blit(texto, (pos[0] - 10, pos[1] - 10))
    
    # Desenha os garfos
    for i in range(N):
        pos_garfo = calcular_posicao(i + 0.5, raio_garfos)
        pygame.draw.line(screen, BLACK, pos_garfo, (pos_garfo[0] + 10, pos_garfo[1] + 10), 3)
        pygame.draw.line(screen, BLACK, pos_garfo, (pos_garfo[0] - 10, pos_garfo[1] + 10), 3)
    
    # Legenda
    legenda_y = 20
    for estado, cor in estados_cores.items():
        nome = ["Pensando", "Faminto", "Comendo"][estado]
        pygame.draw.rect(screen, cor, (20, legenda_y, 20, 20))
        texto = font.render(nome, True, BLACK)
        screen.blit(texto, (50, legenda_y))
        legenda_y += 30

def main():
    # Inicia as threads dos filósofos
    filosofos = []
    for i in range(N):
        filosofo_thread = threading.Thread(target=filosofo, args=(i,), daemon=True)
        filosofos.append(filosofo_thread)
        filosofo_thread.start()
    
    # Loop principal do Pygame
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        screen.fill(WHITE)
        desenhar_mesa()
        
        # Atualiza a tela
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()