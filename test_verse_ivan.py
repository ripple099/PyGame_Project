# npc_question = "Чиваува пацанчик, как бы назвал свою команду?"
# correct_answer = "zxc1337"
# npc_response_correct = "Я как Снайпер: сразу приметил тебя издалека. ХАРОШ(ИЛЮХА)"
# npc_response_incorrect = "mda ... :/"
# pygame.mixer.music.load('songs/dota.mp3')
# pygame.mixer.music.set_volume(0.15)
# pygame.mixer.music.play()
from sprites import *
import pygame
import sys
import pytmx
# import random

# Константы
SCALE = 2
WIDTH, HEIGHT = 1024, 768
FPS = 60

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Параметры диалога
npc_question = "Чиваува пацанчик, как бы назвал свою команду?"
correct_answer = "zxc1337"
npc_response_correct = "Я как Снайпер: сразу приметил тебя издалека. ХАРОШ(ИЛЮХА)"
npc_response_incorrect = "mda ... :/"
pygame.mixer.music.load('songs/dota.mp3')
pygame.mixer.music.set_volume(0.15)

# Переменные для текстового поля
input_box = pygame.Rect(100, 500, 600, 40)
input_color_inactive = pygame.Color('lightskyblue3')
input_color_active = pygame.Color('dodgerblue2')
input_color = input_color_inactive
input_text = ''
input_active = False
show_dialog = False
npc_response = ""

def run_dialog():
    global input_text, input_active, input_color, show_dialog, npc_response

    running = True
    while running:
        screen.fill((30, 30, 30))

        # Отображение текста NPC
        npc_surface = font.render(npc_question, True, (255, 255, 255))
        screen.blit(npc_surface, (100, 100))

        # Отображение ответа NPC (если есть)
        if npc_response:
            response_surface = font.render(npc_response, True, (255, 255, 255))
            screen.blit(response_surface, (100, 200))

        # Отображение введенного текста игрока
        player_surface = font.render(input_text, True, (255, 255, 255))
        screen.blit(player_surface, (100, 400))

        # Отрисовка текстового поля
        pygame.draw.rect(screen, input_color, input_box, 2)
        txt_surface = font.render(input_text, True, input_color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip().lower() == correct_answer.lower():
                        npc_response = npc_response_correct
                    else:
                        npc_response = npc_response_incorrect
                        pygame.mixer.music.play()
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:  # Теперь Escape закрывает окно диалога
                    show_dialog = False
                    running = False
                    pygame.mixer.music.stop()
                else:
                    input_text += event.unicode


def game_loop(x, y):
    global show_dialog

    # Загрузка карты
    tmx_data = pytmx.load_pygame("pygame_map/map.tmx")
    TILE_SIZE = tmx_data.tilewidth * SCALE

    # Игрок
    player_size = TILE_SIZE
    player_x, player_y = 1850, 2300
    player_speed = 4 * SCALE
    current_player_image = pygame.transform.scale(player_images["down"], (player_size, player_size))

    # NPC
    npc_x, npc_y = 2722, 900
    npc_image = pygame.image.load("sprites/ghoul.png").convert_alpha()
    npc_image = pygame.transform.scale(npc_image, (250, 75))

    # Коллизии
    collision_tiles = []
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "walls":
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    tile_rect = pygame.Rect(
                        x * TILE_SIZE,
                        y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    collision_tiles.append(tile_rect)

    def check_collision(new_x, new_y):
        player_rect = pygame.Rect(new_x, new_y, player_size, player_size)
        for wall_rect in collision_tiles:
            if player_rect.colliderect(wall_rect):
                return True
        return False

    running = True
    while running:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx -= player_speed
            current_player_image = pygame.transform.scale(player_images["left"], (player_size, player_size))
        if keys[pygame.K_RIGHT]:
            dx += player_speed
            current_player_image = pygame.transform.scale(player_images["right"], (player_size, player_size))
        if keys[pygame.K_UP]:
            dy -= player_speed
            current_player_image = pygame.transform.scale(player_images["up"], (player_size, player_size))
        if keys[pygame.K_DOWN]:
            dy += player_speed
            current_player_image = pygame.transform.scale(player_images["down"], (player_size, player_size))

        if not check_collision(player_x + dx, player_y + dy):
            player_x += dx
            player_y += dy

        # Проверка встречи с NPC
        if abs(player_x - npc_x) < 50 and abs(player_y - npc_y) < 50 and not show_dialog:
            show_dialog = True
            run_dialog()
            player_x -= 1
            player_y -= 1
            show_dialog = False  # Возвращаем контроль игроку после диалога

        # Камера
        camera_x = max(0, min(player_x - WIDTH // 2, tmx_data.width * TILE_SIZE - WIDTH))
        camera_y = max(0, min(player_y - HEIGHT // 2, tmx_data.height * TILE_SIZE - HEIGHT))

        # Отрисовка карты
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        scaled_tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
                        screen.blit(scaled_tile, (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))

        # Отрисовка NPC
        screen.blit(npc_image, (npc_x - camera_x, npc_y - camera_y))

        # Отрисовка игрока
        screen.blit(current_player_image, (player_x - camera_x, player_y - camera_y))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

game_loop(100, 100)
