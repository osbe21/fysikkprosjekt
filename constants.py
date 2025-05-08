# Skjerm
WIDTH = 1200
HEIGHT = 800
FPS = 120

# Farger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 100, 255)
RED = (255, 100, 0)
GREEN = (0, 200, 50)

# Fysikk-konstanter
g = 9.81           # Tyngderaft (m/s^2)
k = 20           # Fjærkonstant (N/m)
b = 0.3          # Luftmotstand/demping (Ns/m)
px_per_meter = 100  # Brukes for konvertering mellom meter og pixler
time_scale = 1
delta_time = 1 / FPS * time_scale


def render_text(screen, font, text, center_pos, color=(255, 255, 255)):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center_pos)
        screen.blit(text_surface, text_rect)

def convert_to_pygame_pos(array):
    return tuple((array * px_per_meter).astype(int))