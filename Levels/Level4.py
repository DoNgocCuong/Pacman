from Entities.Entity import Entity
from EntitiesManager import EntitiesManager as EM
from Config import Config, Object, Sounds, Board
from Levels.ExperimentBox import ExperimentBox
import pygame
import time
import tracemalloc #de lay bo nho
import math
import heapq
from collections import deque
from queue import PriorityQueue

# testcases: (ghost, pacman)
testcases = [((16, 13), (27, 18)),
             ((21, 3), (4, 13)), 
             ((27, 3), (13, 22)),
             ((6, 2), (29, 27)), 
             ((30, 27), (9, 4))]
testcaseID = 0

quit = False
start = False

class Level4:
  def __init__(self):
    pass

  def setup(self):
    # Setup tọa độ ma trận
    Object.redGhostX, Object.redGhostY = testcases[testcaseID][0]
    Object.pacmanX, Object.pacmanY = testcases[testcaseID][1]
    Object.pinkGhostX, Object.pinkGhostY = -1, -1
    Object.blueGhostX, Object.blueGhostY = -1, -1
    Object.orangeGhostX, Object.orangeGhostY = -1, -1

    Board.maze = [row[:] for row in Board.initMaze]

    # Setup tọa độ thực
    (Object.realPacmanX, Object.realPacmanY) = Entity.getRealCoordinates((Object.pacmanX, Object.pacmanY), Object.PACMAN_SIZE)
    (Object.realRedGhostX, Object.realRedGhostY) = Entity.getRealCoordinates((Object.redGhostX, Object.redGhostY), Object.RED_GHOST_SIZE)

    # Setup ma trận Coordinates 
    Board.coordinates[Object.redGhostX][Object.redGhostY] = Board.RED_GHOST
    Board.coordinates[Object.pacmanX][Object.pacmanY] = Board.PACMAN 

    for i in range (len(Board.coordinates)): # Chỉ giữ lại giá trị Pacman, RedGhost trong ma trận Coordinates, các giá trị còn lại bỏ
      for j in range (len(Board.coordinates[0])):
        if (i, j) not in ((Object.redGhostX, Object.redGhostY), (Object.pacmanX, Object.pacmanY)):
          Board.coordinates[i][j] = Board.BLANK
  # hàm này viết trả hết tất cả các đường đi
  def reconstruct_path(self, came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

  def heuristic(self, ghostX, ghostY):
    return abs(ghostX - Object.pacmanX) + abs(ghostY - Object.pacmanY)
  def reconstruct_path(self, came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
  def isValidPos(self, x, y):
        if 0 <= x < Board.ROWS and 0 <= y < Board.COLS:
            if (Board.maze[x][y] < 3 or Board.maze[x][y] == 9) and Board.coordinates[x][y] in (Board.BLANK, Board.PACMAN):
                return True
        return False

  def AStarFindAll(self, ghost, pacman):
    start = ghost
    goal = pacman

    open_set = PriorityQueue()
    open_set.put((0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: self.heuristic(*start)}

    visited = set()

    DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    PATH_LIMIT = 100

    while not open_set.empty():
        _, current = open_set.get()
        visited.add(current)

        if current == goal or len(came_from) > PATH_LIMIT:
            path = self.reconstruct_path(came_from, current)
            return path, len(visited)

        for dx, dy in DIRECTIONS:
            nx, ny = current

            # Di chuyển thẳng theo hướng đó đến khi gặp node
            while True:
                nx += dx
                ny += dy
                if not self.isValidPos(nx, ny):
                    break
                if (nx, ny) in Board.nodes or (nx, ny) == goal:
                    neighbor = (nx, ny)

                    if neighbor in visited:
                        break

                    # Tránh va chạm ghost khác
                    if neighbor in [(Object.pinkGhostX, Object.pinkGhostY),
                                    (Object.orangeGhostX, Object.orangeGhostY),
                                    (Object.blueGhostX, Object.blueGhostY)]:
                        break

                    tentative_g = g_score[current] + abs(current[0] - neighbor[0]) + abs(current[1] - neighbor[1])

                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f = tentative_g + self.heuristic(*neighbor)
                        f_score[neighbor] = f
                        open_set.put((f, neighbor))
                    break  # chỉ xét 1 node trong mỗi hướng (đầu tiên gặp)
    return None, len(visited)


    
  def updatePos(self):
    oldX, oldY = Object.redGhostX, Object.redGhostY
    path, numOfExpendedNodes = self.AStarFindAll((Object.redGhostX, Object.redGhostY), (Object.pacmanX, Object.pacmanY))
    if path:
      targetPos=path[0]
      if targetPos:
        targetX, targetY = targetPos

        newX, newY = oldX, oldY
        if targetX != oldX:
          newX += (targetX - oldX) // abs(targetX - oldX) 
        if targetY != oldY:
          newY += (targetY - oldY) // abs(targetY - oldY)

        Board.coordinates[oldX][oldY] = Board.BLANK
        Board.coordinates[newX][newY] = Board.RED_GHOST

        Object.redGhostX = newX
        Object.redGhostY = newY
  def get_volume(self, ghost_x, ghost_y, pac_x, pac_y, max_distance=15):
    distance = math.sqrt((ghost_x - pac_x) ** 2 + (ghost_y - pac_y) ** 2)  
    volume = max(0.0, 1 - (distance / max_distance))  # 0.1 là âm lượng nhỏ nhất, 1 là lớn nhất
    return min(1.0, max(0.0, volume))  # Giới hạn từ 0.0 đến 1.0
  
  def execute(self):
    global quit, start

    quit = False
    start = False

    font = pygame.font.Font("Assets/fonts/arial.ttf", 20)
    shortkey = font.render("ESC: Menu  Q: thoát", True, (255, 0,0))

    while Config.running and not quit:
      self.setup()

      Sounds().dramatic_theme_music()
      ghost_move_sound = pygame.mixer.Sound("Assets/sounds/ghost_move.mp3")

      clock = pygame.time.Clock()

      # Bắt đầu đo bộ nhớ
      tracemalloc.start()

      start_time = time.time()  # Lấy thời gian bắt đầu
      path, numOfExpendedNodes = self.AStarFindAll((Object.redGhostX, Object.redGhostY), (Object.pacmanX, Object.pacmanY))
      end_time = time.time()    # Lấy thời gian kết thúc

      # Lấy kết quả peak memory usage
      current, peak = tracemalloc.get_traced_memory()
      # Dừng đo
      tracemalloc.stop()
      
      step = 0
      countFrames = 0

      while Config.running:

        Config.screen.fill('black')

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            ghost_move_sound.stop()
            Sounds.dramatic_theme_music_sound.stop()
            Config.running = False
            return
          elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
              ghost_move_sound.stop()
              Sounds.click_sound.play()
              Sounds.dramatic_theme_music_sound.stop()
              quit = True
              return
            if event.key == pygame.K_q:
              ghost_move_sound.stop()
              Sounds.click_sound.play()
              Sounds.dramatic_theme_music_sound.stop()
              Config.running = False
              return
            if event.key == pygame.K_SPACE:
              if not start:
                ghost_move_sound.play(loops=-1)  # Lặp vô hạn
              start = True

        EM().maze.draw()

        if start:
          if countFrames % 15 == 0:
            targetX, targetY = path[step]
            curX, curY = Object.redGhostX, Object.redGhostY
           
            if (curX, curY) == (targetX, targetY):
              if step < len(path) - 1:
                step += 1
                targetX, targetY = path[step]

            if (curX, curY) != (targetX, targetY):
              newX, newY = curX, curY
              if targetX != curX:
                newX += (targetX - curX) // abs(targetX - curX) 
              if targetY != curY:
                newY += (targetY - curY) // abs(targetY - curY)
              Object.redGhostX = newX
              Object.redGhostY = newY
          EM().redGhost.move()

        EM().pacman.draw()
        EM().redGhost.draw()

        if not start:
          overlay = pygame.Surface((Config.width, Config.height))
          overlay.set_alpha(180)  # Độ trong suốt (0: trong suốt hoàn toàn, 255: không trong suốt)
          overlay.fill((0, 0, 0))  # Màu đen
          Config.screen.blit(overlay, (0, 0))

          color = (255, 255, 255 - countFrames % 30 * 8)
          labelFont = pygame.font.Font("Assets/fonts/arial.ttf", 20)
          space_to_start = labelFont.render("SPACE để bắt đầu trò chơi", True, color)
          Config.screen.blit(space_to_start, (Config.width / 2 - 130, Config.height / 2 - 50))

        Config.screen.blit(shortkey, (580, 800 - 30))

        pygame.display.flip()
        clock.tick(Config.fps)
        countFrames += 1

        if (Object.redGhostX, Object.redGhostY) == (Object.pacmanX, Object.pacmanY):
          ghost_move_sound.stop()
          Sounds.dramatic_theme_music_sound.stop()
          break
      
      Sounds.lose_sound.play()
      
      start = False

      algorithm = "A*"
      search_time = end_time - start_time
      memory_usage = peak / (2 ** 20)
      num_expanded_nodes = numOfExpendedNodes
              
      Config.screen.blit(shortkey, (580, 800 - 30))
            
      while Config.running:
        nextTestcase = ExperimentBox().showResultBoard(algorithm, search_time, memory_usage, num_expanded_nodes)
        if nextTestcase == -1:
          quit = True
          break
        elif nextTestcase != None:
          global testcaseID
          testcaseID = nextTestcase
          break