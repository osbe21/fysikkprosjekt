import pygame as pg

class Spring(pg.sprite.Sprite):
    def __init__(self, screen, connection_1, connection_2):
        self.screen = screen
        self.rest_length = connection_1.rect
        self.connections = (connection_1, connection_2)
    
    def get_force(self):
        pass