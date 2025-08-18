import pygame
from . import settings

class Board:
    def __init__(self, width, height, color, origin, screen, size):
        self.width = width
        self.height = height
        self.color = color
        self.origin = origin
        self.screen = screen
        self.size = size

    def draw(self):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(self.screen,
                                 (0, 0, 0),
                                 ((settings.display_width - self.size*9)/2 + j * self.size,
                                  (settings.display_height - self.size*9)/2 + i * self.size, 
                                  self.size, 
                                  self.size),
                                  width=2)
        