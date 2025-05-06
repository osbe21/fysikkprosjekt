import pygame as pg


class Block(pg.sprite.Sprite):
    def __init__(self, screen, x, y, width, height, is_immovable=False):
        self.screen = screen
        self.is_immovable = is_immovable

        self.connected_springs = []

        self.sum_forces = 0

    def update(self):
        if self.is_immovable:
            self.sum_forces = 0

    def connect_spring(self, spring):
        self.connect_spring.append(spring)
