# # DFS
import heapq
from .Entity import Entity
from .GhostInterface import GhostInterface
from Config import Config, Material, Board, Object, Mode
from collections import deque

class OrangeGhost(GhostInterface):
    def draw(self):
        realX = Object.realOrangeGhostX
        realY = Object.realOrangeGhostY
        if Mode.OrangeGhost == Mode.CHASING:
            Config.screen.blit(Material.OrangeGhostImage, (realY, realX))
        elif Mode.OrangeGhost == Mode.POWER_UP:
            if Mode.powerupTime <= 60 * 2:
                if Mode.powerupTime // 15 % 2 == 0: 
                    Config.screen.blit(Material.PowerupImage, (realY, realX))
                else:
                    Config.screen.blit(Material.OrangeGhostImage, (realY, realX))
            else:
                Config.screen.blit(Material.PowerupImage, (realY, realX))
        else: #dead
            Config.screen.blit(Material.DeadGhostImage, (realY, realX))

    def move(self):
        x, y = Object.orangeGhostX, Object.orangeGhostY

        targetX, targetY = Entity.getRealCoordinates((x, y), Object.ORANGE_GHOST_SIZE) # tọa độ thực muốn đi đến
        realX, realY = Object.realOrangeGhostX, Object.realOrangeGhostY # tọa độ thực hiện tại

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

        Object.realOrangeGhostX = realX
        Object.realOrangeGhostY = realY

    
    
    def isValidPosPowerUp(self, x, y):
        if 0 <= x < Board.ROWS and 0 <= y < Board.COLS:
            if (Board.maze[x][y] < 3 or Board.maze[x][y] == 9) and Board.coordinates[x][y] == Board.BLANK:
                return True
        return False
    
    def getTargetPosPowerUp(self, ghost, target): # UCS*
        (posX, posY) = ghost
        f = 0
        heap = [(f, posX, posY, [])] 
        heapq.heapify(heap)
        visited = set([(posX, posY)])
        
        DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)] # lên, xuống, phải, trái
        PATH_LIMIT = 100

        while heap:
            (f, x, y, path) = heapq.heappop(heap)
            
            if (x, y) == target or len(path) == PATH_LIMIT:
                return path[0] if len(path) > 0 else None

            for dx, dy in DIRECTIONS:
                nx = x + dx
                ny = y + dy
                
                if not self.isValidPosPowerUp(nx, ny):
                    continue
                while (nx, ny) not in Board.nodes and (nx, ny) != target:
                    nx += dx
                    ny += dy
                    if not self.isValidPosPowerUp(nx, ny):
                        break

                if (nx, ny) not in visited and self.isValidPosPowerUp(nx, ny)\
                    and (nx, ny) != (Object.pinkGhostX, Object.pinkGhostY) \
                    and (nx, ny) != (Object.blueGhostX, Object.blueGhostY) \
                    and (nx, ny) != (Object.redGhostX, Object.redGhostY) \
                    and (nx, ny) != (Object.pacmanX, Object.pacmanY): #check collision:
                    nf = f + abs(nx - x) + abs(ny - y)
                    heapq.heappush(heap, (nf, nx, ny, path + [(nx, ny)]))
                    visited.add((nx, ny))
        
        return None
    
    def updatePosPowerUp(self, target):
        oldX, oldY = Object.orangeGhostX, Object.orangeGhostY
        targetPos = self.getTargetPosPowerUp((oldX, oldY), target)

        if targetPos:
            targetX, targetY = targetPos

            newX, newY = oldX, oldY
            if targetX != oldX:
                newX += (targetX - oldX) // abs(targetX - oldX) 
            if targetY != oldY:
                newY += (targetY - oldY) // abs(targetY - oldY)

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.ORANGE_GHOST

            Object.orangeGhostX = newX
            Object.orangeGhostY = newY
    
    def getTargetPosRelive(self, ghost, target): # UCS*
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
        oldX, oldY = Object.orangeGhostX, Object.orangeGhostY
        targetPos = self.getTargetPosRelive((oldX, oldY), target)

        if targetPos:
            targetX, targetY = targetPos

            newX, newY = oldX, oldY
            if targetX != oldX:
                newX += (targetX - oldX) // abs(targetX - oldX) 
            if targetY != oldY:
                newY += (targetY - oldY) // abs(targetY - oldY)

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.ORANGE_GHOST

            Object.orangeGhostX = newX
            Object.orangeGhostY = newY

    def moveRelive(self):
        x, y = Object.orangeGhostX, Object.orangeGhostY

        targetX, targetY = Entity.getRealCoordinates((x, y), Object.ORANGE_GHOST_SIZE) # tọa độ thực muốn đi đến
        realX, realY = Object.realOrangeGhostX, Object.realOrangeGhostY # tọa độ thực hiện tại

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

        Object.realOrangeGhostX = realX
        Object.realOrangeGhostY = realY