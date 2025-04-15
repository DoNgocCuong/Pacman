from Entities.Entity import Entity
from EntitiesManager import EntitiesManager as EM
from Config import Config, Object, Sounds, Board, Mode
import time
import random
import math
import pygame
from .Level1 import Level1
from .Level2 import Level2
from .Level3 import Level3
from .Level4 import Level4
start = False
PacmanGetCaught = False
quit = False

countFrames = 0

ClickOnButton = None

prevHoverOn = None
curHoverOn = None

setUpCoordinates = {
    'blueGhost': (14, 12),
    'pinkGhost': (16, 12),
    'orangeGhost': (14, 17),
    'redGhost': (16, 17),
    'pacman': (24, 14)
}
availableNodes = [(21, 16), (27, 4), (27, 13), (14, 13), (2, 2), (6, 2), (15, 14), (16, 13), (18, 10), (18, 19), (30, 2), (14, 15), (9, 10), (9, 19), (24, 10), (15, 7), (24, 19), (15, 16), (6, 13), (16, 15), (21, 2), (14, 17), (30, 13), (15, 0), (16, 17), (2, 27), (12, 13), (6, 27), (27, 22), (30, 27), (12, 15), (14, 12), (21, 27), (9, 7), (9, 16), (24, 7), (24, 16), (15, 13), (2, 13), (16, 12), (24, 25), (2, 22), (6, 22), (14, 14), (16, 14), (21, 13), (12, 10), (21, 22), (9, 2), (12, 19), (14, 16), (27, 10), (24, 2), (27, 19), (16, 16), (15, 29), (24, 4), (6, 10), (15, 22), (6, 19), (12, 14), (9, 27), (15, 15), (21, 10), (24, 27), (21, 19), (12, 16), (27, 7), (27, 16), (27, 25), (15, 17), (9, 13), (27, 27), (2, 7), (9, 22), (2, 16), (24, 13), (15, 10), (6, 7), (24, 22), (15, 19), (6, 16), (27, 2), (30, 16), (15, 12), (21, 7)]
TargetPosInPowerUp = {
    'blueGhost': (6, 2),
    'pinkGhost': (30, 2),
    'orangeGhost': (30, 27),
    'redGhost': (2, 27),
}

def isHit(pos1, pos2):
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    return dx < Config.p_width and dy < Config.p_height

class Level6:
    def __init__(self):
        pass

    def setup(self):
        global PacmanGetCaught, quit, start, countFrames
        global BlueGhostStatus, PinkGhostStatus, OrangeGhostStatus, RedGhostStatus
        
        countFrames = 0
        PacmanGetCaught = False
        quit = False
        start = False

        Config.KeyMovePacman = None

        # Setup mode
        Mode.mode = Mode.CHASING
        Mode.powerupTime = 0
        Mode.BlueGhost = Mode.CHASING
        Mode.PinkGhost = Mode.CHASING
        Mode.OrangeGhost = Mode.CHASING
        Mode.RedGhost = Mode.CHASING

        # Setup tọa độ ma trận
        Object.pacmanX, Object.pacmanY = setUpCoordinates["pacman"]
        Object.blueGhostX, Object.blueGhostY = setUpCoordinates["blueGhost"]
        Object.pinkGhostX, Object.pinkGhostY = setUpCoordinates["pinkGhost"]
        Object.orangeGhostX, Object.orangeGhostY = setUpCoordinates["orangeGhost"]
        Object.redGhostX, Object.redGhostY = setUpCoordinates["redGhost"]
        
        # Setup tọa độ thực
        (Object.realPacmanX, Object.realPacmanY) = Entity.getRealCoordinates((Object.pacmanX, Object.pacmanY), Object.PACMAN_SIZE)
        (Object.realRedGhostX, Object.realRedGhostY) = Entity.getRealCoordinates((Object.redGhostX, Object.redGhostY), Object.RED_GHOST_SIZE)
        (Object.realOrangeGhostX, Object.realOrangeGhostY) = Entity.getRealCoordinates((Object.orangeGhostX, Object.orangeGhostY), Object.ORANGE_GHOST_SIZE)
        (Object.realPinkGhostX, Object.realPinkGhostY) = Entity.getRealCoordinates((Object.pinkGhostX, Object.pinkGhostY), Object.PINK_GHOST_SIZE)
        (Object.realBlueGhostX, Object.realBlueGhostY) = Entity.getRealCoordinates((Object.blueGhostX, Object.blueGhostY), Object.BLUE_GHOST_SIZE)

        # Setup ma trận Coordinates
        Board.coordinates[Object.blueGhostX][Object.blueGhostY] = Board.BLUE_GHOST
        Board.coordinates[Object.pinkGhostX][Object.pinkGhostY] = Board.PINK_GHOST
        Board.coordinates[Object.orangeGhostX][Object.orangeGhostY] = Board.ORANGE_GHOST
        Board.coordinates[Object.redGhostX][Object.redGhostY] = Board.RED_GHOST
        Board.coordinates[Object.pacmanX][Object.pacmanY] = Board.PACMAN 

        for i in range(len(Board.coordinates)):
            for j in range(len(Board.coordinates[i])):
                if (i, j) not in ((Object.blueGhostX, Object.blueGhostY), \
                                  (Object.pinkGhostX, Object.pinkGhostY), \
                                  (Object.orangeGhostX, Object.orangeGhostY), \
                                  (Object.redGhostX, Object.redGhostY), \
                                  (Object.pacmanX, Object.pacmanY)):
                    Board.coordinates[i][j] = Board.BLANK
    
    def get_volume(self, ghost, pacman, max_distance=15):
        ghost_x, ghost_y = ghost
        pac_x, pac_y = pacman
        distance = math.sqrt((ghost_x - pac_x) ** 2 + (ghost_y - pac_y) ** 2)  
        volume = max(0.0, 1 - (distance / max_distance))  # 0.1 là âm lượng nhỏ nhất, 1 là lớn nhất
        return min(1.0, max(0.0, volume))  # Giới hạn từ 0.0 đến 1.0

    def set_volume(self):
        normal_move_volume = 0
        powerup_move_volume = 0
        ghosts = [(Object.blueGhostX, Object.blueGhostY), \
            (Object.pinkGhostX, Object.pinkGhostY), \
            (Object.orangeGhostX, Object.orangeGhostY), \
            (Object.redGhostX, Object.redGhostY)]
        modes = [Mode.BlueGhost, Mode.PinkGhost, Mode.OrangeGhost, Mode.RedGhost]
        pacman = (Object.pacmanX, Object.pacmanY)

        for i in range(len(ghosts)):
            volume = self.get_volume(ghosts[i], pacman)
            if modes[i] == Mode.CHASING:
                normal_move_volume = max(normal_move_volume, volume)
            elif modes[i] == Mode.POWER_UP:
                powerup_move_volume = max(powerup_move_volume, volume)
        
        Sounds.ghost_move_sound.set_volume(normal_move_volume)
        Sounds.ghost_move_powerup_sound.set_volume(powerup_move_volume)

    def isCaught(self):
        pacmanPos = (Object.pacmanX, Object.pacmanY)
        ghostPos = [(Object.blueGhostX, Object.blueGhostY), (Object.pinkGhostX, Object.pinkGhostY), (Object.redGhostX, Object.redGhostY), (Object.orangeGhostX, Object.orangeGhostY)]
        ghostMode = [Mode.BlueGhost, Mode.PinkGhost, Mode.RedGhost, Mode.OrangeGhost]

        for i in range(len(ghostPos)):
            pos = ghostPos[i]
            mode = ghostMode[i]
            if mode == Mode.CHASING and pos == pacmanPos:
                Config.life -= 1
                return True

        return False
    
    def setTargetPosPowerUp(self):
        global TargetPosInPowerUp
        curCoordinates = {"blueGhost": (Object.blueGhostX, Object.blueGhostY), 
                          "pinkGhost": (Object.realPacmanX, Object.pinkGhostY),
                          "redGhost": (Object.redGhostX, Object.redGhostY), 
                          "orangeGhost": (Object.orangeGhostX, Object.orangeGhostY)}
        
        newBlueGhostPos = TargetPosInPowerUp["blueGhost"]
        while newBlueGhostPos in set(TargetPosInPowerUp.values()) | set(curCoordinates.values()):
            newBlueGhostPos = random.choice(availableNodes)
        TargetPosInPowerUp["blueGhost"] = newBlueGhostPos

        newPinkGhostPos = TargetPosInPowerUp["pinkGhost"]
        while newPinkGhostPos in set(TargetPosInPowerUp.values()) | set(curCoordinates.values()):
            newPinkGhostPos = random.choice(availableNodes)
        TargetPosInPowerUp["pinkGhost"] = newPinkGhostPos

        newOrangeGhostPos = TargetPosInPowerUp["orangeGhost"]
        while newOrangeGhostPos in set(TargetPosInPowerUp.values()) | set(curCoordinates.values()):
            newOrangeGhostPos = random.choice(availableNodes)
        TargetPosInPowerUp["orangeGhost"] = newOrangeGhostPos

        newRedGhostPos = TargetPosInPowerUp["redGhost"]
        while newRedGhostPos in set(TargetPosInPowerUp.values()) | set(curCoordinates.values()):
            newRedGhostPos = random.choice(availableNodes)
        TargetPosInPowerUp["redGhost"] = newRedGhostPos

    def ghostChasingMode(self):
        red=Level4()
        pink=Level2()
        orange=Level3()
        blue=Level1()
        global start, PacmanGetCaught, countFrames
        if start and not PacmanGetCaught:
            if countFrames % 15 == 0:
                if Mode.BlueGhost == Mode.CHASING:
                    blue.updatePos()
                if Mode.PinkGhost == Mode.CHASING and countFrames > 60 * 5:
                    pink.updatePos()
                if Mode.OrangeGhost == Mode.CHASING and countFrames > 60 * 10:
                    orange.updatePos()
                if Mode.RedGhost == Mode.CHASING and countFrames > 60 * 15:
                    red.updatePos()
                PacmanGetCaught = self.isCaught()

            if Mode.BlueGhost == Mode.CHASING:   
                EM().blueGhost.move()
            if Mode.PinkGhost == Mode.CHASING:
                EM().pinkGhost.move()
            if Mode.OrangeGhost == Mode.CHASING:
                EM().orangeGhost.move()
            if Mode.RedGhost == Mode.CHASING:
                EM().redGhost.move()
    
    def powerupMode(self):
        global PacmanGetCaught, random_node, countFrames
        if start and not PacmanGetCaught:
            if countFrames % 60 * 2 == 0:
                self.setTargetPosPowerUp()
            if countFrames % 15 == 0:
                if Mode.BlueGhost == Mode.POWER_UP:
                    EM().blueGhost.updatePosPowerUp(TargetPosInPowerUp["blueGhost"])
                if Mode.PinkGhost == Mode.POWER_UP and countFrames > 60 * 5:
                    EM().pinkGhost.updatePosPowerUp(TargetPosInPowerUp["pinkGhost"])
                if Mode.OrangeGhost == Mode.POWER_UP and countFrames > 60 * 10:
                    EM().orangeGhost.updatePosPowerUp(TargetPosInPowerUp["orangeGhost"])
                if Mode.RedGhost == Mode.POWER_UP and countFrames > 60 * 15:
                    EM().redGhost.updatePosPowerUp(TargetPosInPowerUp["redGhost"])

                pacmanPos = (Object.realPacmanX, Object.realPacmanY)
                blueGhostPos = (Object.realBlueGhostX, Object.realBlueGhostY)
                pinkGhostPos = (Object.realPinkGhostX, Object.realPinkGhostY)
                orangeGhostPos = (Object.realOrangeGhostX, Object.realOrangeGhostY)
                redGhostPos = (Object.realRedGhostX, Object.realRedGhostY)

                if Mode.BlueGhost == Mode.POWER_UP and isHit(blueGhostPos, pacmanPos):
                    Sounds.pacman_eat_ghost_sound.play()
                    (Object.realBlueGhostX, Object.realBlueGhostY) = Entity.getRealCoordinates((Object.blueGhostX, Object.blueGhostY), Object.BLUE_GHOST_SIZE)
                    Mode.BlueGhost = Mode.DEAD
                    Config.score += 50
                if Mode.PinkGhost == Mode.POWER_UP and isHit(pinkGhostPos, pacmanPos):
                    Sounds.pacman_eat_ghost_sound.play()
                    (Object.realPinkGhostX, Object.realPinkGhostY) = Entity.getRealCoordinates((Object.pinkGhostX, Object.pinkGhostY), Object.PINK_GHOST_SIZE)
                    Mode.PinkGhost = Mode.DEAD
                    Config.score += 50
                if Mode.OrangeGhost == Mode.POWER_UP and isHit(orangeGhostPos, pacmanPos):
                    Sounds.pacman_eat_ghost_sound.play()
                    (Object.realOrangeGhostX, Object.realOrangeGhostY) = Entity.getRealCoordinates((Object.orangeGhostX, Object.orangeGhostY), Object.ORANGE_GHOST_SIZE)
                    Mode.OrangeGhost = Mode.DEAD
                    Config.score += 50
                if Mode.RedGhost == Mode.POWER_UP and isHit(redGhostPos, pacmanPos):
                    Sounds.pacman_eat_ghost_sound.play()
                    (Object.realRedGhostX, Object.realRedGhostY) = Entity.getRealCoordinates((Object.redGhostX, Object.redGhostY), Object.RED_GHOST_SIZE)
                    Mode.RedGhost = Mode.DEAD
                    Config.score += 50

            if Mode.BlueGhost == Mode.POWER_UP:   
                EM().blueGhost.move()
            if Mode.PinkGhost == Mode.POWER_UP:
                EM().pinkGhost.move()
            if Mode.OrangeGhost == Mode.POWER_UP:
                EM().orangeGhost.move()
            if Mode.RedGhost == Mode.POWER_UP:
                EM().redGhost.move()
    
    def deadGhostRelives(self):
        if countFrames % 10 == 0:
            if (Mode.BlueGhost == Mode.DEAD):
                if (Object.blueGhostX, Object.blueGhostY) == setUpCoordinates["blueGhost"]:
                    Mode.BlueGhost = Mode.CHASING
                else:
                    EM().blueGhost.updatePosRelive(setUpCoordinates["blueGhost"])
            if (Mode.PinkGhost == Mode.DEAD):
                if (Object.pinkGhostX, Object.pinkGhostY) == setUpCoordinates["pinkGhost"]:
                    Mode.PinkGhost = Mode.CHASING
                else:
                    EM().pinkGhost.updatePosRelive(setUpCoordinates["pinkGhost"])
            if (Mode.OrangeGhost == Mode.DEAD):
                if (Object.orangeGhostX, Object.orangeGhostY) == setUpCoordinates["orangeGhost"]:
                    Mode.OrangeGhost = Mode.CHASING
                else:
                    EM().orangeGhost.updatePosRelive(setUpCoordinates["orangeGhost"])
            if (Mode.RedGhost == Mode.DEAD):
                if (Object.redGhostX, Object.redGhostY) == setUpCoordinates["redGhost"]:
                    Mode.RedGhost = Mode.CHASING
                else:
                    EM().redGhost.updatePosRelive(setUpCoordinates["redGhost"])
        
        if Mode.BlueGhost == Mode.DEAD:   
            EM().blueGhost.moveRelive()
        if Mode.PinkGhost == Mode.DEAD:
            EM().pinkGhost.moveRelive()
        if Mode.OrangeGhost == Mode.DEAD:
            EM().orangeGhost.moveRelive()
        if Mode.RedGhost == Mode.DEAD:
            EM().redGhost.moveRelive()

    def isWin(self):
        return Config.normalDots + Config.powerupDots == 0
    
    def isLost(self):
        return Config.life == 0

    def execute(self):
        global PacmanGetCaught, quit, start, countFrames
        
        quit = False

        font = pygame.font.Font("Assets/fonts/arial.ttf", 20)
        shortkey = font.render("ESC: Menu  Q: Quit", True, (255, 255, 255))

        while Config.running and not quit:
            # Score and Lives:
            Config.score = 0
            Config.life = 3
            
            Config.normalDots = 242
            Config.powerupDots = 4

            Board.maze = [row[:] for row in Board.initMaze]

            self.setup()
            clock = pygame.time.Clock()
            last_tick = pygame.time.get_ticks()
            
            Sounds.dramatic_theme_music_sound.set_volume(0.1)
            Sounds.dramatic_theme_music_sound.play(loops=-1)
            Sounds.ghost_move_powerup_sound.play(loops=-1).set_volume(0)

            while Config.running and not quit:
                Config.screen.fill('black')

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Sounds.ghost_move_powerup_sound.stop()
                        Sounds.ghost_move_sound.stop()
                        Sounds.dramatic_theme_music_sound.stop()
                        Config.running = False
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            Sounds.click_sound.play()
                            Sounds.pacman_eat_dot_sound.stop()
                            Sounds.ghost_move_powerup_sound.stop()
                            Sounds.ghost_move_sound.stop()
                            Sounds.dramatic_theme_music_sound.stop()
                            quit = True
                            return
                        if event.key == pygame.K_q:
                            Sounds.click_sound.play()
                            Sounds.ghost_move_powerup_sound.stop()
                            Sounds.ghost_move_sound.stop()
                            Sounds.dramatic_theme_music_sound.stop()
                            Config.running = False
                            return
                        if event.key == pygame.K_SPACE:
                            if not start:
                                Sounds.pacman_eat_dot_sound.play(loops=-1)
                                Sounds.ghost_move_sound.play(loops=-1)  # Lặp vô hạn
                                Sounds.ghost_move_powerup_sound.play(loops=-1)
                                start = True
                        if event.key == pygame.K_UP:
                            Config.KeyMovePacman = pygame.K_UP
                        if event.key == pygame.K_DOWN:
                            Config.KeyMovePacman = pygame.K_DOWN
                        if event.key == pygame.K_LEFT:
                            Config.KeyMovePacman = pygame.K_LEFT
                        if event.key == pygame.K_RIGHT:
                            Config.KeyMovePacman = pygame.K_RIGHT
                
                if Config.counter < 19:
                    Config.counter += 1
                    if Config.counter > 3:
                        Config.flicker = False
                else:
                    Config.flicker = True
                    Config.counter = 0
                    
                EM().maze.draw()
                EM().pacman.setupdrawdir()
                EM().blueGhost.draw()
                EM().pinkGhost.draw()
                EM().orangeGhost.draw()
                EM().redGhost.draw()
                EM().life.draw()
                EM().score.draw()

                if not start:
                    overlay = pygame.Surface((Config.width, Config.height))
                    overlay.set_alpha(180)  # Độ trong suốt (0: trong suốt hoàn toàn, 255: không trong suốt)
                    overlay.fill((0, 0, 0))  # Màu đen
                    Config.screen.blit(overlay, (0, 0))
                    
                    color = (255, 255, 255 - countFrames % 30 * 8)
                    labelFont =pygame.font.Font("Assets/fonts/arial.ttf", 20)
                    space_to_start = labelFont.render("SPACE để bắt đầu trò chơi", True, color)
                    Config.screen.blit(space_to_start, (Config.width / 2 - 130, Config.height / 2 - 50))

                if Mode.powerupTime == 0:
                    Mode.mode = Mode.CHASING
                    Mode.BlueGhost = Mode.CHASING if Mode.BlueGhost != Mode.DEAD else Mode.DEAD
                    Mode.PinkGhost = Mode.CHASING if Mode.PinkGhost != Mode.DEAD else Mode.DEAD
                    Mode.OrangeGhost = Mode.CHASING if Mode.OrangeGhost != Mode.DEAD else Mode.DEAD
                    Mode.RedGhost = Mode.CHASING if Mode.RedGhost != Mode.DEAD else Mode.DEAD

                self.set_volume()
                self.ghostChasingMode()
                self.powerupMode()

                if start and countFrames % 15 == 0:
                    EM().pacman.updatePos()
                EM().pacman.move()

                self.deadGhostRelives()

                Config.screen.blit(shortkey, (580, 800 - 30))
            
                pygame.display.flip()
                clock.tick(Config.fps)
                if start:
                    countFrames += 1
                    Mode.powerupTime -= 1 if Mode.powerupTime > 0 else 0
                    
                if PacmanGetCaught and not self.isLost():
                    Sounds.lose_sound.play()
                    #Sounds.dramatic_theme_music_sound.stop()
                    Sounds.pacman_eat_dot_sound.stop()
                    Sounds.ghost_move_powerup_sound.stop()
                    Sounds.ghost_move_sound.stop()
                    #Sounds.pacman_death()
                    time.sleep(1.5)
                    self.setup()
                    continue
                
                if self.isWin() or self.isLost():
                    Sounds.pacman_eat_dot_sound.stop()
                    Sounds.ghost_move_powerup_sound.stop()
                    Sounds.ghost_move_sound.stop()
                    break
                
            if self.isWin():
                self.win()
            elif self.isLost():
                self.lose()

            Sounds.dramatic_theme_music_sound.stop()
    
    def lose(self):
        global quit, ClickOnButton
        
        Sounds.lose_sound.play()
        
        clock = pygame.time.Clock()
        last_tick = pygame.time.get_ticks()


        Sounds.dramatic_theme_music_sound.stop()
        
        font =pygame.font.Font("Assets/fonts/arial.ttf", 20)
        shortkey = font.render("ESC: Menu  Q: Thoát", True, (255, 0,0))

        # Font và màu sắc
        font_big = pygame.font.Font("Assets/fonts/arial.ttf", 150)  # Font lớn cho "YOU LOST"
        font_small = pygame.font.Font("Assets/fonts/arial.ttf", 80)  # Font cho "SCORE"
        font_button = pygame.font.Font("Assets/fonts/arial.ttf", 40)  # Font cho các nút
        color_text = (0, 0, 0)  # Màu chữ đen
        color_button = (255, 255, 255)  # Màu nền nút trắng
        color_hover = (144, 238, 144)  # Màu hover xanh nhạt

        # Chữ YOU LOSE
        font_big = pygame.font.Font("Assets/fonts/arial.ttf", 150)  # Chọn font, 150px là kích thước chữ
        you_lose_text = font_big.render("Bạn Thua", True, (255, 0, 0))  # Chữ đỏ
        you_lose_text_rect = you_lose_text.get_rect(center=(400, 800 * 1 // 4))  # Căn giữa, y = 2/3 chiều cao màn hình
        
        # Chữ SCORE: ...
        font_small = pygame.font.Font("Assets/fonts/arial.ttf", 80)
        score_text = f"Điểm: {Config.score}"
        text_score = font_small.render(score_text, True, (255, 255, 255))
        text_score_rect = text_score.get_rect(center=(400, you_lose_text_rect.bottom + 50))

        # Tạo nút (text, x, y, width, height)
        buttons = [
            ("Tiếp tục", 400, text_score_rect.bottom + 50 + 50, 200, 70),
            ("Menu", 400, text_score_rect.bottom + 150 + 50, 200, 70),
            ("Thoát", 400, text_score_rect.bottom + 250 + 50, 200, 70),
        ]

        ClickOnButton = None

        while Config.running and not quit:
            Config.screen.fill('black')

            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Config.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Sounds.click_sound.play()
                        quit = True
                        return
                    if event.key == pygame.K_q:
                        Sounds.click_sound.play()
                        Config.running = False
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for text, x, y, w, h in buttons:
                        if x - w // 2 <= mouse_x <= x + w // 2 and y - h // 2 <= mouse_y <= y + h // 2:
                            ClickOnButton = text 

            EM().maze.draw()
            EM().pacman.setupdrawdir()
            EM().blueGhost.draw()
            EM().pinkGhost.draw()
            EM().orangeGhost.draw()
            EM().redGhost.draw()
            EM().life.draw()
            EM().score.draw()

            overlay = pygame.Surface((Config.width, Config.height))
            overlay.set_alpha(180)  # Độ trong suốt (0: trong suốt hoàn toàn, 255: không trong suốt)
            overlay.fill((0, 0, 0))  # Màu đen
            Config.screen.blit(overlay, (0, 0))

            # Vẽ chữ
            Config.screen.blit(you_lose_text, you_lose_text_rect)
            Config.screen.blit(text_score, text_score_rect)

            # Vẽ nút
            global prevHoverOn, curHoverOn
            curHoverOn = None

            for text, x, y, w, h in buttons:
                is_hovered = x - w // 2 <= mouse_x <= x + w // 2 and y - h // 2 <= mouse_y <= y + h // 2
                color = color_button
                
                if is_hovered:
                    color = color_hover
                    curHoverOn = text

                pygame.draw.rect(Config.screen, color, (x - w // 2, y - h // 2, w, h), border_radius=15)  # Nút bo góc
                text_render = font_button.render(text, True, color_text)
                text_rect = text_render.get_rect(center=(x, y))
                Config.screen.blit(text_render, text_rect)  # Hiển thị chữ trên nút
            
            if curHoverOn != prevHoverOn:
                prevHoverOn = curHoverOn
                if curHoverOn:
                    Sounds.hover_sound.play()

            if ClickOnButton == "Tiếp tục":
                Sounds.click_sound.play()
                return
            elif ClickOnButton == "Menu":
                Sounds.click_sound.play()
                quit = True
                return
            elif ClickOnButton == "Thoát":
                Sounds.click_sound.play()
                Config.running = False
                return

            Config.screen.blit(shortkey, (580, 800 - 30))
            
            pygame.display.flip()
            clock.tick(Config.fps)
    
    def win(self):
        global quit, ClickOnButton

        Sounds.win_sound.set_volume(0.5)
        Sounds.win_sound.play()

        clock = pygame.time.Clock()
        last_tick = pygame.time.get_ticks()

        Sounds.ghost_move_sound.stop()
        Sounds.dramatic_theme_music_sound.stop()
        
        font = pygame.font.Font(None, 30)
        shortkey = font.render("ESC: Menu  Q: Thoát", True, (255, 0, 0))

        # Font và màu sắc
        font_big = pygame.font.Font("Assets/fonts/arial.ttf", 150)  # Font lớn cho "YOU LOST"
        font_small = pygame.font.Font("Assets/fonts/arial.ttf", 80) # Font cho "SCORE"
        font_button = pygame.font.Font("Assets/fonts/arial.ttf", 40)  # Font cho các nút
        color_text = (0, 0, 0)  # Màu chữ đen
        color_button = (255, 255, 255)  # Màu nền nút trắng
        color_hover = (144, 238, 144)  # Màu hover xanh nhạt

        # Chữ YOU LOST
        font_big = pygame.font.Font(None, 150)  # Chọn font, 150px là kích thước chữ
        you_lose_text = font_big.render("Bạn Thắng", True, (144, 238, 144))  # Chữ đỏ
        you_lose_text_rect = you_lose_text.get_rect(center=(400, 800 * 1 // 4))  # Căn giữa, y = 2/3 chiều cao màn hình
        
        # Chữ SCORE: ...
        font_small = pygame.font.Font(None, 80)
        score_text = f"Điểm: {Config.score}"
        text_score = font_small.render(score_text, True, (255, 255, 255))
        text_score_rect = text_score.get_rect(center=(400, you_lose_text_rect.bottom + 50))

        # Tạo nút (text, x, y, width, height)
        buttons = [
            ("Tiếp tục", 400, text_score_rect.bottom + 50 + 50, 200, 70),
            ("Menu", 400, text_score_rect.bottom + 150 + 50, 200, 70),
            ("Thoát", 400, text_score_rect.bottom + 250 + 50, 200, 70),
        ]

        ClickOnButton = None

        while Config.running and not quit:
            Config.screen.fill('black')

            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Config.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Sounds.click_sound.play()
                        quit = True
                        return
                    if event.key == pygame.K_q:
                        Sounds.click_sound.play()
                        Config.running = False
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for text, x, y, w, h in buttons:
                        if x - w // 2 <= mouse_x <= x + w // 2 and y - h // 2 <= mouse_y <= y + h // 2:
                            ClickOnButton = text 

            EM().maze.draw()
            EM().pacman.setupdrawdir()
            EM().blueGhost.draw()
            EM().pinkGhost.draw()
            EM().orangeGhost.draw()
            EM().redGhost.draw()
            EM().life.draw()
            EM().score.draw()

            overlay = pygame.Surface((Config.width, Config.height))
            overlay.set_alpha(180)  # Độ trong suốt (0: trong suốt hoàn toàn, 255: không trong suốt)
            overlay.fill((0, 0, 0))  # Màu đen
            Config.screen.blit(overlay, (0, 0))

            # Vẽ chữ
            Config.screen.blit(you_lose_text, you_lose_text_rect)
            Config.screen.blit(text_score, text_score_rect)

            # Vẽ nút
            global prevHoverOn, curHoverOn
            curHoverOn = None

            for text, x, y, w, h in buttons:
                is_hovered = x - w // 2 <= mouse_x <= x + w // 2 and y - h // 2 <= mouse_y <= y + h // 2
                color = color_button
                
                if is_hovered:
                    color = color_hover
                    curHoverOn = text

                pygame.draw.rect(Config.screen, color, (x - w // 2, y - h // 2, w, h), border_radius=15)  # Nút bo góc
                text_render = font_button.render(text, True, color_text)
                text_rect = text_render.get_rect(center=(x, y))
                Config.screen.blit(text_render, text_rect)  # Hiển thị chữ trên nút
            
            if curHoverOn != prevHoverOn:
                prevHoverOn = curHoverOn
                if curHoverOn:
                    Sounds.hover_sound.play()

            if ClickOnButton == "Tiếp tục":
                Sounds.click_sound.play()
                return
            elif ClickOnButton == "Menu":
                Sounds.click_sound.play()
                quit = True
                return
            elif ClickOnButton == "Thoát":
                Sounds.click_sound.play()
                Config.running = False
                return
            
            Config.screen.blit(shortkey, (580, 800 - 30))
            
            pygame.display.flip()
            clock.tick(Config.fps)