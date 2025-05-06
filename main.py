import pygame
from constants import WIDTH, HEIGHT, WHITE, BLACK, BLUE, FPS, x0, amplitude, dt, akselerasjon

# Initier pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fjær og masse simulering")
clock = pygame.time.Clock()

settings_open = False
settings_button_rect = pygame.Rect(10, HEIGHT - 60, 120, 50)
close_button_rect = pygame.Rect(0, 0, 40, 40)
font = pygame.font.SysFont(None, 36)

air_resistance = False

# Initialverdier
x = x0 + amplitude
v = 0

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if settings_open:
                box_rect = pygame.Rect(300, 200, 600, 400)
                toggle_rect = pygame.Rect(box_rect.x + 250, box_rect.y + 90, 40, 40)
                if close_button_rect.collidepoint(mx, my):
                    settings_open = False
                elif toggle_rect.collidepoint(mx, my):
                    air_resistance = not air_resistance

            if settings_button_rect.collidepoint(mx, my):
                settings_open = True

    # === FYSIKK ===
    a = akselerasjon(x, v) if air_resistance else akselerasjon(x, 0)
    v += a * dt
    x += v * dt

    # === TEGNING ===
    screen.fill(WHITE)

    # Simulering (fjær + masse)
    pygame.draw.line(screen, BLACK, (100, HEIGHT // 2), (x, HEIGHT // 2), 5)
    pygame.draw.circle(screen, BLUE, (int(x), HEIGHT // 2), 20)

    # Settings-knapp
    pygame.draw.rect(screen, (100, 100, 200), settings_button_rect)
    settings_text = font.render("Settings", True, WHITE)
    screen.blit(settings_text, (settings_button_rect.x + 5, settings_button_rect.y + 10))

    # Settings-meny
    if settings_open:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        box_rect = pygame.Rect(300, 200, 600, 400)
        pygame.draw.rect(screen, (60, 60, 60), box_rect)
        pygame.draw.rect(screen, (200, 200, 200), box_rect, 2)

        title_surf = font.render("Settings", True, WHITE)
        screen.blit(title_surf, (box_rect.x + 20, box_rect.y + 20))

        close_button_rect.topleft = (box_rect.right - 50, box_rect.y + 10)
        pygame.draw.rect(screen, (150, 50, 50), close_button_rect)
        close_text = font.render("X", True, WHITE)
        screen.blit(close_text, (close_button_rect.x + 10, close_button_rect.y))

        # Luftmotstand toggle
        label_surf = font.render("Luftmotstand", True, WHITE)
        screen.blit(label_surf, (box_rect.x + 50, box_rect.y + 100))
        toggle_rect = pygame.Rect(box_rect.x + 250, box_rect.y + 90, 40, 40)
        color = (0, 200, 0) if air_resistance else (200, 0, 0)
        pygame.draw.rect(screen, color, toggle_rect)
        pygame.draw.rect(screen, WHITE, toggle_rect, 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
