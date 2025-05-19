# jantar_filosofos.py
import threading
import random
import time
import pygame
from pygame.locals import *
import sys

PENSANDO, FAMINTO, COMENDO = 0, 1, 2
N = 5

class InterfaceJantar:
    def __init__(self, screen, font, width, height, WHITE, BLACK, RED, GREEN, BLUE, YELLOW):
        self.screen = screen
        self.font = font
        self.WIDTH = width
        self.HEIGHT = height
        self.WHITE = WHITE
        self.BLACK = BLACK
        self.RED = RED
        self.GREEN = GREEN
        self.BLUE = BLUE
        self.YELLOW = YELLOW

        self.centro = (width // 2, height // 2)
        self.raio_mesa = 210
        self.raio_filosofos = 150
        self.raio_garfos = 180

        self.estados = [PENSANDO] * N
        self.estados_cores = {PENSANDO: self.BLUE, FAMINTO: self.RED, COMENDO: self.GREEN}
        self.mutex = threading.Semaphore(1)
        self.semaforos = [threading.Semaphore(0) for _ in range(N)]

        self.imagem_garfo = pygame.image.load("garfo.png").convert_alpha()
        self.imagem_garfo = pygame.transform.scale(self.imagem_garfo, (40, 40))  
        

    def calcular_posicao(self, i, raio):
        angulo = 2 * 3.14159 * i / N
        x = self.centro[0] + raio * pygame.math.Vector2(1, 0).rotate(angulo * 180 / 3.14159).x
        y = self.centro[1] + raio * pygame.math.Vector2(1, 0).rotate(angulo * 180 / 3.14159).y
        return (int(x), int(y))

    def pensar(self, i):
        self.estados[i] = PENSANDO
        time.sleep(random.uniform(1, 3))

    def comer(self, i):
        self.estados[i] = COMENDO
        time.sleep(random.uniform(1, 3))

    def pegar_garfos(self, i):
        self.mutex.acquire()
        self.estados[i] = FAMINTO
        self.testar(i)
        self.mutex.release()
        self.semaforos[i].acquire()

    def largar_garfos(self, i):
        self.mutex.acquire()
        self.estados[i] = PENSANDO
        self.testar((i + N - 1) % N)
        self.testar((i + 1) % N)
        self.mutex.release()

    def testar(self, i):
        if self.estados[i] == FAMINTO and \
           self.estados[(i + N - 1) % N] != COMENDO and \
           self.estados[(i + 1) % N] != COMENDO:
            self.estados[i] = COMENDO
            self.semaforos[i].release()

    def filosofo(self, i):
        while True:
            self.pensar(i)
            self.pegar_garfos(i)
            self.comer(i)
            self.largar_garfos(i)

    def desenhar_mesa(self):
        pygame.draw.circle(self.screen, self.YELLOW, self.centro, self.raio_mesa)
        
        for i in range(N):
            pos = self.calcular_posicao(i, self.raio_filosofos)
            cor = self.estados_cores[self.estados[i]]
            pygame.draw.circle(self.screen, cor, pos, 25)
            texto = self.font.render(f"FL {i}", True, self.BLACK)
            self.screen.blit(texto, (pos[0] - 12, pos[1] - 7))
        
        import math

        for i in range(N):
            pos_garfo = self.calcular_posicao(i + 0.5, self.raio_garfos)

            dx = self.centro[0] - pos_garfo[0]
            dy = self.centro[1] - pos_garfo[1]
            angulo = math.atan2(dy, dx)

            angulo_graus = math.degrees(angulo) + 90 

            garfo_rotacionado = pygame.transform.rotate(self.imagem_garfo, -angulo_graus)
            rect = garfo_rotacionado.get_rect(center=pos_garfo)

            self.screen.blit(garfo_rotacionado, rect)

        
        legenda_y = 480
        for estado, cor in self.estados_cores.items():
            nome = ["Pensando", "Faminto", "Comendo"][estado]
            pygame.draw.rect(self.screen, cor, (20, legenda_y, 15, 15))
            texto = self.font.render(nome, True, self.BLACK)
            self.screen.blit(texto, (50, legenda_y))
            legenda_y += 40

    def iniciar_jantar(self):
        for i in range(N):
            threading.Thread(target=self.filosofo, args=(i,), daemon=True).start()

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            
            self.screen.fill(self.WHITE)
            self.desenhar_mesa()
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()
