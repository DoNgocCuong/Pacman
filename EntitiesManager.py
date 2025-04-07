import pygame
from Entities import *

class EntitiesManager:
    def __init__(self):
        self.maze = Maze()
        self.pacman = Pacman()
        self.orangeGhost = OrangeGhost()
        self.redGhost = RedGhost()
        self.pinkGhost = PinkGhost()
        self.blueGhost = BlueGhost()
        self.life = Life()
        self.score = Score()
    
    def reset(self):
        self.pacman.reset()
        self.maze.reset()
        self.redGhost.reset()
        self.orangeGhost.reset()
        self.pinkGhost.reset()
        self.blueGhost.reset()
