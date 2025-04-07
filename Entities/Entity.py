import pygame
from Config import Config

class Entity:
  @staticmethod
  def getRealCoordinates(coordinates, size):
    x, y = coordinates
    realX = x * Config.p_height + Config.p_height * 0.5 - size * 0.5 
    realY = y * Config.p_width + Config.p_width * 0.5 - size * 0.5
    return (realX, realY)

  def draw(self): # vẽ entity lên màn hình
    pass
