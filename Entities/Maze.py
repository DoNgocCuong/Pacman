from Config import Color, Config, Board
from math import pi
import copy
import pygame

pygame.init()

class Maze:
    def __init__(self):
        self.map = copy.deepcopy(Board.maze)

    def draw(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                
                cell = self.map[i][j]
                cx = j * Config.p_width + (0.5 * Config.p_width)
                cy = i * Config.p_height + (0.5 * Config.p_height)
                
                if cell == 1:
                    pygame.draw.circle(Config.screen, Color.color_food, (cx, cy), 4)
                    
                elif cell == 2 and not Config.flicker:
                    pygame.draw.circle(Config.screen, Color.color_food, (cx, cy), 10)
                    
                elif cell == 3:
                    pygame.draw.line(Config.screen, Color.color_wall, (cx, i * Config.p_height), (cx, i * Config.p_height + Config.p_height), 4)
                
                elif cell == 4:
                    pygame.draw.line(Config.screen, Color.color_wall, (j * Config.p_width, cy), (j * Config.p_width + Config.p_width, cy), 4)
                
                elif cell == 5:
                    pygame.draw.arc(Config.screen, Color.color_wall, [(j * Config.p_width - (Config.p_width * 0.4)) - 2, cy, Config.p_width, Config.p_height], 0, pi / 2, 4)
                
                elif cell == 6:
                    pygame.draw.arc(Config.screen, Color.color_wall, [(j * Config.p_width + (Config.p_width * 0.5)), cy, Config.p_width, Config.p_height],pi / 2, pi, 4)
                
                elif cell == 7:
                    pygame.draw.arc(Config.screen, Color.color_wall, [(j * Config.p_width + (Config.p_width * 0.5)), (i * Config.p_height - (0.4 * Config.p_height)), Config.p_width, Config.p_height],pi, 3 * pi / 2, 4)
                
                elif cell == 8:
                    pygame.draw.arc(Config.screen, Color.color_wall, [(j * Config.p_width - (Config.p_width * 0.4)) - 2, (i * Config.p_height - (0.4 * Config.p_height)), Config.p_width, Config.p_height],3 * pi / 2, 2 * pi, 4)
                
                elif cell == 9:
                    pygame.draw.line(Config.screen, Color.color_fence,(j * Config.p_width, cy),(j * Config.p_width + Config.p_width, cy), 4)
