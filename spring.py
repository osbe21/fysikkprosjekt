import pygame as pg
import numpy as np
from data_logger import DataLogger
from constants import *

class Spring:
    next_letter_name = "A"

    def __init__(self, block_1, block_2, rel_pos_1, rel_pos_2):
        #TODO: Gjør at man kan endre denne verdien dynamisk
        self.rest_length = 1 #np.linalg.norm(block_1.position - block_2.position)

        self.block_1 = block_1
        self.block_2 = block_2

        self.rel_pos_1 = rel_pos_1 / px_per_meter
        self.rel_pos_2 = rel_pos_2 / px_per_meter

        self.letter_name = Spring.next_letter_name
        Spring.next_letter_name = chr(ord(Spring.next_letter_name) + 1)

        self.logger = DataLogger(f"Fjærkraft {self.letter_name}")
    
    def apply_forces(self, elapsed_time):
        dist_vector = (self.block_2.position + self.rel_pos_2) - (self.block_1.position + self.rel_pos_1)

        dist = np.linalg.norm(dist_vector)

        displacement = dist - self.rest_length

        unit_dir = dist_vector / dist

        # Hookes lov (F = k*x)
        force = k * displacement

        self.block_1.add_force(force * unit_dir)
        self.block_2.add_force(force * -unit_dir)

        self.logger.log(elapsed_time, force)
    
    def draw(self, screen, font):
        point_1 = self.block_1.position + self.rel_pos_1
        point_2 = self.block_2.position + self.rel_pos_2

        dist = np.linalg.norm(point_1 - point_2)

        text = f"{self.letter_name}: {dist:.1f}m"

        pg.draw.line(screen, BLACK, convert_to_pygame_pos(point_1), convert_to_pygame_pos(point_2))
        render_text(screen, font, text, convert_to_pygame_pos((point_1 + point_2)/2), BLACK, WHITE)