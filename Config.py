import os
import pygame

current_dir = os.path.dirname(__file__)  # Lấy đường dẫn hiện tại của file Config.py
icon_path = os.path.join(current_dir, "Assets", "icon.jpg")
iconImage = pygame.image.load(icon_path)


pygame.mixer.init()

class Config:
  flicker = False
  running = True
  score = 0 #max score without powerup: 2500 (1: 10, 2: 20) -> 2500 + 50 * 4 * 4 = 3300 (max score with powerup)
  life = 3
  normalDots = 0 # 242
  powerupDots = 0 # 4
  KeyMovePacman = None
  width = 800
  height = 800
  p_width = 800/30 
  p_height = 750//32
  screen = pygame.display.set_mode([width, height])
  fps = 60 #600
  counter = 0
  prevkeyboard = (0, 0)

class Mode:
  CHASING = 0
  POWER_UP = 1
  mode = CHASING
  powerupTime = 0
  powerupTimeLimit = 60 * 8

  DEAD = 3
  BlueGhost = CHASING
  PinkGhost = CHASING
  OrangeGhost = CHASING
  RedGhost = CHASING

class Object:
  PACMAN_SIZE = 35
  BLUE_GHOST_SIZE = 35
  PINK_GHOST_SIZE = 35
  RED_GHOST_SIZE = 35
  ORANGE_GHOST_SIZE = 35  
  POWER_UP_SIZE = 35
  HEART_SIZE = 35
  PACMAN_DIRX = 0
  PACMAN_DIRY = 0
  PACMAN_DRAWX = 0
  PACMAN_DRAWY = 0
  
  pacmanX = 24
  pacmanY = 14
  blueGhostX = 16
  blueGhostY = 15
  pinkGhostX = 16
  pinkGhostY = 13
  redGhostX = 15
  redGhostY = 15
  orangeGhostX = 15
  orangeGhostY = 13

  realPacmanX = 0
  realPacmanY = 0
  realBlueGhostX = 0
  realBlueGhostY = 0
  realPinkGhostX = 0
  realPinkGhostY = 0
  realRedGhostX = 0
  realRedGhostY = 0
  realOrangeGhostX = 0
  realOrangeGhostY = 0

  
class Color:
  color_wall = 'blue'
  color_food = 'white'
  color_bg = 'black'
  color_fence = 'white'
  color_text = 'white'

class Material:
  iconImage = pygame.image.load("Assets/icon.jpg")
  BlueGhostImage = pygame.transform.scale(pygame.image.load("Assets/ghost_images/blue.png"), (Object.BLUE_GHOST_SIZE, Object.BLUE_GHOST_SIZE))
  RedGhostImage = pygame.transform.scale(pygame.image.load("Assets/ghost_images/red.png"), (Object.RED_GHOST_SIZE, Object.RED_GHOST_SIZE))
  PinkGhostImage = pygame.transform.scale(pygame.image.load("Assets/ghost_images/pink.png"), (Object.PINK_GHOST_SIZE, Object.PINK_GHOST_SIZE))
  OrangeGhostImage = pygame.transform.scale(pygame.image.load("Assets/ghost_images/orange.png"), (Object.ORANGE_GHOST_SIZE, Object.ORANGE_GHOST_SIZE))
  DeadGhostImage = pygame.transform.scale(pygame.image.load("Assets/ghost_images/dead.png"), (Config.p_height, Config.p_width))
  PowerupImage = pygame.transform.scale(pygame.image.load("Assets/ghost_images/powerup.png"), (Object.POWER_UP_SIZE, Object.POWER_UP_SIZE))
  Pacman1Image = pygame.transform.scale(pygame.image.load("Assets/player_images/1.png"), (Object.PACMAN_SIZE, Object.PACMAN_SIZE))
  Pacman2Image = pygame.transform.scale(pygame.image.load("Assets/player_images/2.png"), (Object.PACMAN_SIZE, Object.PACMAN_SIZE))
  Pacman3Image = pygame.transform.scale(pygame.image.load("Assets/player_images/3.png"), (Object.PACMAN_SIZE, Object.PACMAN_SIZE))
  Pacman4Image = pygame.transform.scale(pygame.image.load("Assets/player_images/4.png"), (Object.PACMAN_SIZE, Object.PACMAN_SIZE))
  HeartImage = pygame.transform.scale(pygame.image.load("Assets/player_images/heart.png"), (Object.HEART_SIZE, Object.HEART_SIZE))
  
class Board:
# 0 = empty black rectangle, 1 = dot, 2 = big dot, 3 = vertical line,
# 4 = horizontal line, 5 = top right, 6 = top left, 7 = bot left, 8 = bot right
# 9 = gate
  PACMAN = 50
  BLUE_GHOST = 60
  PINK_GHOST = 61
  RED_GHOST = 62
  ORANGE_GHOST = 63

  ROWS = 33
  COLS = 30
  BLANK = 0
  initMaze = [
[6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
[3, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 2, 3, 0, 0, 3, 1, 3, 0, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 0, 3, 1, 3, 0, 0, 3, 2, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 7, 4, 4, 4, 4, 5, 1, 3, 7, 4, 4, 5, 0, 3, 3, 0, 6, 4, 4, 8, 3, 1, 6, 4, 4, 4, 4, 8, 3],
[3, 99, 99, 99, 99, 99, 3, 1, 3, 6, 4, 4, 8, 0, 7, 8, 0, 7, 4, 4, 5, 3, 1, 3, 99, 99, 99, 99, 99, 3],
[3, 99, 99, 99, 99, 99, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 99, 99, 99, 99, 99, 3],
[8, 99, 99, 99, 99, 99, 3, 1, 3, 3, 0, 6, 4, 4, 9, 9, 4, 4, 5, 0, 3, 3, 1, 3, 99, 99, 99, 99, 99, 7],
[4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4],
[5, 99, 99, 99, 99, 99, 3, 1, 3, 3, 0, 7, 4, 4, 4, 4, 4, 4, 8, 0, 3, 3, 1, 3, 99, 99, 99, 99, 99, 6],
[3, 99, 99, 99, 99, 99, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 99, 99, 99, 99, 99, 3],
[3, 99, 99, 99, 99, 99, 3, 1, 3, 3, 0, 6, 4, 4, 4, 4, 4, 4, 5, 0, 3, 3, 1, 3, 99, 99, 99, 99, 99, 3],
[3, 6, 4, 4, 4, 4, 8, 1, 7, 8, 0, 7, 4, 4, 5, 6, 4, 4, 8, 0, 7, 8, 1, 7, 4, 4, 4, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 5, 3, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 3, 6, 4, 8, 1, 3, 3],
[3, 3, 2, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 2, 3, 3],
[3, 7, 4, 5, 1, 3, 3, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 3, 3, 1, 6, 4, 8, 3],
[3, 6, 4, 8, 1, 7, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 8, 1, 7, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 4, 4, 8, 7, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 8, 7, 4, 4, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 3],
[7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8]
]  
  maze = []
  coordinates = []
  nodes = {(21, 16), (27, 4), (27, 13), (14, 13), (2, 2), (6, 2), (15, 14), (16, 13), (18, 10), (18, 19), (30, 2), (14, 15), (9, 10), (9, 19), (24, 10), (15, 7), (24, 19), (15, 16), (6, 13), (16, 15), (21, 2), (14, 17), (30, 13), (15, 0), (16, 17), (2, 27), (12, 13), (6, 27), (27, 22), (30, 27), (12, 15), (14, 12), (21, 27), (9, 7), (9, 16), (24, 7), (24, 16), (15, 13), (2, 13), (16, 12), (24, 25), (2, 22), (6, 22), (14, 14), (16, 14), (21, 13), (12, 10), (21, 22), (9, 2), (12, 19), (14, 16), (27, 10), (24, 2), (27, 19), (16, 16), (15, 29), (24, 4), (6, 10), (15, 22), (6, 19), (12, 14), (9, 27), (15, 15), (21, 10), (24, 27), (21, 19), (12, 16), (27, 7), (27, 16), (27, 25), (15, 17), (9, 13), (27, 27), (2, 7), (9, 22), (2, 16), (24, 13), (15, 10), (6, 7), (24, 22), (15, 19), (6, 16), (27, 2), (30, 16), (15, 12), (21, 7)}

def setup():
  # set up map cho maze
  Board.maze = [row[:] for row in Board.initMaze]

  # set up coordinates
  Board.coordinates = [[Board.BLANK for _ in range(Board.COLS)] for _ in range(Board.ROWS)] # tạo ma trận cols x rows với các ô có giá trị 0

  Board.coordinates[Object.pacmanX][Object.pacmanY] = Board.PACMAN
  Board.coordinates[Object.blueGhostX][Object.blueGhostY] = Board.BLUE_GHOST
  Board.coordinates[Object.pinkGhostX][Object.pinkGhostY] = Board.PINK_GHOST
  Board.coordinates[Object.redGhostX][Object.redGhostY] = Board.RED_GHOST
  Board.coordinates[Object.orangeGhostX][Object.orangeGhostY] = Board.ORANGE_GHOST

  Object.realPacmanX = Object.pacmanX * Config.p_height + Config.p_height * 0.5 - Object.PACMAN_SIZE * 0.5 
  Object.realPacmanY = Object.pacmanY * Config.p_width + Config.p_width * 0.5 - Object.PACMAN_SIZE * 0.5
  Object.realBlueGhostX = Object.blueGhostX * Config.p_height + Config.p_height * 0.5 - Object.BLUE_GHOST_SIZE * 0.5 
  Object.realBlueGhostY = Object.blueGhostY * Config.p_width + Config.p_width * 0.5 - Object.BLUE_GHOST_SIZE * 0.5
  Object.realPinkGhostX = Object.pinkGhostX * Config.p_height + Config.p_height * 0.5 - Object.PINK_GHOST_SIZE * 0.5 
  Object.realPinkGhostY = Object.pinkGhostY * Config.p_width + Config.p_width * 0.5 - Object.PINK_GHOST_SIZE * 0.5
  Object.realRedGhostX = Object.redGhostX * Config.p_height + Config.p_height * 0.5 - Object.RED_GHOST_SIZE * 0.5 
  Object.realRedGhostY = Object.redGhostY * Config.p_width + Config.p_width * 0.5 - Object.RED_GHOST_SIZE * 0.5
  Object.realOrangeGhostX = Object.orangeGhostX * Config.p_height + Config.p_height * 0.5 - Object.ORANGE_GHOST_SIZE * 0.5 
  Object.realOrangeGhostY = Object.orangeGhostY * Config.p_width + Config.p_width * 0.5 - Object.ORANGE_GHOST_SIZE * 0.5

class Sounds:
  dramatic_theme_music_sound = pygame.mixer.Sound("Assets/sounds/dramatic_theme_music.mp3")  # Âm thanh nhạc nền trong game
  pacman_eat_dot_sound = pygame.mixer.Sound("Assets/sounds/pacman_eating_dots.mp3")  # Âm thanh khi ăn
  ghost_move_sound = pygame.mixer.Sound("Assets/sounds/ghost_move.mp3")  # Âm thanh ma di chuyển
  pacman_death_sound = pygame.mixer.Sound("Assets/sounds/pacman_death.wav")
  beginning_game_sound = pygame.mixer.Sound("Assets/sounds/pacman_beginning.wav")
  ghost_move_powerup_sound = pygame.mixer.Sound("Assets/sounds/ghost_move_powerup.mp3")
  pacman_eat_ghost_sound = pygame.mixer.Sound("Assets/sounds/pacman_eat_ghost.mp3")
  hover_sound = pygame.mixer.Sound("Assets/sounds/hover.mp3")
  click_sound = pygame.mixer.Sound("Assets/sounds/click.wav")
  win_sound = pygame.mixer.Sound("Assets/sounds/win.mp3")
  lose_sound = pygame.mixer.Sound("Assets/sounds/lose.wav")

  def beginning_game(self):
    self.beginning_game_sound.play()

  def pacman_eat_dot(self):
    self.pacman_eat_dot_sound.play()

  def pacman_death(self):
    self.pacman_death_sound.play()
  
  def ghost_move(self):
    self.ghost_move_sound.play()

  def dramatic_theme_music(self):
    self.dramatic_theme_music_sound.play().set_volume(0.1)
