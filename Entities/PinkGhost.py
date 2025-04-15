# # DFS
from .Entity import Entity
from .GhostInterface import GhostInterface
from Config import Config, Material, Board, Object, Mode
from collections import deque

class PinkGhost(GhostInterface):
    def draw(self):
        realX = Object.realPinkGhostX
        realY = Object.realPinkGhostY
        if Mode.PinkGhost == Mode.CHASING:
            Config.screen.blit(Material.PinkGhostImage, (realY, realX))
        elif Mode.PinkGhost == Mode.POWER_UP:
            if Mode.powerupTime <= 60 * 2:
                if Mode.powerupTime // 15 % 2 == 0: 
                    Config.screen.blit(Material.PowerupImage, (realY, realX))
                else:
                    Config.screen.blit(Material.PinkGhostImage, (realY, realX))
            else:
                Config.screen.blit(Material.PowerupImage, (realY, realX))
        else: #dead
            Config.screen.blit(Material.DeadGhostImage, (realY, realX))

    def move(self):
        x, y = Object.pinkGhostX, Object.pinkGhostY

        targetX, targetY = Entity.getRealCoordinates((x, y), Object.PINK_GHOST_SIZE) # tọa độ thực muốn đi đến
        realX, realY = Object.realPinkGhostX, Object.realPinkGhostY # tọa độ thực hiện tại

        dx, dy = (targetX - realX), (targetY - realY)
        sX = Config.p_height / 15
        sY = Config.p_width / 15
        if abs(dx) >= sX:
            realX = realX + dx / abs(dx) * sX
        else:
            realX = targetX
        
        if abs(dy) >= sY:
            realY = realY + dy / abs(dy) * sY
        else:
            realY = targetY

        Object.realPinkGhostX = realX
        Object.realPinkGhostY = realY

    

    def updatePosForEachLv(self, newPos):
        oldX, oldY = Object.pinkGhostX, Object.pinkGhostY
        if newPos:
            newX, newY = newPos

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.PINK_GHOST

            Object.pinkGhostX = newX
            Object.pinkGhostY = newY
    
    def getTargetPosPowerUp(self, ghost, target):
        #Neu ban dau da o target
        if (ghost) == target:
            return None 
            
        ids_direction = [(1, 0), (-1, 0), (0, -1), (0, 1)] # Xuống, Lên, Trái, Phải
        max_depth_limit = 30
        depth_limit = 1
        while depth_limit <= max_depth_limit:
            stack = deque([(ghost)])
            visited = set([ghost])
            depths = {ghost: 0}  
            parent = {ghost : None}

            while stack:# is not None or count_depth == depth_limit:
                (ghost_x, ghost_y) = stack.pop()
                depth = depths[(ghost_x, ghost_y)]
                #print((depth_limit, (ghost_x, ghost_y), depth))

                #Neu gap target
                if (ghost_x, ghost_y) == target:
                    path = [] #list path
                    while (ghost_x, ghost_y) != ghost:
                        path.append((ghost_x, ghost_y))
                        (ghost_x, ghost_y) = parent[(ghost_x, ghost_y)]
                    #path.append((ghost_x, ghost_y))
                    path = path[::-1]
                    return path[0] 
                
                if depth < depth_limit:
                    for x, y in ids_direction:
                        go_x = ghost_x + x
                        go_y = ghost_y + y

                        if 0 <= go_x < Board.ROWS and 0 <= go_y < Board.COLS and ((go_x, go_y) not in visited or depth + 1 < depths[(go_x, go_y)]):
                            if (0 <= Board.maze[go_x][go_y] <= 2 or Board.maze[go_x][go_y] == 9)\
                                and (go_x, go_y) != (Object.orangeGhostX, Object.orangeGhostY) \
                                and (go_x, go_y) != (Object.blueGhostX, Object.blueGhostY) \
                                and (go_x, go_y) != (Object.redGhostX, Object.redGhostY) \
                                and (go_x, go_y) != (Object.pacmanX, Object.pacmanY): #check collision:
                                    stack.append((go_x, go_y))
                                    visited.add((go_x, go_y))
                                    depths[(go_x, go_y)] = depth + 1
                                    parent[(go_x, go_y)] = (ghost_x, ghost_y)

                else: visited.discard((ghost_x, ghost_y))
            depth_limit += 1
    
    def updatePosPowerUp(self, target):
        oldX, oldY = Object.pinkGhostX, Object.pinkGhostY
        newPos = self.getTargetPosPowerUp((oldX, oldY), target)
        if newPos:
            newX, newY = newPos

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.PINK_GHOST

            Object.pinkGhostX = newX
            Object.pinkGhostY = newY

    def getTargetPosRelive(self, ghost, target):
        bfs_direction = [(0, -1), (0, 1), (-1, 0), (1, 0)] #trai, phai, tren, duoi
        queue = deque([ghost])
        visited = set([ghost])
        parent = {ghost : None} # con : cha

        if ghost == target: return None

        while queue:
            ghost_x, ghost_y = queue.popleft()

            #Neu gap target
            if (ghost_x, ghost_y) == target:     
                path = [] #list path
                while (ghost_x, ghost_y) != ghost:
                    path.append((ghost_x, ghost_y))
                    (ghost_x, ghost_y) = parent[(ghost_x, ghost_y)]
                #path.append((ghost_x, ghost_y))
                path = path[::-1]
                return path[0]

            #Duyet BFS
            for x, y in bfs_direction:
                go_x = ghost_x + x
                go_y = ghost_y + y
                if 0 <= go_x < Board.ROWS and 0 <= go_y < Board.COLS:
                    if (0 <= Board.maze[go_x][go_y] <= 2 or Board.maze[go_x][go_y] == 9) and (go_x, go_y) not in visited:
                        queue.append((go_x, go_y))
                        visited.add((go_x, go_y))
                        parent[(go_x, go_y)] = (ghost_x, ghost_y)                        
        return None
    
    def updatePosRelive(self, target):
        oldX, oldY = Object.pinkGhostX, Object.pinkGhostY
        newPos = self.getTargetPosRelive((oldX, oldY), target)
        if newPos:
            newX, newY = newPos

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.PINK_GHOST

            Object.pinkGhostX = newX
            Object.pinkGhostY = newY

    def moveRelive(self):
        x, y = Object.pinkGhostX, Object.pinkGhostY

        targetX, targetY = Entity.getRealCoordinates((x, y), Object.PINK_GHOST_SIZE) # tọa độ thực muốn đi đến
        realX, realY = Object.realPinkGhostX, Object.realPinkGhostY # tọa độ thực hiện tại

        dx, dy = (targetX - realX), (targetY - realY)
        sX = Config.p_height / 10
        sY = Config.p_width / 10
        if abs(dx) >= sX:
            realX = realX + dx / abs(dx) * sX
        else:
            realX = targetX
        
        if abs(dy) >= sY:
            realY = realY + dy / abs(dy) * sY
        else:
            realY = targetY

        Object.realPinkGhostX = realX
        Object.realPinkGhostY = realY