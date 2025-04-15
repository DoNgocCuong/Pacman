from EntitiesManager import EntitiesManager as EM
from Config import Config, Sounds, Object, Board
from collections import deque
from Entities.Entity import Entity
from Levels.ExperimentBox import ExperimentBox
import time
import tracemalloc #de lay bo nho
import pygame
import math

# testcases: (ghost, pacman)
testcases = [((16, 13), (24, 14)),
             ((21, 3), (15, 21)), 
             ((27, 3), (29, 27)),
             ((6, 2), (24, 26)), 
             ((30, 27), (4, 2))]
testcaseID = 0

quit = False
start = False

class Level1:
    def __init__(self):
        pass

    def setup(self):
        Board.maze = [row[:] for row in Board.initMaze]

        # Setup tọa độ ma trận
        Object.blueGhostX, Object.blueGhostY = testcases[testcaseID][0]
        Object.pacmanX, Object.pacmanY = testcases[testcaseID][1]
        Object.pinkGhostX, Object.pinkGhostY = -1, -1
        Object.redGhostX, Object.redGhostY = -1, -1
        Object.orangeGhostX, Object.orangeGhostY = -1, -1

        # Setup tọa độ thực
        (Object.realPacmanX, Object.realPacmanY) = Entity.getRealCoordinates((Object.pacmanX, Object.pacmanY), Object.PACMAN_SIZE)
        (Object.realBlueGhostX, Object.realBlueGhostY) = Entity.getRealCoordinates((Object.blueGhostX, Object.blueGhostY), Object.BLUE_GHOST_SIZE)

        # Setup ma trận Coordinates 
        Board.coordinates[Object.blueGhostX][Object.blueGhostY] = Board.BLUE_GHOST
        Board.coordinates[Object.pacmanX][Object.pacmanY] = Board.PACMAN 

        for i in range (len(Board.coordinates)): # Chỉ giữ lại giá trị Pacman, BlueGhost trong ma trận Coordinates, các giá trị còn lại bỏ
            for j in range (len(Board.coordinates[0])):
                if (i, j) not in ((Object.blueGhostX, Object.blueGhostY), (Object.pacmanX, Object.pacmanY)):
                    Board.coordinates[i][j] = Board.BLANK
    # BFS trả về toàn bộ đường đi
    def BFSFindAll(self, ghost, pacman):
        bfs_direction = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # trái, phải, trên, dưới
        queue = deque([ghost])
        visited = set([ghost])
        parent = {ghost: None}
        expanded_nodes = 0  # Đếm số node mở rộng để báo cáo kết quả

        if ghost == pacman:
            return None, 0

        while queue:
            ghost_x, ghost_y = queue.popleft()
            expanded_nodes += 1
            
            if (ghost_x, ghost_y) == pacman:
                path = []
                while (ghost_x, ghost_y) != ghost:
                    path.append((ghost_x, ghost_y))
                    (ghost_x, ghost_y) = parent[(ghost_x, ghost_y)]
                path = path[::-1]
                return path, expanded_nodes

            for x, y in bfs_direction:
                go_x = ghost_x + x
                go_y = ghost_y + y
                
                if (0 <= go_x < Board.ROWS and 0 <= go_y < Board.COLS and
                    (0 <= Board.maze[go_x][go_y] <= 2 or Board.maze[go_x][go_y] == 9) and
                    (go_x, go_y) not in visited and
                    (go_x, go_y) != (Object.pinkGhostX, Object.pinkGhostY) and
                    (go_x, go_y) != (Object.orangeGhostX, Object.orangeGhostY) and
                    (go_x, go_y) != (Object.redGhostX, Object.redGhostY)):
                    queue.append((go_x, go_y))
                    visited.add((go_x, go_y))
                    parent[(go_x, go_y)] = (ghost_x, ghost_y)
        
        
        return None, expanded_nodes


    
    def updatePos(self):
        oldX, oldY = Object.blueGhostX, Object.blueGhostY
        list_path, expand = self.BFSFindAll((oldX, oldY), (Object.pacmanX, Object.pacmanY))
        if list_path:
            newPos = list_path[0]
            if newPos:
                newX, newY = newPos

                Board.coordinates[oldX][oldY] = Board.BLANK
                Board.coordinates[newX][newY] = Board.BLUE_GHOST

                Object.blueGhostX = newX
                Object.blueGhostY = newY

            return 
    def get_volume(self, ghost_x, ghost_y, pac_x, pac_y, max_distance=15):
        distance = math.sqrt((ghost_x - pac_x) ** 2 + (ghost_y - pac_y) ** 2)  
        volume = max(0.0, 1 - (distance / max_distance))  # 0.1 là âm lượng nhỏ nhất, 1 là lớn nhất
        return min(1.0, max(0.0, volume))  # Giới hạn từ 0.0 đến 1.0
    
    def execute(self):
        global quit, start
        quit = False
        start = False

        font = pygame.font.Font("Assets/fonts/arial.ttf", 20)
        shortkey = font.render("ESC: Menu  Q: Thoát", True, (255,0, 0))

        while Config.running and not quit:
            self.setup()

            Sounds().dramatic_theme_music()
            ghost_move_sound = pygame.mixer.Sound("Assets/sounds/ghost_move.mp3")

            clock = pygame.time.Clock()
            countFrames = 0

            # Bắt đầu đo bộ nhớ
            tracemalloc.start()

            start_time = time.time()  # Lấy thời gian bắt đầu
            listPos, expanded_nodes = self.BFSFindAll((Object.blueGhostX, Object.blueGhostY), (Object.pacmanX, Object.pacmanY))   # Chạy thuật toán
            end_time = time.time()    # Lấy thời gian kết thúc

            # Lấy kết quả peak memory usage
            current, peak = tracemalloc.get_traced_memory()
            # Dừng đo
            tracemalloc.stop()

            listPos = deque(listPos)

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
                        if listPos:
                            newPos = listPos.popleft()
                            EM().blueGhost.updatePosForEachLv(newPos)
                    volume = self.get_volume(Object.blueGhostX, Object.blueGhostY, Object.pacmanX, Object.pacmanY)
                    ghost_move_sound.set_volume(volume)
                    
                    EM().blueGhost.move()

                EM().pacman.draw()
                EM().blueGhost.draw()
                
                if not start:
                    overlay = pygame.Surface((Config.width, Config.height))
                    overlay.set_alpha(180)  # Độ trong suốt (0: trong suốt hoàn toàn, 255: không trong suốt)
                    overlay.fill((0, 0, 0))  # Màu đen
                    Config.screen.blit(overlay, (0, 0))

                    color = (255, 255, 255 - countFrames % 30 * 8)
                    labelFont =  pygame.font.Font("Assets/fonts/arial.ttf", 20)
                    space_to_start = labelFont.render("SPACE để bắt đầu trò chơi", True, color)
                    Config.screen.blit(space_to_start, (Config.width / 2 - 130, Config.height / 2 - 50))

                if not listPos:
                    ghost_move_sound.stop()
                    Sounds.dramatic_theme_music_sound.stop()
                    break

                Config.screen.blit(shortkey, (580, 800 - 30))  

                pygame.display.flip()
                clock.tick(Config.fps)
                countFrames += 1
            
            Sounds.lose_sound.play()

            start = False

            algorithm = "BFS"
            search_time = end_time - start_time
            memory_usage = peak / (2 ** 20)
            num_expanded_nodes = expanded_nodes
            
            print(search_time * 1000)
            print(memory_usage * 1024)
            print(num_expanded_nodes)

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

