import pygame
from . import settings

class Board:
    def __init__(self, width, height, color, origin, size, highlight_color,highlight_edge_color,attacked_color):
        self.width = width
        self.height = height
        self.color = color
        self.origin = origin
        self.size = size
        self.highlight_color = highlight_color
        self.highlight_edge_color = highlight_edge_color
        self.attacked_color = attacked_color


    def draw(self,screen,highlight_cells = None,attacked_cells = None,state = "playing"):
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
        for cell in highlight_cells:
            overlay = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.be_highlight_cell(cell,screen,overlay)
            
        for cell in attacked_cells:
            self.be_attacked_cell(cell,screen)

        if state == "gameover":
            # ここにGAMEOVER処理を挿入
            # screen.fill(self.gameover_color)
            pass
            
    def be_highlight_cell(self,cell,screen,overlay):
        x = self.origin[0] + cell[0] * self.size
        y = self.origin[1] + cell[1] * self.size
        overlay.fill(self.highlight_color)
        screen.blit(overlay, (x, y))
        pygame.draw.rect(screen,self.highlight_edge_color,(x,y,self.size, self.size),width=2)
    
    def be_attacked_cell(self,cell,screen):
        pygame.draw.rect(screen,
                    self.attacked_color,
                    (self.origin[0] + cell[0] * self.size,
                    self.origin[1] + cell[1] * self.size, 
                    self.size, 
                    self.size)
                    )
        pygame.draw.rect(screen,
                    (0,0,0),
                    (self.origin[0] + cell[0] * self.size,
                    self.origin[1] + cell[1] * self.size, 
                    self.size, 
                    self.size,),
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