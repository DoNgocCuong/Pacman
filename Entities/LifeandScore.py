from Config import Color, Config, Material
from math import pi
import copy
import pygame

pygame.init()

class Life:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.x = 160
        self.y = 755
        
    def draw(self):
        for i in range(Config.life):
            Config.screen.blit(Material.HeartImage, (self.x + 40 * i, self.y))

class Score:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        
    def draw(self):
        text = self.font.render("Score: " + str(Config.score), 1, Color.color_text)
        Config.screen.blit(text, (20, 760))
        
