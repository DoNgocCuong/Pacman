# # BFS
from .Entity import Entity
from .GhostInterface import GhostInterface
from Config import Config, Material, Board, Object, Mode
from collections import deque

class BlueGhost(GhostInterface):
    def draw(self):
        realX = Object.realBlueGhostX
        realY = Object.realBlueGhostY
        if Mode.BlueGhost == Mode.CHASING:
            Config.screen.blit(Material.BlueGhostImage, (realY, realX))
        elif Mode.BlueGhost == Mode.POWER_UP:
            if Mode.powerupTime <= 60 * 2:
                if Mode.powerupTime // 15 % 2 == 0: 
                    Config.screen.blit(Material.PowerupImage, (realY, realX))
                else:
                    Config.screen.blit(Material.BlueGhostImage, (realY, realX))
            else:
                Config.screen.blit(Material.PowerupImage, (realY, realX))
        else: #dead
            Config.screen.blit(Material.DeadGhostImage, (realY, realX))
    def move(self):
        x, y = Object.blueGhostX, Object.blueGhostY
        targetX, targetY = Entity.getRealCoordinates((x, y), Object.BLUE_GHOST_SIZE) # tọa độ thực muốn đi đến
        realX, realY = Object.realBlueGhostX, Object.realBlueGhostY # tọa độ thực hiện tại

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

        Object.realBlueGhostX = realX
        Object.realBlueGhostY = realY

    def updatePosForEachLv(self, newPos):
        oldX, oldY = Object.blueGhostX, Object.blueGhostY        
        if newPos:
            newX, newY = newPos

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.BLUE_GHOST

            Object.blueGhostX = newX
            Object.blueGhostY = newY

    def getTargetPosPowerUp(self, ghost, target):
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
                    if (0 <= Board.maze[go_x][go_y] <= 2 or Board.maze[go_x][go_y] == 9) and (go_x, go_y) not in visited\
                        and (go_x, go_y) != (Object.pinkGhostX, Object.pinkGhostY) \
                        and (go_x, go_y) != (Object.orangeGhostX, Object.orangeGhostY) \
                        and (go_x, go_y) != (Object.redGhostX, Object.redGhostY) \
                        and (go_x, go_y) != (Object.pacmanX, Object.pacmanY):
                        queue.append((go_x, go_y))
                        visited.add((go_x, go_y))
                        parent[(go_x, go_y)] = (ghost_x, ghost_y)                        
        return None
    
    def updatePosPowerUp(self, target):
        oldX, oldY = Object.blueGhostX, Object.blueGhostY
        newPos = self.getTargetPosPowerUp((oldX, oldY), target)
        
        if newPos:
            newX, newY = newPos

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.BLUE_GHOST

            Object.blueGhostX = newX
            Object.blueGhostY = newY

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
        oldX, oldY = Object.blueGhostX, Object.blueGhostY
        newPos = self.getTargetPosRelive((oldX, oldY), target)
        
        if newPos:
            newX, newY = newPos

            Board.coordinates[oldX][oldY] = Board.BLANK
            Board.coordinates[newX][newY] = Board.BLUE_GHOST

            Object.blueGhostX = newX
            Object.blueGhostY = newY
    
    def moveRelive(self):
        x, y = Object.blueGhostX, Object.blueGhostY

        targetX, targetY = Entity.getRealCoordinates((x, y), Object.BLUE_GHOST_SIZE) # tọa độ thực muốn đi đến
        realX, realY = Object.realBlueGhostX, Object.realBlueGhostY # tọa độ thực hiện tại

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

        Object.realBlueGhostX = realX
        Object.realBlueGhostY = realY