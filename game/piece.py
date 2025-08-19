import pygame
import math

from . import settings

class Piece:

    def __init__(self, color, current, radius, width_color):
        self.color = color
        self.current = current
        self.radius = radius
        self.width_color = width_color
    
    def center_pos(self,origin, board_square_size):
        return (
            origin[0] + self.current[0] * board_square_size + board_square_size/2,
            origin[1] + self.current[1] * board_square_size + board_square_size/2,
            )

    def draw(self, screen, board_square_size, origin):
        pygame.draw.circle(screen, 
                           self.color, 
                           self.center_pos(origin,board_square_size), 
                           self.radius,
                           )
        pygame.draw.circle(screen, 
                           self.width_color, 
                           self.center_pos(origin,board_square_size),
                           self.radius,
                           width = 1)
        
    def move(self, target):
        self.current = target

    def tatch(self, pos, origin, board_square_size):
        if math.hypot(pos[0] - self.center_pos(origin, board_square_size)[0], pos[1] - self.center_pos(origin, board_square_size)[1]) < self.radius:        
            return True
        else:
            return False        