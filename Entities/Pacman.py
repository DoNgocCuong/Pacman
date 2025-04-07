from .Entity import Entity
from Config import Config, Material, Object, Board, Mode, Sounds
import pygame

class Pacman(Entity):
  def __init__(self):
    self.PacmanImages = [Material.Pacman1Image, Material.Pacman2Image, Material.Pacman3Image, Material.Pacman4Image]
  
  def draw(self):
    realX = Object.realPacmanX
    realY = Object.realPacmanY
    Config.screen.blit(Material.Pacman1Image, (realY, realX))

  def picperdir(self, picture, direction, realX, realY):
    if direction == (0, 1) or direction == (0, 0):
          Config.screen.blit(picture, (realY, realX))
    elif direction == (0, -1):
        Config.screen.blit(pygame.transform.flip(picture, True, False), (realY, realX))  
    elif direction == (-1, 0):
        Config.screen.blit(pygame.transform.rotate(picture, 90),(realY, realX))
    elif direction == (1, 0):
        Config.screen.blit(pygame.transform.rotate(picture, 270), (realY, realX))
        
  def drawdir(self, direction):
    realX = Object.realPacmanX
    realY = Object.realPacmanY
    if (Board.maze[Object.pacmanX][Object.pacmanY] != 0):
      self.picperdir(self.PacmanImages[Config.counter // 5], direction, realX, realY)
    else:
      self.picperdir(Material.Pacman2Image, direction, realX, realY)    
        
  def setupdrawdir(self):
    direction = Object.PACMAN_DIRX, Object.PACMAN_DIRY

    if direction != (0, 0):
        Object.PACMAN_DRAWX, Object.PACMAN_DRAWY = direction
        self.drawdir(direction)
    else:
      direction = Object.PACMAN_DRAWX, Object.PACMAN_DRAWY
      self.drawdir(direction)
        
  def keyboardHandle(self):
    keys = Config.KeyMovePacman

    if keys is None:  
      return (0, 0)
    elif keys == pygame.K_UP:
      return (-1, 0)
    elif keys == pygame.K_DOWN:
      return (1, 0)
    elif keys == pygame.K_LEFT:
      return (0, -1)
    elif keys ==pygame.K_RIGHT:
      return (0, 1)
  
    return (0, 0)
  
  def isValidPos(self, x, y):
      if 0 <= x < Board.ROWS and 0 <= y < Board.COLS:
          if (Board.maze[x][y] < 3 or Board.maze[x][y] == 9) \
            and ((x, y) != (Object.blueGhostX, Object.blueGhostY) or Mode.BlueGhost != Mode.CHASING) \
            and ((x, y) != (Object.pinkGhostX, Object.pinkGhostY) or Mode.PinkGhost != Mode.CHASING) \
            and ((x, y) != (Object.redGhostX, Object.redGhostY) or Mode.RedGhost != Mode.CHASING) \
            and ((x, y) != (Object.orangeGhostX, Object.orangeGhostY) or Mode.OrangeGhost != Mode.CHASING):
              return True
      return False
    
  def getTargetPos(self):
    (dx, dy) = self.keyboardHandle()
    oldx, oldy = Object.pacmanX + Object.PACMAN_DIRX, Object.pacmanY + Object.PACMAN_DIRY
    
    if ((dx, dy) != (0,0)):
      Config.prevkeyboard = dx, dy

      if (Config.prevkeyboard) != (0, 0):
        newx, newy = Object.pacmanX + dx, Object.pacmanY + dy
        if self.isValidPos(newx, newy):
          Object.PACMAN_DIRX, Object.PACMAN_DIRY = (dx, dy)
          return (newx, newy)
        
      if self.isValidPos(oldx, oldy):
          return (oldx, oldy)
      else:
          return (Object.pacmanX, Object.pacmanY)
        
    else:
      (dx, dy) = Config.prevkeyboard

      if (Config.prevkeyboard) != (0, 0):
        newx, newy = Object.pacmanX + dx, Object.pacmanY + dy
        if self.isValidPos(newx, newy):
          Object.PACMAN_DIRX, Object.PACMAN_DIRY = (dx, dy)
          return (newx, newy)
        
      if self.isValidPos(oldx, oldy):
          return (oldx, oldy)
      else:
          return (Object.pacmanX, Object.pacmanY)
      
    
    
  def move(self):
    x, y = Object.pacmanX, Object.pacmanY
    if Board.maze[x][y] in (1, 2):
      Sounds.pacman_eat_dot_sound.set_volume(0.3)
    targetX, targetY = Entity.getRealCoordinates((x, y), Object.PACMAN_SIZE) 
    realX, realY = Object.realPacmanX, Object.realPacmanY

    dx, dy = (targetX - realX), (targetY - realY)
    sX = Config.p_height / 15
    sY = Config.p_width / 15
  
    if abs(dx) >= sX:
      realX = realX + dx / abs(dx) * sX
    else:
      realX = targetX
    
    if (abs(dy)) == 728:
      realY = 0
      realX = 15 * Config.p_height + Config.p_height * 0.5 - Object.PACMAN_SIZE * 0.5
    elif abs(dy) >= sY:
      realY = realY + dy / abs(dy) * sY
    else:
      realY = targetY

    Object.realPacmanX = realX
    Object.realPacmanY = realY
  
  def updatePos(self):
    oldX, oldY = Object.pacmanX, Object.pacmanY
    if (oldX, oldY) == (15, 0) and Config.KeyMovePacman == pygame.K_LEFT:
      Board.coordinates[oldX][oldY] = Board.BLANK
      Board.coordinates[15][29] = Board.PACMAN
      Object.pacmanX, Object.pacmanY = 15, 29
      (Object.realPacmanX, Object.realPacmanY) = Entity.getRealCoordinates((15, 30), Object.PACMAN_SIZE)
      return
    elif (oldX, oldY) == (15, 29) and Config.KeyMovePacman == pygame.K_RIGHT:
      Board.coordinates[oldX][oldY] = Board.BLANK
      Board.coordinates[15][0] = Board.PACMAN
      Object.pacmanX, Object.pacmanY = 15, 0
      (Object.realPacmanX, Object.realPacmanY) = Entity.getRealCoordinates((15, -1), Object.PACMAN_SIZE)
      return
    else:
      if Board.maze[oldX][oldY] == 1: # normal dot
        Board.maze[oldX][oldY] = 0
        Config.score += 10
        Config.normalDots -= 1

      elif Board.maze[oldX][oldY] == 2: # powerup dot
        Board.maze[oldX][oldY] = 0
        Config.score += 20
        Config.powerupDots -= 1
        Mode.mode = Mode.POWER_UP
        Mode.powerupTime += Mode.powerupTimeLimit  
        Mode.BlueGhost = Mode.POWER_UP if Mode.BlueGhost != Mode.DEAD else Mode.DEAD    
        Mode.PinkGhost = Mode.POWER_UP if Mode.PinkGhost != Mode.DEAD else Mode.DEAD       
        Mode.RedGhost = Mode.POWER_UP if Mode.RedGhost != Mode.DEAD else Mode.DEAD   
        Mode.OrangeGhost = Mode.POWER_UP  if Mode.OrangeGhost != Mode.DEAD else Mode.DEAD    

      elif Board.maze[oldX][oldY] == 0:
        Sounds.pacman_eat_dot_sound.set_volume(0)
        
      targetPos = self.getTargetPos()
    
      if targetPos:
          targetX, targetY = targetPos
          newX, newY = oldX, oldY
          
          if targetX != oldX:
              newX += 1 if targetX > oldX else -1 
          if targetY != oldY:
              newY += 1 if targetY > oldY else -1 


          Board.coordinates[oldX][oldY] = Board.BLANK
          Board.coordinates[newX][newY] = Board.PACMAN
          Object.pacmanX, Object.pacmanY = newX, newY