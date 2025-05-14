import pygame
from pygame.locals import *
from Jantar import Estado

class InterfaceJantar:
    def __init__(self, jantar, largura=800, altura=600):
        self.jantar = jantar
        self.largura = largura
        self.altura = altura
        self.estados = None
        
        # Cores
        self.CORES = {
            Estado.PENSANDO: (0, 0, 255),    # Azul
            Estado.FAMINTO: (255, 0, 0),    # vermelho
            Estado.COMENDO: (0, 255, 0)       # Verde
        }
        
        self.inicializar_pygame()
    
    def inicializar_pygame(self):
        pygame.init()
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Jantar dos Filósofos")
        self.fonte = pygame.font.SysFont('Arial', 20)
    
    def atualizar(self, estados):
        self.estados = estados
        self.desenhar()
    
    def desenhar(self):
        self.tela.fill((255, 255, 255))
        
        centro = (self.largura // 2, self.altura // 2)
        raio_mesa = 200
        raio_filosofos = 150
        raio_garfos = 180
        
        # Desenha a mesa
        pygame.draw.circle(self.tela, (150, 150, 150), centro, raio_mesa)
        
        # Desenha os filósofos
        if self.estados:
            for i, estado in enumerate(self.estados):
                pos = self._calcular_posicao(i, raio_filosofos, centro)
                cor = self.CORES[estado]
                pygame.draw.circle(self.tela, cor, pos, 30)
                texto = self.fonte.render(f"F{i}", True, (0, 0, 0))
                self.tela.blit(texto, (pos[0] - 10, pos[1] - 10))
        
        # Desenha os garfos
        for i in range(len(self.estados) if self.estados else 5):
            pos_garfo = self._calcular_posicao(i + 0.5, raio_garfos, centro)
            pygame.draw.line(self.tela, (0, 0, 0), pos_garfo, (pos_garfo[0] + 10, pos_garfo[1] + 10), 3)
            pygame.draw.line(self.tela, (0, 0, 0), pos_garfo, (pos_garfo[0] - 10, pos_garfo[1] + 10), 3)
        
        # Legenda
        self._desenhar_legenda()
        
        pygame.display.flip()
    
    def _calcular_posicao(self, i, raio, centro):
        import math
        angulo = 2 * math.pi * i / (len(self.estados) if self.estados else 5)
        x = centro[0] + raio * math.cos(angulo)
        y = centro[1] + raio * math.sin(angulo)
        return (int(x), int(y))
    
    def _desenhar_legenda(self):
        y = 20
        for estado, cor in self.CORES.items():
            pygame.draw.rect(self.tela, cor, (20, y, 20, 20))
            texto = self.fonte.render(estado.name, True, (0, 0, 0))
            self.tela.blit(texto, (50, y))
            y += 30
    
    def executar(self):
        relogio = pygame.time.Clock()
        executando = True
        
        while executando:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    executando = False
            
            relogio.tick(30)
        
        pygame.quit()