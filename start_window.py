from settings import *
import pygame
import sys

def start_screen():
    title_font = pygame.font.Font(None, 64)
    menu_font = pygame.font.Font(None, 36)
    title_text = title_font.render("Lost in Memory", True, (255, 255, 255))
    options = ["начать", "", "выход"]
    selected = 0

    while True:
        screen.fill((0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (150, 150, 150)
            option_text = menu_font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 50))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_RETURN:
                    if options[selected] == "начать":
                        return "game"
                    if options[selected] == "выход":
                        pygame.quit()
                        sys.exit()
                    if options[selected] == "хз_чо":
                        pass