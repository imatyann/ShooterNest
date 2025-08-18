import pygame
from . import settings

class Piece:

    def __init__(self, color, current, radius, width_color):
        self.color = color
        self.current = current
        self.radius = radius
        self.width_color = width_color
    
    def draw(self, screen, board_square_size, origin):
        pygame.draw.circle(screen, 
                           self.color, 
                           (origin[0] + self.current[0]*board_square_size + board_square_size/2, 
                            origin[1] + self.current[1]*board_square_size + board_square_size/2), 
                           self.radius,
                           )
        pygame.draw.circle(screen, 
                           self.width_color, 
                           (origin[0] + self.current[0]*board_square_size + board_square_size/2, 
                            origin[1] + self.current[1]*board_square_size + board_square_size/2), 
                           self.radius,
                           width = 1)