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

font = pg.font.SysFont(None, 36)

is_paused = True
in_block_mode = True

first_block_point = None
first_spring_object = None # (obj, rel_pos)

blocks = [Block(WIDTH/2, 25, WIDTH, 50, True)]
springs = []


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
        
        # Bytt mellom å plassere blokk eller fjær
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                is_paused = not is_paused
            if event.key == pg.K_m:
                in_block_mode = not in_block_mode

        if event.type == pg.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if in_block_mode: # Plasser blokk
                if first_block_point is None:
                    first_block_point = (mx, my)
                else:
                    x = (mx + first_block_point[0])/2
                    y = (my + first_block_point[1])/2
                    width = abs(mx - first_block_point[0])
                    height = abs(my - first_block_point[1])

                    blocks.append(Block(x, y, width, height))

                    first_block_point = None
            
            else: # Plasser fjær
                selected_block = None

                for block in blocks:
                    if block.rect.collidepoint(mx, my):
                        selected_block = block
                        break
                
                if selected_block is None: # Trykket ikke på en blokk
                    continue

                if first_spring_object is None:
                    first_spring_object = (selected_block, np.array([mx, my]) - selected_block.position * px_per_meter)
                else:
                    second_spring_object = (selected_block, np.array([mx, my]) - selected_block.position * px_per_meter)
                    springs.append(
                        Spring(
                            first_spring_object[0], 
                            second_spring_object[0], 
                            first_spring_object[1], 
                            second_spring_object[1])
                    )
                    first_spring_object = None

    # === TEGNING ===
    screen.fill(WHITE)

    if not is_paused:
        update_objects()
    
    draw_objects()
    
    text = "Simulasjonen er pauset ('P' for å starte)" if is_paused else "Simulasjonen kjører ('P' for å stoppe)"
    color = RED if is_paused else BLACK
    render_text(screen, font, text, (WIDTH/2, 150), color)
    
    text = ("Blokk" if in_block_mode else "Fjær") + " modus ('M' for å bytte)"
    color = BLUE if in_block_mode else GREEN
    render_text(screen, font, text, (WIDTH/2, 100), color)

    pg.display.flip()
    delta_time = clock.tick(FPS) / 1000 * time_scale

pg.quit()
