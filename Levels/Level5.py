from Entities.Entity import Entity
from EntitiesManager import EntitiesManager as EM
from Config import Config, Object, Sounds, Board, Material
import pygame
from .Level1 import Level1
from .Level2 import Level2
from .Level3 import Level3
from .Level4 import Level4


start = False
quit = False
PacmanGetCaught = False

isSettingPos = True
EntityNames = ["Pacman", "BlueGhost", "PinkGhost", "OrangeGhost", "RedGhost"]
EntityBeingSetIndex = 0

prevHoverOn = None
curHoverOn = None

class Level5():
    def __init__(self):
        pass

    def setup(self):
        global PacmanGetCaught, quit, start, isSettingPos, EntityBeingSetIndex

        Board.maze = [row[:] for row in Board.initMaze]

        PacmanGetCaught = False
        quit = False
        start = False
        isSettingPos = True
        EntityBeingSetIndex = 0

        # Setup tọa độ ma trận
        Object.blueGhostX = -1#6
        Object.blueGhostY = -1#2
        Object.pinkGhostX = -1#30
        Object.pinkGhostY = -1#27
        Object.orangeGhostX = -1#21#27
        Object.orangeGhostY = -1#4#3
        Object.redGhostX = -1#21
        Object.redGhostY = -1#3
        Object.pacmanX = -1#15
        Object.pacmanY = -1#21

        #Setup tọa độ thực
        (Object.realPacmanX, Object.realPacmanY) = Entity.getRealCoordinates((Object.pacmanX, Object.pacmanY), Object.PACMAN_SIZE)
        (Object.realRedGhostX, Object.realRedGhostY) = Entity.getRealCoordinates((Object.redGhostX, Object.redGhostY), Object.RED_GHOST_SIZE)
        (Object.realOrangeGhostX, Object.realOrangeGhostY) = Entity.getRealCoordinates((Object.orangeGhostX, Object.orangeGhostY), Object.ORANGE_GHOST_SIZE)
        (Object.realPinkGhostX, Object.realPinkGhostY) = Entity.getRealCoordinates((Object.pinkGhostX, Object.pinkGhostY), Object.PINK_GHOST_SIZE)
        (Object.realBlueGhostX, Object.realBlueGhostY) = Entity.getRealCoordinates((Object.blueGhostX, Object.blueGhostY), Object.BLUE_GHOST_SIZE)

        for i in range(len(Board.coordinates)):
            for j in range(len(Board.coordinates[i])):
                Board.coordinates[i][j] = Board.BLANK

    def isCaught(self):
        pacmanPos = (Object.pacmanX, Object.pacmanY)
        blueGhostPos = (Object.blueGhostX, Object.blueGhostY)
        pinkGhostPos = (Object.pinkGhostX, Object.pinkGhostY)
        redGhostPos = (Object.redGhostX, Object.redGhostY)
        orangeGhostPos = (Object.orangeGhostX, Object.orangeGhostY)
        return pacmanPos in (blueGhostPos, pinkGhostPos, redGhostPos, orangeGhostPos)

    def settingPosProcess(self, entityName):
        global EntityBeingSetIndex
        
        px, py = Config.p_height, Config.p_width

        mouse_y, mouse_x = pygame.mouse.get_pos()

        for x in range(len(Board.initMaze)):
            for y in range(len(Board.initMaze[x])):
                if (x, y) in ((Object.pacmanX, Object.pacmanY), \
                                (Object.blueGhostX, Object.blueGhostY), \
                                (Object.pinkGhostX, Object.pinkGhostY), \
                                (Object.orangeGhostX, Object.orangeGhostY), \
                                (Object.redGhostX, Object.redGhostY)) \
                or Board.initMaze[x][y] > 2:
                    continue
                if x * px < mouse_x < (x + 1) * px and y * py < mouse_y < (y + 1) * py:
                    if entityName == "Pacman":
                        (realX, realY) = Entity.getRealCoordinates((x, y), Object.PACMAN_SIZE)
                        Config.screen.blit(Material.Pacman1Image, (realY, realX))
                    elif entityName == "BlueGhost":
                        (realX, realY) = Entity.getRealCoordinates((x, y), Object.BLUE_GHOST_SIZE)
                        Config.screen.blit(Material.BlueGhostImage, (realY, realX))
                    elif entityName == "PinkGhost":
                        (realX, realY) = Entity.getRealCoordinates((x, y), Object.PINK_GHOST_SIZE)
                        Config.screen.blit(Material.PinkGhostImage, (realY, realX))
                    elif entityName == "OrangeGhost":
                        (realX, realY) = Entity.getRealCoordinates((x, y), Object.ORANGE_GHOST_SIZE)
                        Config.screen.blit(Material.OrangeGhostImage, (realY, realX))
                    elif entityName == "RedGhost":
                        (realX, realY) = Entity.getRealCoordinates((x, y), Object.RED_GHOST_SIZE)
                        Config.screen.blit(Material.RedGhostImage, (realY, realX))

    def execute(self):
        global PacmanGetCaught, quit, start, EntityBeingSetIndex, isSettingPos, quit

        quit = False
        
        font = pygame.font.Font("Assets/fonts/arial.ttf", 20)
        shortkey = font.render("ESC: Menu  Q: Thoát", True, (255, 0,0))
        red=Level4()
        pink=Level2()
        orange=Level3()
        blue=Level1()
        

        while Config.running and not quit:
            self.setup()
            clock = pygame.time.Clock()

            countFrames = 0
            
            Sounds.dramatic_theme_music_sound.set_volume(0.1)
            Sounds.dramatic_theme_music_sound.play(loops=-1)

            px, py = Config.p_height, Config.p_width

            while Config.running and not quit:
                Config.screen.fill('black')

                mouse_y, mouse_x = pygame.mouse.get_pos()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Sounds.ghost_move_sound.stop()
                        Sounds.dramatic_theme_music_sound.stop()
                        Config.running = False
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            Sounds.click_sound.play()
                            Sounds.ghost_move_sound.stop()
                            Sounds.dramatic_theme_music_sound.stop()
                            quit = True
                            return
                        if event.key == pygame.K_q:
                            Sounds.click_sound.play()
                            Sounds.ghost_move_sound.stop()
                            Sounds.dramatic_theme_music_sound.stop()
                            Config.running = False
                            return
                        if event.key == pygame.K_SPACE:
                            if not isSettingPos and not start:
                                Sounds.ghost_move_sound.play(loops=-1)  # Lặp vô hạn
                                start = True
                    if isSettingPos:
                        entityName = EntityNames[EntityBeingSetIndex]
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            for x in range(len(Board.initMaze)):
                                for y in range(len(Board.initMaze[x])):
                                    if (x,y) in ((Object.pacmanX, Object.pacmanY), \
                                                    (Object.blueGhostX, Object.blueGhostY), \
                                                    (Object.pinkGhostX, Object.pinkGhostY), \
                                                    (Object.orangeGhostX, Object.orangeGhostY), \
                                                    (Object.redGhostX, Object.redGhostY)) \
                                    or Board.initMaze[x][y] > 2:
                                        continue
                                    if x * px < mouse_x < (x + 1) * px and y * py < mouse_y < (y + 1) * py:
                                        Sounds.click_sound.play()
                                        if entityName == "Pacman":
                                            (realX, realY) = Entity.getRealCoordinates((x, y), Object.PACMAN_SIZE)
                                            Object.pacmanX, Object.pacmanY = x, y
                                            Object.realPacmanX, Object.realPacmanY = realX, realY
                                            Board.coordinates[x][y] = Board.PACMAN
                                            EntityBeingSetIndex += 1
                                        elif entityName == "BlueGhost":
                                            (realX, realY) = Entity.getRealCoordinates((x, y), Object.BLUE_GHOST_SIZE)
                                            Object.blueGhostX, Object.blueGhostY = x, y
                                            Object.realBlueGhostX, Object.realBlueGhostY = realX, realY
                                            Board.coordinates[x][y] = Board.BLUE_GHOST
                                            EntityBeingSetIndex += 1
                                        elif entityName == "PinkGhost":
                                            (realX, realY) = Entity.getRealCoordinates((x, y), Object.PINK_GHOST_SIZE)
                                            Object.pinkGhostX, Object.pinkGhostY = x, y
                                            Object.realPinkGhostX, Object.realPinkGhostY = realX, realY
                                            Board.coordinates[x][y] = Board.PINK_GHOST
                                            EntityBeingSetIndex += 1
                                        elif entityName == "OrangeGhost":
                                            (realX, realY) = Entity.getRealCoordinates((x, y), Object.ORANGE_GHOST_SIZE)
                                            Object.orangeGhostX, Object.orangeGhostY = x, y
                                            Object.realOrangeGhostX, Object.realOrangeGhostY = realX, realY
                                            Board.coordinates[x][y] = Board.ORANGE_GHOST
                                            EntityBeingSetIndex += 1
                                        elif entityName == "RedGhost":
                                            (realX, realY) = Entity.getRealCoordinates((x, y), Object.RED_GHOST_SIZE)
                                            Object.redGhostX, Object.redGhostY = x, y
                                            Object.realRedGhostX, Object.realRedGhostY = realX, realY
                                            Board.coordinates[x][y] = Board.RED_GHOST
                                            EntityBeingSetIndex += 1
                EM().maze.draw()
            
                if isSettingPos:
                    if EntityBeingSetIndex < len(EntityNames):
                        self.settingPosProcess(EntityNames[EntityBeingSetIndex])
                    else:
                        isSettingPos = False
                
                EM().pacman.draw()
                EM().blueGhost.draw()
                EM().pinkGhost.draw()
                EM().orangeGhost.draw()
                EM().redGhost.draw()

                if not start and not isSettingPos:
                    overlay = pygame.Surface((Config.width, Config.height))
                    overlay.set_alpha(180)  # Độ trong suốt (0: trong suốt hoàn toàn, 255: không trong suốt)
                    overlay.fill((0, 0, 0))  # Màu đen
                    Config.screen.blit(overlay, (0, 0))

                    color = (255, 255, 255 - countFrames % 30 * 8)
                    labelFont =pygame.font.Font("Assets/fonts/arial.ttf", 20)
                    space_to_start = labelFont.render("SPACE để bắt đầu trò chơi", True, color)
                    Config.screen.blit(space_to_start, (Config.width / 2 - 130, Config.height / 2 - 50))

                if start and not isSettingPos and not PacmanGetCaught:
                    if countFrames % 15 == 0:
                        blue.updatePos()
                        pink.updatePos()
                        orange.updatePos()
                        red.updatePos()
                    PacmanGetCaught = self.isCaught()
                    EM().blueGhost.move()
                    EM().pinkGhost.move()
                    EM().orangeGhost.move()
                    EM().redGhost.move()

                Config.screen.blit(shortkey, (580, 800 - 30))

                pygame.display.flip()
                clock.tick(Config.fps)
                countFrames += 1

                if PacmanGetCaught:
                    Sounds.ghost_move_sound.stop()
                    Sounds.dramatic_theme_music_sound.stop()
                    break
            self.finish()
                
    def finish(self):
        global quit, ClickOnButton

        clock = pygame.time.Clock()
        last_tick = pygame.time.get_ticks()

        Sounds.ghost_move_sound.stop()
        Sounds.dramatic_theme_music_sound.stop()

        Sounds.win_sound.set_volume(0.5)
        Sounds.win_sound.play()
        
        # Hướng dẫn phím tắt
        font = pygame.font.Font(None, 30)
        shortkey = font.render("ESC: Menu  Q: Thoát", True, (255,0, 0))

        # Font và màu sắc
        font_big = pygame.font.Font(None, 150)  # Font lớn cho "YOU LOST"
        font_small = pygame.font.Font(None, 80)  # Font cho "SCORE"
        font_button = pygame.font.Font(None, 40)  # Font cho các nút
        color_text = (0, 0, 0)  # Màu chữ đen
        color_button = (255, 255, 255)  # Màu nền nút trắng
        color_hover = (144, 238, 144)  # Màu hover xanh nhạt

        # Chữ YOU LOST
        font_big = pygame.font.Font(None, 70)  # Chọn font, 150px là kích thước chữ
        finish_text = font_big.render("Bạn đã thua", True, (144, 238, 144))  # Chữ đỏ
        finish_text_rect = finish_text.get_rect(center=(400, 800 * 1 // 4))  # Căn giữa, y = 2/3 chiều cao màn hình
        
        # Tạo nút (text, x, y, width, height)
        buttons = [
            ("Tiếp tục", 400, finish_text_rect.bottom + 50 + 50, 200, 70),
            ("Menu", 400, finish_text_rect.bottom + 150 + 50, 200, 70),
            ("Thoát", 400, finish_text_rect.bottom + 250 + 50, 200, 70),
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

            overlay = pygame.Surface((Config.width, Config.height))
            overlay.set_alpha(180)  # Độ trong suốt (0: trong suốt hoàn toàn, 255: không trong suốt)
            overlay.fill((0, 0, 0))  # Màu đen
            Config.screen.blit(overlay, (0, 0))

            # Vẽ chữ
            Config.screen.blit(finish_text, finish_text_rect)

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

            if ClickOnButton == "Again":
                Sounds.click_sound.play()
                return
            elif ClickOnButton == "Menu":
                Sounds.click_sound.play()
                quit = True
                return
            elif ClickOnButton == "Quit":
                Sounds.click_sound.play()
                Config.running = False
                return
            
            Config.screen.blit(shortkey, (580, 800 - 30))

            pygame.display.flip()
            clock.tick(Config.fps)