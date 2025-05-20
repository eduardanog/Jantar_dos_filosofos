import pygame

from Interface import InterfaceJantar

pygame.init()
WIDTH, HEIGHT = 900,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jantar dos Filósofos")
font = pygame.font.SysFont('Roboto', 18)

branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 30, 0)
verde = (51, 204, 102)
azul = (102, 153, 255)
amarelo = (255, 255, 153)


def main():
    jantar = InterfaceJantar(screen, font, WIDTH, HEIGHT, branco, preto, vermelho, verde, azul, amarelo)
    jantar.iniciar_jantar()

if __name__ == "__main__":
    main()
