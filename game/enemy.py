import pygame
import random

class Enemy:

    def __init__(self, color, current, radius, width_color, can_move, move_tick,alive):
        self.color = color
        self.current = current
        self.radius = radius
        self.width_color = width_color
        self.can_move = can_move
        self.move_tick = move_tick
        self.alive = alive


    def center_pos(self,origin, board_square_size):
        return (
            origin[0] + self.current[0] * board_square_size + board_square_size/2,
            origin[1] + self.current[1] * board_square_size + board_square_size/2,
            )
    
    def draw(self, screen, board_square_size, origin):
        if self.alive:
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

    def can_go_cells(self,board):
        can_move = self.can_move
        result = set()
        for cell in can_move:
            next_cell = (self.current[0] + cell[0], self.current[1] + cell[1])
            if not ((next_cell[0] <= -1) or (next_cell[1] <= -1) or (next_cell[0] >= board.width) or (next_cell[1] >= board.height)):
                result.add((self.current[0] + cell[0], self.current[1] + cell[1]))
        return result
    
    def choose_random_cell(self,can_go_cells):
        if can_go_cells:
            target = random.choice(list(can_go_cells))
            return target
    
    def hit(self):
        self.alive = False