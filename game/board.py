import pygame
from . import settings

class Board:
    def __init__(self, width, height, color, origin, size):
        self.width = width
        self.height = height
        self.color = color
        self.origin = origin
        self.size = size

    def draw(self,screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen,
                                 self.color,
                                 (self.origin[0] + j * self.size,
                                  self.origin[1] + i * self.size, 
                                  self.size, 
                                  self.size),
                                 width=1)
        pygame.draw.rect(screen,
                                 self.color,
                                 (self.origin[0],
                                  self.origin[1],
                                  self.size * self.height, 
                                  self.size * self.width),
                                 width=4)
                
        