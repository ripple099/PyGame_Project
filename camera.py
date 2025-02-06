# import pygame
# import sys

# # Инициализация Pygame
# pygame.init()

# # Настройки окна
# SCREEN_WIDTH = 800  # Размер экрана (не меняем)
# SCREEN_HEIGHT = 600
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Камера с уменьшенным зумом")

# # Настройки "виртуального окна" (чем меньше, тем сильнее зум)
# VIEWPORT_WIDTH = 400  # Окно просмотра мира (уменьшено в 2 раза)
# VIEWPORT_HEIGHT = 300
# camera_zoom = 2  # Коэффициент зума (больше = меньше объектов)

# # Цвета
# WHITE = (255, 255, 255)
# BLUE = (0, 0, 255)

# # Игрок
# player_width = 20  # Размер уменьшен в 2 раза
# player_height = 30
# player_x = 500
# player_y = 400
# player_speed = 5

# # Мир (карта)
# world_width = 2000
# world_height = 2000

# # Камера
# camera_x = 0
# camera_y = 0
# camera_smooth_speed = 1

# # Загрузка фона (масштабируем)
# background_image = pygame.image.load("sprites/background_1.png").convert_alpha()
# background_image = pygame.transform.scale(background_image, (world_width, world_height))

# # Основной цикл
# clock = pygame.time.Clock()
# running = True

# while running:
#     dt = clock.tick(60) / 1000  # Дельта-время

#     # Обработка событий
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Управление игроком
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_a]:
#         player_x -= player_speed
#     if keys[pygame.K_d]:
#         player_x += player_speed
#     if keys[pygame.K_w]:
#         player_y -= player_speed
#     if keys[pygame.K_s]:
#         player_y += player_speed

#     # Центрируем камеру на игроке
#     target_camera_x = player_x - VIEWPORT_WIDTH // 2
#     target_camera_y = player_y - VIEWPORT_HEIGHT // 2

#     # Плавное движение камеры
#     camera_x += (target_camera_x - camera_x) * camera_smooth_speed
#     camera_y += (target_camera_y - camera_y) * camera_smooth_speed

#     # Ограничение камеры

#     # Отрисовка фона (с учетом зума)
#     screen.fill(WHITE)
#     viewport = pygame.Surface((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))  # Виртуальная камера
#     viewport.blit(background_image, (-camera_x, -camera_y))

#     # Отрисовка игрока (уменьшенного)
#     player_rect = pygame.Rect(
#         player_x - camera_x,
#         player_y - camera_y,
#         player_width,
#         player_height
#     )
#     # pygame.draw.rect(viewport, BLUE, player_rect)

#     # Масштабируем всё (эффект "зум камеры")
#     scaled_viewport = pygame.transform.scale(viewport, (SCREEN_WIDTH, SCREEN_HEIGHT))
#     screen.blit(scaled_viewport, (0, 0))

#     pygame.display.flip()

# pygame.quit()
# sys.exit()

import pygame
import random

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
BLUE = (0, 120, 255)

# Игрок
player = pygame.Rect(400, 300, 30, 40)
player_speed_x = 0
player_speed_y = 0
GRAVITY = 0.3
JUMP_FORCE = -8
ON_GROUND = False

# Платформы
platforms = [
    pygame.Rect(0, HEIGHT-40, WIDTH, 40),
    pygame.Rect(200, 400, 100, 20),
    pygame.Rect(500, 300, 100, 20)
]

# Основной цикл
running = True
while running:
    screen.fill(BLACK)
    
    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ON_GROUND:
                player_speed_y = JUMP_FORCE
                ON_GROUND = False

    # Движение игрока
    keys = pygame.key.get_pressed()
    player_speed_x = (keys[pygame.K_d] - keys[pygame.K_a]) * 5
    player.x += player_speed_x
    player.y += player_speed_y
    player_speed_y += GRAVITY

    # Коллизия с платформами
    ON_GROUND = False
    for platform in platforms:
        if player.colliderect(platform):
            if player_speed_y > 0:
                ON_GROUND = True
                player_speed_y = 0
                player.bottom = platform.top

    # Отрисовка
    pygame.draw.rect(screen, BLUE, player)
    for platform in platforms:
        pygame.draw.rect(screen, ORANGE, platform)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()