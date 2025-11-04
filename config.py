import pygame

WIDTH = 800
HEIGH = 600

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.set_caption("Tiny Football")
screen = pygame.display.set_mode((WIDTH,HEIGH))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (60, 120, 150)
GRAY = (200, 200, 200)
GREEN_FIELD = (63, 122, 57)
YELLOW = (255,255,0)
RED = (255, 0, 0)