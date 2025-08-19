import pygame
import math

from . import settings

class Piece:

    def __init__(self, color, current, radius, width_color, selected_color):
        self.color = color
        self.current = current
        self.radius = radius
        self.width_color = width_color
        self.selected_color = selected_color
    
    def center_pos(self,origin, board_square_size):
        return (
            origin[0] + self.current[0] * board_square_size + board_square_size/2,
            origin[1] + self.current[1] * board_square_size + board_square_size/2,
            )

    def draw(self, screen, board_square_size, origin, selected_piece):
        if selected_piece != self:
            current_width_color = self.color
            current_radius = self.radius
        else:
            current_width_color = self.selected_color
            current_radius = self.radius - 1

        pygame.draw.circle(screen, 
                           current_width_color, 
                           self.center_pos(origin,board_square_size), 
                           current_radius,
                           )
        pygame.draw.circle(screen, 
                        self.width_color, 
                        self.center_pos(origin,board_square_size),
                        current_radius,
                        width = 1)
        
    def move(self, target):
        self.current = target

    def tatch(self, pos, origin, board_square_size):
        if math.hypot(pos[0] - self.center_pos(origin, board_square_size)[0], pos[1] - self.center_pos(origin, board_square_size)[1]) < self.radius:        
            return True
        else:
            return False
    
    # def clicked(self,selected_piece):
    #     if selected_piece == self:
    #         self.is_selected = True
    #     else:
    #         self.is_selected = False