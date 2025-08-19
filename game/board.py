import pygame
from . import settings

class Board:
    def __init__(self, width, height, color, origin, size, highlight_cell, highlight_color):
        self.width = width
        self.height = height
        self.color = color
        self.origin = origin
        self.size = size
        self.highlight_cell = highlight_cell
        self.highlight_color = highlight_color


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
                                  self.size * self.width, 
                                  self.size * self.height),
                                 width=4)
        for cell in self.highlight_cell:
            self.be_highlight_cell(cell,screen)
        
    def be_highlight_cell(self,cell,screen):
        pygame.draw.rect(screen,
                    self.highlight_color,
                    (self.origin[0] + cell[0] * self.size,
                    self.origin[1] + cell[1] * self.size, 
                    self.size, 
                    self.size),
                    width=2
                    )
    
    def pos_to_cell(self,pos):
        cell_pos_x = pos[0] - self.origin[0]
        cell_pos_y = pos[1] - self.origin[1]

        if (cell_pos_x < 0 or cell_pos_y < 0):
            return None
        
        cell_x = cell_pos_x // self.size
        cell_y = cell_pos_y // self.size

        if (cell_x >= self.width or cell_y >= self.height):
            return None

        return (cell_x, cell_y)