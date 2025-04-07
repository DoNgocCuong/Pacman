from Levels import *
from Config import setup, Sounds, Material
from Menu import Menu
import pygame

def main():
  Sounds.beginning_game_sound.play()
  setup()
  pygame.init()
  pygame.display.set_caption("Pacman")
  pygame.display.set_icon(Material.iconImage)
  menu = Menu()
  menu.execute()

if __name__ == "__main__":
  main()  