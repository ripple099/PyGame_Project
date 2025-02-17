# # import pygame
# # import sys

# # # Инициализация Pygame
# # pygame.init()

# # # Настройки окна
# # SCREEN_WIDTH = 800  # Размер экрана (не меняем)
# # SCREEN_HEIGHT = 600
# # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# # pygame.display.set_caption("Камера с уменьшенным зумом")

# # # Настройки "виртуального окна" (чем меньше, тем сильнее зум)
# # VIEWPORT_WIDTH = 400  # Окно просмотра мира (уменьшено в 2 раза)
# # VIEWPORT_HEIGHT = 300
# # camera_zoom = 2  # Коэффициент зума (больше = меньше объектов)

# # # Цвета
# # WHITE = (255, 255, 255)
# # BLUE = (0, 0, 255)

# # # Игрок
# # player_width = 20  # Размер уменьшен в 2 раза
# # player_height = 30
# # player_x = 500
# # player_y = 400
# # player_speed = 5

# # # Мир (карта)
# # world_width = 2000
# # world_height = 2000

# # # Камера
# # camera_x = 0
# # camera_y = 0
# # camera_smooth_speed = 1

# # # Загрузка фона (масштабируем)
# # background_image = pygame.image.load("sprites/background_1.png").convert_alpha()
# # background_image = pygame.transform.scale(background_image, (world_width, world_height))

# # # Основной цикл
# # clock = pygame.time.Clock()
# # running = True

# # while running:
# #     dt = clock.tick(60) / 1000  # Дельта-время

# #     # Обработка событий
# #     for event in pygame.event.get():
# #         if event.type == pygame.QUIT:
# #             running = False

# #     # Управление игроком
# #     keys = pygame.key.get_pressed()
# #     if keys[pygame.K_a]:
# #         player_x -= player_speed
# #     if keys[pygame.K_d]:
# #         player_x += player_speed
# #     if keys[pygame.K_w]:
# #         player_y -= player_speed
# #     if keys[pygame.K_s]:
# #         player_y += player_speed

# #     # Центрируем камеру на игроке
# #     target_camera_x = player_x - VIEWPORT_WIDTH // 2
# #     target_camera_y = player_y - VIEWPORT_HEIGHT // 2

# #     # Плавное движение камеры
# #     camera_x += (target_camera_x - camera_x) * camera_smooth_speed
# #     camera_y += (target_camera_y - camera_y) * camera_smooth_speed

# #     # Ограничение камеры

# #     # Отрисовка фона (с учетом зума)
# #     screen.fill(WHITE)
# #     viewport = pygame.Surface((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))  # Виртуальная камера
# #     viewport.blit(background_image, (-camera_x, -camera_y))

# #     # Отрисовка игрока (уменьшенного)
# #     player_rect = pygame.Rect(
# #         player_x - camera_x,
# #         player_y - camera_y,
# #         player_width,
# #         player_height
# #     )
# #     # pygame.draw.rect(viewport, BLUE, player_rect)

# #     # Масштабируем всё (эффект "зум камеры")
# #     scaled_viewport = pygame.transform.scale(viewport, (SCREEN_WIDTH, SCREEN_HEIGHT))
# #     screen.blit(scaled_viewport, (0, 0))

# #     pygame.display.flip()

# # pygame.quit()
# # sys.exit()

# import pygame
# import random

# # Инициализация
# pygame.init()
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# clock = pygame.time.Clock()

# # Цвета
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# ORANGE = (255, 165, 0)
# BLUE = (0, 120, 255)

# # Игрок
# player = pygame.Rect(400, 300, 30, 40)
# player_speed_x = 0
# player_speed_y = 0
# GRAVITY = 0.3
# JUMP_FORCE = -8
# ON_GROUND = False

# # Платформы
# platforms = [
#     pygame.Rect(0, HEIGHT-40, WIDTH, 40),
#     pygame.Rect(200, 400, 100, 20),
#     pygame.Rect(500, 300, 100, 20)
# ]

# # Основной цикл
# running = True
# while running:
#     screen.fill(BLACK)
    
#     # События
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE and ON_GROUND:
#                 player_speed_y = JUMP_FORCE
#                 ON_GROUND = False

#     # Движение игрока
#     keys = pygame.key.get_pressed()
#     player_speed_x = (keys[pygame.K_d] - keys[pygame.K_a]) * 5
#     player.x += player_speed_x
#     player.y += player_speed_y
#     player_speed_y += GRAVITY

#     # Коллизия с платформами
#     ON_GROUND = False
#     for platform in platforms:
#         if player.colliderect(platform):
#             if player_speed_y > 0:
#                 ON_GROUND = True
#                 player_speed_y = 0
#                 player.bottom = platform.top

#     # Отрисовка
#     pygame.draw.rect(screen, BLUE, player)
#     for platform in platforms:
#         pygame.draw.rect(screen, ORANGE, platform)
    
#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()

# Python program to move the image
# with the mouse

# Import the library pygame


# import pygame
# from pygame.locals import *

# # Take colors input
# YELLOW = (255, 255, 0)
# BLUE = (0, 0, 255)

# # Construct the GUI game
# pygame.init()

# # Set dimensions of game GUI
# w, h = 640, 350
# screen = pygame.display.set_mode((w, h))

# # Take image as input
# img = pygame.image.load('geni.png')
# img.convert()

# # Draw rectangle around the image
# rect = img.get_rect()
# rect.center = w//2, h//2

# # Set running and moving values
# running = True
# moving = False

# # Setting what happens when game 
# # is in running state
# while running:
	
# 	for event in pygame.event.get():

# 		# Close if the user quits the 
# 		# game
# 		if event.type == QUIT:
# 			running = False

# 		# Making the image move
# 		elif event.type == MOUSEBUTTONDOWN:
# 			if rect.collidepoint(event.pos):
# 				moving = True

# 		# Set moving as False if you want 
# 		# to move the image only with the 
# 		# mouse click
# 		# Set moving as True if you want 
# 		# to move the image without the 
# 		# mouse click
# 		elif event.type == MOUSEBUTTONUP:
# 			moving = False

# 		# Make your image move continuously
# 		elif event.type == MOUSEMOTION and moving:
# 			rect.move_ip(event.rel)

# 	# Set screen color and image on screen
# 	screen.fill(YELLOW)
# 	screen.blit(img, rect)

# 	# Construct the border to the image
# 	pygame.draw.rect(screen, BLUE, rect, 2)

# 	# Update the GUI pygame
# 	pygame.display.update()

# # Quit the GUI game
# pygame.quit()
import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle Game")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Параметры пазла
ROWS, COLS = 4, 4  # Усложненный пазл
PUZZLE_SIZE = 400
TILE_SIZE = PUZZLE_SIZE // ROWS
SNAP_THRESHOLD = 15  # Чувствительность притягивания

class PuzzlePiece:
    def __init__(self, image, correct_pos, number):
        self.image = image
        self.correct_pos = correct_pos
        self.number = number
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(50, WIDTH - TILE_SIZE - 50),
                              random.randint(50, HEIGHT - TILE_SIZE - 50))
        self.dragging = False
        self.correct = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if not self.correct:
            # Отображение номера кусочка
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.number), True, RED)
            surface.blit(text, self.rect.move(5, 5))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.correct:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.offset_x = self.rect.x - event.pos[0]
                self.offset_y = self.rect.y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            self.dragging = False
            # Проверка правильности позиции
            distance = pygame.math.Vector2(
                self.rect.x - self.correct_pos[0],
                self.rect.y - self.correct_pos[1]
            ).length()
            
            if distance < SNAP_THRESHOLD:
                self.rect.topleft = self.correct_pos
                self.correct = True

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.rect.x = event.pos[0] + self.offset_x
            self.rect.y = event.pos[1] + self.offset_y

def load_puzzle_image(path):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (PUZZLE_SIZE, PUZZLE_SIZE))
    return image

def show_victory_screen(surface):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 128))
    surface.blit(overlay, (0, 0))
    
    font = pygame.font.Font(None, 74)
    text = font.render('ПОБЕДА!', True, GREEN)
    surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 40))
    
    font = pygame.font.Font(None, 36)
    text = font.render('Нажмите R для новой игры', True, BLACK)
    surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 20))

def main():
    image = load_puzzle_image("sprites/image1.png")  # Укажите свой путь
    
    pieces = []
    numbers = list(range(1, ROWS*COLS + 1))
    
    for y in range(ROWS):
        for x in range(COLS):
            tile = image.subsurface(x*TILE_SIZE, y*TILE_SIZE,
                                   TILE_SIZE, TILE_SIZE)
            correct_pos = (WIDTH//2 - PUZZLE_SIZE//2 + x*TILE_SIZE,
                          HEIGHT//2 - PUZZLE_SIZE//2 + y*TILE_SIZE)
            pieces.append(PuzzlePiece(tile, correct_pos, numbers.pop(0)))

    random.shuffle(pieces)
    victory = False
    clock = pygame.time.Clock()
    
    running = True
    while running:
        WIN.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and victory:
                    main()
                    return
            
            for piece in pieces:
                piece.update(event)

        # Отрисовка
        for piece in pieces:
            piece.draw(WIN)
            if piece.correct:
                pygame.draw.rect(WIN, GREEN, piece.rect, 3)

        # Проверка победы
        victory = all(piece.correct for piece in pieces)
        if victory:
            show_victory_screen(WIN)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()