from Config import Config, Sounds
import pygame

BoxWidth = 400
BoxHeight = 220

boxX = (Config.width - BoxWidth) / 2
boxY = 100

ButtonWidth = (BoxWidth - 6 * 10) / 5
ButtonHeight = 30
ButtonX = boxX + 10
ButtonY = boxY + 22 + 160

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font("Assets/fonts/arial.ttf", 20)

prevHoverOn = None
curHoverOn = None

class ExperimentBox:
    def showResultBoard(self, algorithm, search_time, memory_usage , num_expanded_nodes):
        pygame.draw.rect(Config.screen, (44,10 ,40), (boxX, boxY, BoxWidth, BoxHeight), border_radius=15)

        algorithm_text = font.render(f"Thuật toán: {algorithm}", True, WHITE)
        search_time_text = font.render(f"Thời gian: {search_time * 1000:.4f} mili giây", True, WHITE)
        memory_usage_text = font.render(f"Bộ nhớ: {memory_usage * 1024:.4f} KB", True, WHITE)
        num_expanded_nodes_text = font.render(f"Số bước mở rộng : {num_expanded_nodes}", True, WHITE)
        pick_testcase_text = font.render("Thử các vị trí khác ", True, WHITE)
            
        Config.screen.blit(algorithm_text, (boxX + 24, boxY + 22))
        Config.screen.blit(search_time_text, (boxX + 24, boxY + 22 + 30))
        Config.screen.blit(memory_usage_text, (boxX + 24, boxY + 22 + 60))
        Config.screen.blit(num_expanded_nodes_text, (boxX + 24, boxY + 22 + 90))
        pygame.draw.line(Config.screen, (0, 0, 0), (boxX + 24, boxY + 22 + 120), (boxX + BoxWidth - 24, boxY + 22 + 120), 2)
        Config.screen.blit(pick_testcase_text, (boxX + 100, boxY + 22 + 130))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        global prevHoverOn, curHoverOn
        curHoverOn = None

        for i in range(5):
            button_x = ButtonX + i * (10 + ButtonWidth)
            button_y = ButtonY
            button_color = 'WHITE'

            if button_x <= mouse_x <= button_x + ButtonWidth and button_y <= mouse_y <= button_y + ButtonHeight:
                curHoverOn = i
                button_color = (144, 238, 144) # Màu xanh lục nhạt
            
            pygame.draw.rect(Config.screen, 'BLACK', (button_x - 2, button_y - 2, ButtonWidth + 4, ButtonHeight + 4), border_radius=15)
            pygame.draw.rect(Config.screen, button_color, (button_x, button_y, ButtonWidth, ButtonHeight), border_radius=15)
            
            id = font.render(f"{i + 1}", True, BLACK)
            Config.screen.blit(id, (ButtonX + i * (10 + ButtonWidth) + ButtonWidth / 2 - 6, ButtonY + 5))
        
        if curHoverOn != prevHoverOn:
            prevHoverOn = curHoverOn
            if curHoverOn != None:
                Sounds.hover_sound.play()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Config.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return -1 # quit level signal
                if event.key == pygame.K_q:
                    Config.running = False
                    return -1 # quit level ssignal
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 là chuột trái
                for i in range(5):
                    button_x = ButtonX + i * (10 + ButtonWidth)
                    button_y = ButtonY
                    if button_x <= mouse_x <= button_x + ButtonWidth and button_y <= mouse_y <= button_y + ButtonHeight:
                        Sounds.click_sound.play()
                        return i
        
        return None
