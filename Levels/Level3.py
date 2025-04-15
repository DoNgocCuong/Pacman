from EntitiesManager import EntitiesManager as EM
from Entities.Entity import Entity
from Config import Config, Object, Sounds, Board
from Levels.ExperimentBox import ExperimentBox
import pygame
import time
import tracemalloc #de lay bo nho
import math
import pygame
from collections import deque
import heapq

# testcases: (ghost, pacman)
testcases = [((16, 13), (24, 14)),
             ((21, 3), (15, 21)), 
             ((27, 3), (29, 27)),
             ((6, 2), (24, 26)), 
             ((30, 27), (4, 2))]
testcaseID = 0

quit = False
start = False

class Level3:
  def __init__(self):
    pass

  def setup(self):
    Object.orangeGhostX, Object.orangeGhostY = testcases[testcaseID][0]
    Object.pacmanX, Object.pacmanY = testcases[testcaseID][1]
    Object.pinkGhostX, Object.pinkGhostY = -1, -1
    Object.redGhostX, Object.redGhostY = -1, -1
    Object.blueGhostX, Object.blueGhostY = -1, -1

    Board.maze = [row[:] for row in Board.initMaze]  # Reset maze
    Board.coordinates = [[Board.BLANK for _ in range(Board.COLS)] for _ in range(Board.ROWS)]  # Reset coordinates

    # Setup coordinates
    Board.coordinates[Object.orangeGhostX][Object.orangeGhostY] = Board.ORANGE_GHOST
    Board.coordinates[Object.pacmanX][Object.pacmanY] = Board.PACMAN

    # Setup real coordinates
    Object.realPacmanX, Object.realPacmanY = Entity.getRealCoordinates((Object.pacmanX, Object.pacmanY), Object.PACMAN_SIZE)
    Object.realOrangeGhostX, Object.realOrangeGhostY = Entity.getRealCoordinates((Object.orangeGhostX, Object.orangeGhostY), Object.ORANGE_GHOST_SIZE)

    for i in range (len(Board.coordinates)): # Chỉ giữ lại giá trị Pacman, OrangeGhost trong ma trận Coordinates, các giá trị còn lại bỏ
      for j in range (len(Board.coordinates[0])):
        if (i, j) not in ((Object.orangeGhostX, Object.orangeGhostY), (Object.pacmanX, Object.pacmanY)):
            Board.coordinates[i][j] = Board.BLANK
  
  # hàm này viết trả hết tất cả các đường đi
  def UcsFindAll(self, ghost, pacman):
    start_x, start_y = ghost
    goal_x, goal_y = pacman
    
    # Use a more efficient tuple structure in the priority queue
    frontier = [(0, start_x, start_y, [])]  # (cost, x, y, path)
    heapq.heapify(frontier)
    
    visited = set()
    expanded_nodes = 0
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # Pre-compute maze dimensions to avoid repeated len() calls
    maze_rows = len(Board.maze)
    maze_cols = len(Board.maze[0])
    
    # Pre-compute wall values for faster checking
    wall_values = {3, 4, 5, 6, 7, 8}
    
    # Pre-compute other ghost positions for collision avoidance
    other_ghosts = {
        (Object.redGhostX, Object.redGhostY),
        (Object.pinkGhostX, Object.pinkGhostY),
        (Object.blueGhostX, Object.blueGhostY)
    }
    # Remove invalid ghost positions (-1, -1)
    other_ghosts = {pos for pos in other_ghosts if pos[0] >= 0 and pos[1] >= 0}
    
    while frontier:
        cost, current_x, current_y, path = heapq.heappop(frontier)
        expanded_nodes += 1
        
        # Check if we've reached the goal
        if (current_x, current_y) == (goal_x, goal_y):
            full_path = path + [(current_x, current_y)]
            return full_path, expanded_nodes
        
        # Skip if already visited
        if (current_x, current_y) in visited:
            continue
        
        visited.add((current_x, current_y))
        current_path = path + [(current_x, current_y)]
        
        # Process all valid neighbor positions
        for dx, dy in directions:
            next_x, next_y = current_x + dx, current_y + dy
            
            # Fast bounds and wall check
            if (0 <= next_x < maze_rows and 
                0 <= next_y < maze_cols and 
                Board.maze[next_x][next_y] not in wall_values and
                (next_x, next_y) not in visited):
                
                # Skip if position is occupied by another ghost
                if (next_x, next_y) in other_ghosts:
                    continue
                
                new_cost = cost + 1
                heapq.heappush(frontier, (new_cost, next_x, next_y, current_path))
    
    # No path found
    return [], expanded_nodes
  
  # def UCSFindOne(self, ghost, pacman):
  #   start_x, start_y = ghost
  #   goal_x, goal_y = pacman
    
  #   frontier = [(0, start_x, start_y, [])]  
  #   heapq.heapify(frontier)
    
  #   visited = set()
  #   directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
  #   while frontier:
  #       cost, current_x, current_y, path = heapq.heappop(frontier)
        
  #       if (current_x, current_y) == (goal_x, goal_y):
  #           if path:
  #               return path[0]
  #           return (current_x, current_y)
        
  #       if (current_x, current_y) in visited:
  #           continue
        
  #       visited.add((current_x, current_y))
        
  #       for dx, dy in directions:
  #           # Calculate next position clearly and separately
  #           next_x = current_x + dx
  #           next_y = current_y + dy
            
            
  #           # Move in straight lines until reaching an intersection or wall
  #           while (0 <= next_x < len(Board.maze) and 
  #                 0 <= next_y < len(Board.maze[0]) and 
  #                 Board.maze[next_x][next_y] not in [3, 4, 5, 6, 7, 8]):
                
  #               # Stop at nodes/intersections or the goal
  #               if (next_x, next_y) in Board.nodes or (next_x, next_y) == (goal_x, goal_y):
  #                   # Skip if occupied by another ghost
  #                   if (next_x, next_y) in [(Object.redGhostX, Object.redGhostY),
  #                                         (Object.pinkGhostX, Object.pinkGhostY),
  #                                         (Object.blueGhostX, Object.blueGhostY)]:
  #                       break
                        
  #                   if (next_x, next_y) not in visited:
  #                       new_cost = cost + abs(current_x - next_x) + abs(current_y - next_y)
  #                       new_path = path + [(current_x, current_y)]
  #                       heapq.heappush(frontier, (new_cost, next_x, next_y, new_path))
  #                   break
                
  #               # Keep moving in the same direction
  #               next_x += dx
  #               next_y += dy
    
  #   return None
  

  def updatePos(self):
    oldX, oldY = Object.orangeGhostX, Object.orangeGhostY
    
    # Get full path and expanded nodes from UcsFindAll
    path, expanded_nodes = self.UcsFindAll((oldX, oldY), (Object.pacmanX, Object.pacmanY))
    
    # If path exists and has at least 2 positions (start + next)
    if path and len(path) >= 2:
        # The first position is current, second position is where to move
        targetX, targetY = path[1]  # Get the next step from the path
        
        newX, newY = oldX, oldY
        if targetX != oldX:
            newX += (targetX - oldX) // abs(targetX - oldX) 
        if targetY != oldY:
            newY += (targetY - oldY) // abs(targetY - oldY)

        Board.coordinates[oldX][oldY] = Board.BLANK
        Board.coordinates[newX][newY] = Board.ORANGE_GHOST

        Object.orangeGhostX = newX
        Object.orangeGhostY = newY
  def get_volume(self, ghost_x, ghost_y, pac_x, pac_y, max_distance=15):
    distance = math.sqrt((ghost_x - pac_x) ** 2 + (ghost_y - pac_y) ** 2)  
    volume = max(0.0, 1 - (distance / max_distance))  # 0.1 là âm lượng nhỏ nhất, 1 là lớn nhất
    return min(1.0, max(0.0, volume))  # Giới hạn từ 0.0 đến 1.0
  def execute(self):
    global quit, start

    quit = False
    start = False

    font = pygame.font.Font("Assets/fonts/arial.ttf", 20)
    shortkey = font.render("ESC: Menu  Q: Thoát", True, (255, 0, 0))

    while Config.running and not quit:
      self.setup()

      Sounds().dramatic_theme_music()
      ghost_move_sound = pygame.mixer.Sound("Assets/sounds/ghost_move.mp3")

      clock = pygame.time.Clock()
      countFrames = 0

      # Bắt đầu đo bộ nhớ
      tracemalloc.start()

      start_time = time.time()  # Lấy thời gian bắt đầu
      path, numberofExpandnodes = self.UcsFindAll((Object.orangeGhostX, Object.orangeGhostY), (Object.pacmanX, Object.pacmanY))
      end_time = time.time()    # Lấy thời gian kết thúc

      # Lấy kết quả peak memory usage
      current, peak = tracemalloc.get_traced_memory()
      # Dừng đo
      tracemalloc.stop()

      node = 0
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
            if (node >= len(path)):
              continue
            
            moveX, moveY = path[node]
            node += 1
            
            oldX, oldY = Object.orangeGhostX, Object.orangeGhostY
            if (oldX, oldY) != (moveX, moveY):
              newX, newY = oldX, oldY
              if moveX != oldX:
                newX += 1 if moveX > oldX else -1 
              if moveY != oldY:
                newY += 1 if moveY > oldY else -1 
          
              Object.orangeGhostX = newX
              Object.orangeGhostY = newY
        
          EM().orangeGhost.move()

        EM().pacman.draw()
        EM().orangeGhost.draw() 
        
        if not start:
          overlay = pygame.Surface((Config.width, Config.height))
          overlay.set_alpha(180)  # Độ trong suốt (0: trong suốt hoàn toàn, 255: không trong suốt)
          overlay.fill((0, 0, 0))  # Màu đen
          Config.screen.blit(overlay, (0, 0))

          color = (255, 255, 255 - countFrames % 30 * 8)
          labelFont =  pygame.font.Font("Assets/fonts/arial.ttf", 20)
          space_to_start = labelFont.render("SPACE để bắt đầu trò chơi", True, color)
          Config.screen.blit(space_to_start, (Config.width / 2 - 130, Config.height / 2 - 50))
        
        Config.screen.blit(shortkey, (580, 800 - 30))

        pygame.display.flip()
        clock.tick(Config.fps)
        countFrames += 1

        if (Object.orangeGhostX, Object.orangeGhostY) == (Object.pacmanX, Object.pacmanY):
          ghost_move_sound.stop()
          Sounds.dramatic_theme_music_sound.stop()
          break
      
      Sounds.lose_sound.play()

      start = False

      algorithm = "UCS"
      search_time = end_time - start_time
      memory_usage = peak / (2 ** 20)
      num_expanded_nodes = numberofExpandnodes
       
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