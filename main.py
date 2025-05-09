import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
import constants as const
from block import Block
from spring import Spring

# Initier pg
pg.init()
screen = pg.display.set_mode((const.WIDTH, const.HEIGHT))
pg.display.set_caption("Fjær og masse simulering")
clock = pg.time.Clock()

font = pg.font.SysFont(None, 36)

is_paused = True
in_block_mode = True

first_block_point = None
first_spring_object = None # (obj, rel_pos)

blocks = [Block(const.WIDTH/2, 25, const.WIDTH, 50, True)]
springs = []


def update_objects():
    for spring in springs:
        spring.apply_forces()

    for block in blocks:
        block.add_force(const.g * block.mass * np.array([0, 1])) # Tyngdekraft (g*m)
        block.add_force(const.b * -block.velocity) # Luftmotstand (-b*v)
        block.update_position()

def draw_objects():
    for block in blocks:
        block.draw(screen, font)
    
    for spring in springs:
        spring.draw(screen, font)

def render_state_text():
    text = "Simulasjonen er pauset ('P' for å starte)" if is_paused else "Simulasjonen kjører ('P' for å stoppe)"
    color = const.RED if is_paused else const.BLACK
    const.render_text(screen, font, text, (const.WIDTH/2, 150), color)
    
    text = ("Blokk" if in_block_mode else "Fjær") + " modus ('M' for å bytte)"
    color = const.BLUE if in_block_mode else const.GREEN
    const.render_text(screen, font, text, (const.WIDTH/2, 100), color)


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
                    first_spring_object = (selected_block, np.array([mx, my]) - selected_block.position * const.px_per_meter)
                else:
                    second_spring_object = (selected_block, np.array([mx, my]) - selected_block.position * const.px_per_meter)
                    springs.append(
                        Spring(
                            first_spring_object[0], 
                            second_spring_object[0], 
                            first_spring_object[1], 
                            second_spring_object[1])
                    )
                    first_spring_object = None

    # === TEGNING ===
    screen.fill(const.WHITE)

    if not is_paused:
        update_objects()
        const.time_elapsed += const.dt
    
    draw_objects()

    render_state_text()

    pg.display.flip()
    const.dt = clock.tick(const.FPS) / 1000 * const.time_scale

pg.quit()

for spring in springs:
    spring.logger.plot()

plt.legend()
plt.title("Fjærkraft over tid")
plt.xlabel("Kraft (N)")
plt.ylabel("Tid (s)")
plt.grid(axis='y')
plt.show()