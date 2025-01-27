import pygame
import sys

# --- Настройки ---
WIDTH = 1024
HEIGHT = 1024
FPS = 60

# --- Инициализация Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lost in Memory")
clock = pygame.time.Clock()

# --- Загрузка спрайтов ---
player_image_left = pygame.image.load("sprites/geni_left.png").convert_alpha()
player_image_right = pygame.image.load("sprites/geni_right.png").convert_alpha()
player_image_back = pygame.image.load("sprites/geni_back.png").convert_alpha()
player_image_front = pygame.image.load("sprites/geni_front.png").convert_alpha()

player_images = {
    "left": player_image_left,
    "right": player_image_right,
    "up": player_image_back,
    "down": player_image_front
}

current_player_image = player_image_front
player_rect = current_player_image.get_rect()
player_rect.topleft = (WIDTH // 2, HEIGHT // 2)


# --- Экран входа в игру ---
def start_screen():
    title_font = pygame.font.Font(None, 64)
    menu_font = pygame.font.Font(None, 36)
    title_text = title_font.render("Lost in Memory", True, (255, 255, 255))
    options = ["начать", "хз_чо", "выход"]
    selected = 0

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        for i, option in enumerate(options):
            if i == selected:
                color = (255, 255, 0) 
            else:
                color = (150, 150, 150)
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
                        running = False
                    if options[selected] == "выход":
                        pygame.quit()
                        sys.exit()

# --- Управление персонажем ---
def handle_keys(player_rect):
    global current_player_image
    keys = pygame.key.get_pressed()
    speed = 4

    if keys[pygame.K_LEFT]:
        if player_rect.x <= 80 and (player_rect.y <= 464 or player_rect.y >= 492):
            pass
        else:
            player_rect.x -= speed
        current_player_image = player_images["left"]
        print(player_rect.x, player_rect.y)
    if keys[pygame.K_RIGHT]:
        if player_rect.x >= 820 and (player_rect.y <= 464 or player_rect.y >= 492):
            pass
        else:
            player_rect.x += speed
            current_player_image = player_images["right"]
            print(player_rect.x, player_rect.y)
    if keys[pygame.K_UP]:
        if (player_rect.y <= 120 and (player_rect.x <= 384 or player_rect.x >= 524)) or player_rect.x < 75 or player_rect.x > 820:
            pass
        else:
            player_rect.y -= speed
            current_player_image = player_images["up"]
            print(player_rect.x, player_rect.y)
    if keys[pygame.K_DOWN]:
        if player_rect.y >= 800 or player_rect.x < 75 or player_rect.x > 820:
            pass
        else:
            player_rect.y += speed
            current_player_image = player_images["down"]
            print(player_rect.x, player_rect.y)
    if player_rect.y < 50:
        player_rect.y = 100
        start_screen()
        


background_image = pygame.image.load("sprites/background_1.png").convert_alpha()
sign = pygame.image.load('sprites/arrow.png')
resized_arrow = pygame.transform.scale(sign, (100, 100))
arrow_rigth = pygame.transform.rotate(resized_arrow, -90)
arrow_left = pygame.transform.rotate(resized_arrow, 90)

# --- Основной игровой цикл ---
def main():
    start_screen()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_keys(player_rect)
        screen.fill((0, 0, 0))  # Очистка экрана

        # Отрисовка фона
        screen.blit(background_image, (0, 0))
        screen.blit(resized_arrow, (465, 200))
        screen.blit(arrow_left, (175, 500))
        screen.blit(arrow_rigth, (775, 500))

        # Отрисовка игрока
        screen.blit(current_player_image, player_rect)

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
