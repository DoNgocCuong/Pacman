from Levels import *
from Config import Config, Sounds
import pygame

backgroundPath = "Assets/background_menu_game.jpg"

buttonWidth = 300
buttonHeight = 75

exitButtonWidth = 300
exitButtonHeight = 75

buttonX = (Config.width - buttonWidth) / 2

margin_top = 100  # Khoảng cách giữa các hàng
# Tính toán vị trí của các nút Level

buttons = [
    (125, 3 * margin_top, buttonWidth - 100, buttonHeight, "Level 1", Level1(), (0, 0, 255)),  # Màu xanh
    (475, 3 * margin_top, buttonWidth - 100, buttonHeight, "Level 2", Level2(), (255, 105, 180)),  # Màu hồng
    (125, 3 * margin_top + buttonHeight + 50, buttonWidth - 100, buttonHeight, "Level 3", Level3(), (255, 128, 0)),  # Màu cam
    (475, 3 * margin_top + buttonHeight + 50, buttonWidth - 100, buttonHeight, "Level 4", Level4(), (255, 0, 0)),  # Màu đỏ
    (125, 3 * margin_top + 2 * (buttonHeight + 50), buttonWidth - 100, buttonHeight, "Level 5", Level5(), (0, 255, 0)),  # Màu xanh dương
    (475, 3 * margin_top + 2 * (buttonHeight + 50), buttonWidth - 100, buttonHeight, "Level 6", Level6(), (255, 255, 0)),  # Màu vàng
]

exitButtonX = (Config.width - exitButtonWidth) / 2
exitButtonY = 3 * margin_top + 3 * (buttonHeight + 50)  # Đặt bên dưới hàng cuối cùng

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
LIGHT_GRAY = (200, 200, 200)
RED = (200, 0, 0)
LIGHT_RED = (255, 50, 50)
BLACK = (0, 0, 0)
LIGHT_GREEN = (144, 238, 144)  # Màu xanh nhạt (Light Green)

prevHoverOn = None
curHoverOn = None

class Menu:
  def drawBackground(self):
    background = pygame.image.load(backgroundPath)
    bg_width, bg_height = background.get_size()
    # Tính tọa độ để căn giữa ảnh
    bg_x = (Config.width - bg_width) // 2
    bg_y = 0 #(Config.height - bg_height) // 2

    # Vẽ ảnh background lên màn hình
    Config.screen.blit(background, (bg_x, bg_y))
    
    
    bg_width, bg_height = background.get_size()
    screen_width, screen_height = Config.screen.get_size()
    background_resized = pygame.transform.scale(background, (screen_width, screen_height))
    Config.screen.blit(background_resized, (0, 0))
    
    # vẽ banner
    banner = pygame.image.load("Assets/banner.png")
    bn_width, bn_height = banner.get_size()
    banner_x = (Config.width - bn_width) // 2
    banner_y = 100 # (Config.height - bg_height) // 2
    Config.screen.blit(banner, (banner_x, banner_y))

  def drawLevelButtons(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    global curHoverOn, prevHoverOn

    for x, y, width, height, text, level, color in buttons:
        # default_color = color  # Sử dụng màu được chỉ định trong danh sách
        hover_color = WHITE  # Màu khi hover

        text_size = 36

        # Kiểm tra chuột có hover vào nút Level không
        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
            curHoverOn = text
            pygame.draw.rect(Config.screen, hover_color, (x - 2.5, y - 2.5, width + 5, height + 5), border_radius=15)
            text_size = 40
        else:
            pygame.draw.rect(Config.screen, color,(x, y, width, height), border_radius=15)

        font = pygame.font.Font(None, text_size)

        # Hiển thị text trên nút
        text_surface = font.render(text, True, BLACK)
        text_x = x + (width - text_surface.get_width()) / 2
        text_y = y + (height - text_surface.get_height()) / 2
        Config.screen.blit(text_surface, (text_x, text_y))

  def drawExitButton(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    global curHoverOn, prevHoverOn

    # Vẽ nút Exit
    if exitButtonX <= mouse_x <= exitButtonX + exitButtonWidth and 650 <= mouse_y <= 650 + exitButtonHeight:
      curHoverOn = "Exit"
      pygame.draw.rect(Config.screen, LIGHT_RED, (exitButtonX, exitButtonY, exitButtonWidth, exitButtonHeight), border_radius=15)
    else:
      pygame.draw.rect(Config.screen, RED, (exitButtonX, exitButtonY, 300, exitButtonHeight), border_radius=15)

    font = pygame.font.Font(None, 36)

    # Hiển thị văn bản trên nút Exit
    text = "Exit"
    text_surface = font.render(text, True, WHITE)
    text_x = exitButtonX + (exitButtonWidth - text_surface.get_width()) / 2
    text_y = exitButtonY + (exitButtonHeight - text_surface.get_height()) / 2
    Config.screen.blit(text_surface, (text_x, text_y))

  def execute(self):
    global curHoverOn, prevHoverOn

    while Config.running:
      Config.screen.fill(WHITE)
      self.drawBackground()

      curHoverOn = None

      self.drawLevelButtons()
      self.drawExitButton()

      if curHoverOn != prevHoverOn:
        prevHoverOn = curHoverOn
        if curHoverOn != None:
          Sounds.hover_sound.play()

      pygame.display.flip()
      
      mouse_x, mouse_y = pygame.mouse.get_pos()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Config.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Nếu click vào nút Levels
            for x, y, width, height, text, level, color in buttons:
              if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                Sounds.click_sound.play()
                Sounds.beginning_game_sound.stop()
                level.execute()
            # Nếu click Exit
            if exitButtonX <= mouse_x <= exitButtonX + exitButtonWidth and 650 <= mouse_y <= 650 + exitButtonHeight:
              Sounds.click_sound.play()
              Config.running = False
              

    pygame.quit()