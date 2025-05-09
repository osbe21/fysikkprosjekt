import pygame as pg
import numpy as np
from constants import *
from block import Block
from spring import Spring

# Initier pg
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Fjær og masse simulering")
clock = pg.time.Clock()
delta_time = 1 / FPS

is_paused = False

settings_open = False
settings_button_rect = pg.Rect(10, HEIGHT - 60, 120, 50)
close_button_rect = pg.Rect(0, 0, 40, 40)
font = pg.font.SysFont(None, 36)

air_resistance = False

block_1 = Block(220, 200, 200, 100)
block_2 = Block(200, 50, 100, 20, is_immovable=True)
blocks = [block_1, block_2]
springs = [Spring(block_1, block_2, np.array([0, 0]), np.array([0, 0]))]

def update_objects():
    for spring in springs:
        spring.apply_forces()

    for block in blocks:
        block.add_force(g * block.mass * np.array([0, 1])) # Tyngdekraft (g*m)
        block.add_force(b * -block.velocity) # Luftmotstand (-b*v)
        block.update_position(delta_time)

def draw_objects():
    for block in blocks:
        block.draw(screen, font)
    
    for spring in springs:
        spring.draw(screen)

# Game loop
running = True
while running:
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if settings_open:
                box_rect = pg.Rect(300, 200, 600, 400)
                toggle_rect = pg.Rect(box_rect.x + 250, box_rect.y + 90, 40, 40)
                if close_button_rect.collidepoint(mx, my):
                    settings_open = False
                elif toggle_rect.collidepoint(mx, my):
                    air_resistance = not air_resistance

            elif settings_button_rect.collidepoint(mx, my):
                settings_open = True

    # === TEGNING ===
    screen.fill(WHITE)

    if not is_paused:
        update_objects()
    
    draw_objects()

    # Settings-knapp
    pg.draw.rect(screen, (100, 100, 200), settings_button_rect)
    settings_text = font.render("Settings", True, WHITE)
    screen.blit(settings_text, (settings_button_rect.x + 5, settings_button_rect.y + 10))

    # Settings-meny
    if settings_open:
        overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        box_rect = pg.Rect(300, 200, 600, 400)
        pg.draw.rect(screen, (60, 60, 60), box_rect)
        pg.draw.rect(screen, (200, 200, 200), box_rect, 2)

        title_surf = font.render("Settings", True, WHITE)
        screen.blit(title_surf, (box_rect.x + 20, box_rect.y + 20))

        close_button_rect.topleft = (box_rect.right - 50, box_rect.y + 10)
        pg.draw.rect(screen, (150, 50, 50), close_button_rect)
        close_text = font.render("X", True, WHITE)
        screen.blit(close_text, (close_button_rect.x + 10, close_button_rect.y))

        # Luftmotstand toggle
        label_surf = font.render("Luftmotstand", True, WHITE)
        screen.blit(label_surf, (box_rect.x + 50, box_rect.y + 100))
        toggle_rect = pg.Rect(box_rect.x + 250, box_rect.y + 90, 40, 40)
        color = (0, 200, 0) if air_resistance else (200, 0, 0)
        pg.draw.rect(screen, color, toggle_rect)
        pg.draw.rect(screen, WHITE, toggle_rect, 2)

    pg.display.flip()
    delta_time = clock.tick(FPS) / 1000 * time_scale

pg.quit()
