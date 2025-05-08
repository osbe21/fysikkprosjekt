import pygame as pg
import numpy as np
from constants import *


class Block:
    def __init__(self, x, y, width, height, is_immovable=False):
        self.mass = width * height / px_per_meter**2
        self.sum_forces = np.zeros(2)
        self.velocity = np.zeros(2)
        self.position = np.array([x, y], dtype=float) / px_per_meter

        self.rect = pg.Rect((0, 0), (width, height))
        self.rect.center = convert_to_pygame_pos(self.position)

        self.is_immovable = is_immovable
    
    def add_force(self, force):
        self.sum_forces += force

    def update_position(self, dt):
        if not self.is_immovable:
            self.velocity += self.sum_forces / self.mass * dt
            self.position += self.velocity * dt

        self.sum_forces = np.zeros(2)

    def draw(self, screen, font):
        self.rect.center = convert_to_pygame_pos(self.position)

        color = GRAY if self.is_immovable else BLUE
        pg.draw.rect(screen, color, self.rect)

        if not self.is_immovable:
            render_text(screen, font, f"{self.mass:.1f}kg", self.rect.center)
