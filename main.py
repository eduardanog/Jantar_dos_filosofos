# main.py
import pygame

from Interface import InterfaceJantar

pygame.init()
WIDTH, HEIGHT = 900,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jantar dos Filósofos")
font = pygame.font.SysFont('Roboto', 18)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 30, 0)
GREEN = (51, 204, 102)
BLUE = (102, 153, 255)
YELLOW = (255, 255, 153)


def main():
    jantar = InterfaceJantar(screen, font, WIDTH, HEIGHT, WHITE, BLACK, RED, GREEN, BLUE, YELLOW)
    jantar.iniciar_jantar()

if __name__ == "__main__":
    main()
