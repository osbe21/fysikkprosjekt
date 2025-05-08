import pygame as pg
import numpy as np
from constants import *

class Spring:
    def __init__(self, block_1, block_2, rel_pos_1, rel_pos_2):
        self.rest_length = 2#np.linalg.norm(block_1.position - block_2.position)

        self.block_1 = block_1
        self.block_2 = block_2

        self.rel_pos_1 = rel_pos_1 / px_per_meter
        self.rel_pos_2 = rel_pos_2 / px_per_meter
    
    def apply_forces(self):
        dist_vector = (self.block_2.position + self.rel_pos_2) - (self.block_1.position + self.rel_pos_1)

        dist = np.linalg.norm(dist_vector)

        displacement = dist - self.rest_length

        unit_dir = dist_vector / dist

        # Hookes lov (F = k*x)
        self.block_1.add_force(k * displacement * unit_dir)
        self.block_2.add_force(k * displacement * -unit_dir)
    
    def draw(self, screen):
        pg.draw.line(screen, BLACK, convert_to_pygame_pos(self.block_1.position + self.rel_pos_1), convert_to_pygame_pos(self.block_2.position + self.rel_pos_2))