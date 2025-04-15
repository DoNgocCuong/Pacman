from EntitiesManager import EntitiesManager as EM
from Config import Config, Sounds, Object, Board
from collections import deque
from Entities.Entity import Entity
from Levels.ExperimentBox import ExperimentBox
import time
import tracemalloc #de lay bo nho
import math
import pygame

# testcases: (ghost, pacman)
testcases = [((16, 13), (27, 18)),
             ((21, 3), (4, 13)), 
             ((27, 3), (13, 22)),
             ((6, 2), (29, 27)), 
             ((30, 27), (9, 4))]
testcaseID = 0

quit = False
start = False

class Level2:
    def __init__(self):
        pass

    def setup(self):
        Board.maze = [row[:] for row in Board.initMaze]

        # Setup tọa độ ma trận
        Object.pinkGhostX, Object.pinkGhostY = testcases[testcaseID][0]
        Object.pacmanX, Object.pacmanY = testcases[testcaseID][1]
        Object.blueGhostX, Object.blueGhostY = -1, -1
        Object.redGhostX, Object.redGhostY = -1, -1
        Object.orangeGhostX, Object.orangeGhostY = -1, -1

        # Setup tọa độ thực
        (Object.realPacmanX, Object.realPacmanY) = Entity.getRealCoordinates((Object.pacmanX, Object.pacmanY), Object.PACMAN_SIZE)
        (Object.realPinkGhostX, Object.realPinkGhostY) = Entity.getRealCoordinates((Object.pinkGhostX, Object.pinkGhostY), Object.PINK_GHOST_SIZE)

        # Setup ma trận Coordinates 
        Board.coordinates[Object.pinkGhostX][Object.pinkGhostY] = Board.PINK_GHOST
        Board.coordinates[Object.pacmanX][Object.pacmanY] = Board.PACMAN 

        for i in range (len(Board.coordinates)): # Chỉ giữ lại giá trị Pacman, PinkGhost trong ma trận Coordinates, các giá trị còn lại bỏ
            for j in range (len(Board.coordinates[0])):
                if (i, j) not in ((Object.pinkGhostX, Object.pinkGhostY), (Object.pacmanX, Object.pacmanY)):
                    Board.coordinates[i][j] = Board.BLANK
    # hàm này viết trả hết tất cả các đường đi
    # hàm này viết trả hết tất cả các đường đi
    def DfsFindAll(self, ghost, pacman):
        if ghost == pacman:
            return None 
        # Nếu ghost và pacman ở cùng một vị trí thì không cần tìm đường đi
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)] # Xuống, Lên, Trái, Phải
        # độ sâu tối đa
        max_depth = 100
        # độ sâu hiện tại
        current_depth = 1
        # số lượng node đã duyệt
        nodes_expanded = 0
        # duyệt từ độ sâu 1 đến độ sâu tối đa
        while current_depth <= max_depth:
            stack = deque([ghost]) # bắt đầu stack từ ghost
            visited = {ghost} # đánh dấu ghost đã được duyệt
            depth_map = {ghost: 0} # đánh dấu độ sâu của ghost là 0
            parent_map = {ghost: None} # đánh dấu cha của ghost là None
            while stack: # stack không rỗng
                current = stack.pop() # lấy ra phần tử cuối cùng trong stack
                nodes_expanded += 1 # tăng số lượng node đã duyệt lên 1
                current_depth_level = depth_map[current] # lấy độ sâu của phần tử hiện tại
                if current == pacman: # nếu phần tử hiện tại là pacman thì trả về đường đi
                    path = [] # khởi tạo đường đi
                    while current != ghost: # trong khi phần tử hiện tại không phải là ghost thì tiếp tục duyệt
                        path.append(current) # thêm phần tử hiện tại vào đường đi
                        current = parent_map[current]  # cập nhật phần tử hiện tại là cha của nó
                    return path[::-1], nodes_expanded # trả về đường đi từ ghost đến pacman và số lượng node đã duyệt
                if current_depth_level < current_depth: # nếu độ sâu của phần tử hiện tại nhỏ hơn độ sâu tối đa thì tiếp tục duyệt
                    for dx, dy in directions: # duyệt các hướng đi
                        neighbor = (current[0] + dx, current[1] + dy) # tính toán tọa độ của phần tử kề bên
                        # kiểm tra tọa độ kề bên có hợp lệ không và có trong danh sách đã duyệt chưa
                        # kiểm tra độ sâu của phần tử kề bên có nhỏ hơn độ sâu đã duyệt chưa
                        # kiểm tra phần tử kề bên có phải là pacman không
                        if (0 <= neighbor[0] < Board.ROWS and 0 <= neighbor[1] < Board.COLS and
                            (neighbor not in visited or current_depth_level + 1 < depth_map.get(neighbor, float('inf')))):
                            # kiểm tra phần tử kề bên có phải là tường không
                            # kiểm tra phần tử kề bên có phải là pacman không 
                            if (0 <= Board.maze[neighbor[0]][neighbor[1]] <= 2 or Board.maze[neighbor[0]][neighbor[1]] == 9) and \
                            neighbor not in {(Object.blueGhostX, Object.blueGhostY),
                                                (Object.orangeGhostX, Object.orangeGhostY),
                                                (Object.redGhostX, Object.redGhostY)}:
                                # nếu phần tử kề bên không phải là tường và không phải là pacman thì thêm vào stack
                                # thêm phần tử kề bên vào stack
                                stack.append(neighbor)
                                # đánh dấu phần tử kề bên đã được duyệt
                                visited.add(neighbor)
                                # đánh dấu độ sâu của phần tử kề bên là độ sâu của phần tử hiện tại + 1
                                depth_map[neighbor] = current_depth_level + 1
                                # đánh dấu cha của phần tử kề bên là phần tử hiện tại
                                parent_map[neighbor] = current
            # nếu không tìm thấy đường đi thì tăng độ sâu lên 1 và tiếp tục duyệt
            current_depth += 1
        # nếu không tìm thấy đường đi thì trả về None
        return None, nodes_expanded

    
    def updatePos(self):
        oldX, oldY = Object.pinkGhostX, Object.pinkGhostY
        list_path, expand = self.DfsFindAll((oldX, oldY), (Object.pacmanX, Object.pacmanY))
        if list_path:
            newPos = list_path[0]         
            if newPos:
                newX, newY = newPos

                Board.coordinates[oldX][oldY] = Board.BLANK
                Board.coordinates[newX][newY] = Board.PINK_GHOST

                Object.pinkGhostX = newX
                Object.pinkGhostY = newY
    
    def get_volume(self, ghost_x, ghost_y, pac_x, pac_y, max_distance=15):
        distance = math.sqrt((ghost_x - pac_x) ** 2 + (ghost_y - pac_y) ** 2)  
        volume = max(0.0, 1 - (distance / max_distance))  # 0.1 là âm lượng nhỏ nhất, 1 là lớn nhất
        return min(1.0, max(0.0, volume))  # Giới hạn từ 0.0 đến 1.0
    
    def execute(self):
        global quit, start

        quit = False
        start = False

        font = pygame.font.Font("Assets/fonts/arial.ttf", 20)
        shortkey = font.render("ESC: Menu  Q: thoát", True, (255, 0, 0))

        while Config.running and not quit:
            self.setup()

            Sounds().dramatic_theme_music()
            ghost_move_sound = pygame.mixer.Sound("Assets/sounds/ghost_move.mp3")

            clock = pygame.time.Clock()
            countFrames = 0 # 0

            # Bắt đầu đo bộ nhớ
            tracemalloc.start()

            start_time = time.time()  # Lấy thời gian bắt đầu
            listPos, expanded_nodes = self.DfsFindAll((Object.pinkGhostX, Object.pinkGhostY), (Object.pacmanX, Object.pacmanY))   # Chạy thuật toán
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
                            EM().pinkGhost.updatePosForEachLv(newPos)
                    volume = self.get_volume(Object.pinkGhostX, Object.pinkGhostY, Object.pacmanX, Object.pacmanY)
                    ghost_move_sound.set_volume(volume)
                    
                    EM().pinkGhost.move()

                EM().pacman.draw()
                EM().pinkGhost.draw()
                
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

            algorithm = "IDS"
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