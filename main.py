# main.py

import pygame
from constants import WIDTH, HEIGHT, WHITE, BLACK, BLUE, FPS, x0, amplitude, dt, akselerasjon

# Initier pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fjær og masse simulering")
clock = pygame.time.Clock()

# Initialverdier
x = x0 + amplitude
v = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Tegn
    screen.fill(WHITE)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
