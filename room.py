from sprites import *
import pygame
import sys
import pygame
import pytmx
from test_verse_lesha import first_minigame


def game_loop():
    # Загрузка карты
    tmx_data = pytmx.load_pygame("maps/map.tmx")
    TILE_SIZE = tmx_data.tilewidth

    # Игрок
    player_size = TILE_SIZE
    player_x, player_y = 950, 1140  # Безопасная стартовая позиция
    player_speed = 5

    # Коллизии
    collision_tiles = []

    # Загрузка коллизий из слоя walls
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

    print(f" Загружено стен: {len(collision_tiles)}")
    print(f" Стартовая позиция: {player_x}, {player_y}")

    # Проверка коллизий
    def check_collision(new_rect):
        for wall_rect in collision_tiles:
            if new_rect.colliderect(wall_rect):
                return True
        return False

    # Основной цикл
    clock = pygame.time.Clock()
    global current_player_image
    running = True
    while running:
        if player_x == 174 and player_y == 1200:
            first_minigame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((30, 30, 30))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Движение
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        speed = 4
        if keys[pygame.K_LEFT]:
            player_rect.x -= speed
            dx -= player_speed
            current_player_image = player_images["left"]
        if keys[pygame.K_RIGHT]:
            player_rect.x += speed
            dx += player_speed
            current_player_image = player_images["right"]
        if keys[pygame.K_UP]:
            player_rect.y -= speed
            dy -= player_speed
            current_player_image = player_images["up"]
        if keys[pygame.K_DOWN]:
            player_rect.y += speed
            dy += player_speed
            current_player_image = player_images["down"]

        # Обновляем позицию с проверкой коллизий
        new_rect = pygame.Rect(player_x + dx, player_y + dy, player_size, player_size)
        if not check_collision(new_rect):
            player_x += dx
            player_y += dy

        # Камера
        camera_x = (player_x - WIDTH // 2)
        camera_y = (player_y - HEIGHT // 2)
        camera_x = max(0, min(camera_x, tmx_data.width * TILE_SIZE - WIDTH))
        camera_y = max(0, min(camera_y, tmx_data.height * TILE_SIZE - HEIGHT))
        screen.blit(screen, (-camera_x, -camera_y))

        # Отрисовка карты
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))


        screen.blit(current_player_image, (player_x - camera_x, player_y - camera_y, player_size, player_size))
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()
