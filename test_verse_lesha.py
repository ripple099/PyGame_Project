import pygame
import sys
import random
import time
# --- Настройки ---
WIDTH = 1024
HEIGHT = 1024
FPS = 60
VIEWPORT_WIDTH = 500  # Окно просмотра мира (уменьшено в 2 раза)
VIEWPORT_HEIGHT = 400
# --- Инициализация Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lost in Memory")
clock = pygame.time.Clock()

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

background_image = pygame.image.load("sprites/background_1.png").convert_alpha()
# --- Основной игровой цикл ---
def main():
    start_screen()
    scene = 1
    running = True
    keys = pygame.key.get_pressed()
    player_x = 500
    player_y = 400
    player_speed = 5
    camera_x = 0
    camera_y = 0
    camera_smooth_speed = 1
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

    while running:
        dt = clock.tick(60) / 1000  # Дельта-время

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
            current_player_image = player_images["left"]
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
            current_player_image = player_images["right"]
        if keys[pygame.K_UP]:
            player_y -= player_speed
            current_player_image = player_images["up"]
        if keys[pygame.K_DOWN]:
            player_y += player_speed
            current_player_image = player_images["down"]

        # Центрируем камеру на игроке
        target_camera_x = player_x - VIEWPORT_WIDTH // 2
        target_camera_y = player_y - VIEWPORT_HEIGHT // 2

        # Плавное движение камеры
        camera_x += (target_camera_x - camera_x) * camera_smooth_speed
        camera_y += (target_camera_y - camera_y) * camera_smooth_speed

        # Ограничение камеры

        # Отрисовка фона (с учетом зума)
        screen.fill((255, 255, 255))
        viewport = pygame.Surface((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))  # Виртуальная камера
        viewport.blit(background_image, (-camera_x, -camera_y))

        # Масштабируем всё (эффект "зум камеры")
        scaled_viewport = pygame.transform.scale(viewport, (WIDTH, HEIGHT))
        screen.blit(scaled_viewport, (0, 0))
        screen.blit(current_player_image, (WIDTH // 2, HEIGHT // 2))

        if player_y < 50:
            first_minigame()
            pygame.quit()
            sys.exit()

        pygame.display.flip()
    pygame.quit()
    sys.exit()


def first_minigame():
    surface = pygame.display.set_mode((1024, 1024))
    running = True
    player_speed = 5
    hero_y = HEIGHT // 2
    hero_x = 100
    tick = clock.tick(60)
    timer_interval = 1000 # 0.5 seconds
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event , timer_interval)
    hp = pygame.image.load("sprites/hp.png").convert_alpha()
    hpt = pygame.transform.rotozoom(hp, 0, 0.05)
    hero = pygame.image.load("sprites/geni_right.png").convert_alpha()
    bullet = pygame.image.load('sprites/arrow.png')
    bulletp = pygame.transform.rotozoom(bullet, -90, 0.1)
    enemy_b = pygame.transform.rotozoom(bullet, 90, 0.1)
    drawing = 0
    draw2 = 0
    bullets = []
    bullets_enemy = []
    my_hp = [1, 1, 1, 1, 1]
    enemy_hp = [1, 1, 1, 1, 1]
    enemy_hp_x = 100
    hp_y = 300
    damage = 0
    me_damage = 0
    a = (HEIGHT // 2)

    while running:
        
        surface.fill((0, 0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_e: 
                    drawing = 1
                    sx, sy = 0, 0
                    bullets.append([100, hero_y, sx, sy])
            if event.type == timer_event:
                a = random.randint(50, 850)  
                draw2 = 1
                sxe, sye = 0, 0
                bullets_enemy.append([800, a, sxe, sye])
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            hero_y -= player_speed
        if keys[pygame.K_DOWN]:
            hero_y += player_speed
        if drawing:
            # tick = clock.tick(60)
            for i in range(len(bullets) - 1):
                bullets[i][2] += 200 * tick / 1000
                s2 = bullets[i][0] + bullets[i][2]
                surface.blit(bulletp, (s2, bullets[i][1]))
                if s2 > 1500:
                    del bullets[i]
                if s2 > 800 and s2 < 928 and bullets[i][1] > a and bullets[i][1] < a + 128:
                    damage = 1
        if draw2:
            for i in range(len(bullets_enemy) - 1):
                bullets_enemy[i][2] -= 200 * tick / 1000
                se2 = bullets_enemy[i][0] + bullets_enemy[i][2]
                surface.blit(enemy_b, (se2, bullets_enemy[i][1]))
                if se2 < 0:
                    del bullets_enemy[i]
                if se2 > hero_x and se2 < hero_x + 128 and bullets_enemy[i][1] > hero_y and bullets_enemy[i][1] < hero_y + 128:
                    me_damage = 1
        for j in range(len(enemy_hp)):
            if enemy_hp[j] == 1:
                enemy_hp_x += 50
                surface.blit(hpt, (enemy_hp_x, hp_y))
                
        # if random.randint
        surface.blit(hero, (800, a))
        surface.blit(hero, (hero_x, hero_y))
        pygame.display.flip()
    pygame.quit()
    sys.exit()


        


if __name__ == "__main__":
    main()
import datetime

