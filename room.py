from sprites import *
import pygame
import sys
import pygame
import pytmx
from final_window import show_credits
# from test_verse_lesha import first_minigame
import random

pygame.init()
# Константы

SCALE = 2  # Коэффициент зума (изменяй для нужного масштаба)

# font = pygame.font.Font(None, 36)

# Параметры диалога
npc_question = "Чиваува пацанчик, как бы назвал свою команду?"
correct_answer = "zxc1337"
npc_response_correct = "Я как Снайпер: сразу приметил тебя издалека. ХАРОШ(ИЛЮХА)"
npc_response_incorrect = "mda ... :/"
pygame.mixer.music.stop()
pygame.mixer.music.unload()
end_img = pygame.image.load('sprites/end.png').convert_alpha()
end_img = pygame.transform.scale(end_img, (200, 150))
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
        npc_surface = pygame.font.Font(None, 36).render(npc_question, True, (255, 255, 255))
        screen.blit(npc_surface, (100, 100))

        # Отображение ответа NPC (если есть)
        if npc_response:
            response_surface = pygame.font.Font(None, 36).render(npc_response, True, (255, 255, 255))
            screen.blit(response_surface, (100, 200))

        # Отображение введенного текста игрока
        player_surface = pygame.font.Font(None, 64).render(input_text, True, (255, 255, 255)) 
        screen.blit(player_surface, (100, 400))

        # Отрисовка текстового поля
        pygame.draw.rect(screen, input_color, input_box, 2)
        txt_surface = pygame.font.Font().render(input_text, True, input_color) 
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip().lower() == correct_answer.lower():
                        npc_response = npc_response_correct
                    else:
                        npc_response = npc_response_incorrect
                        pygame.mixer.music.load('songs/dota.mp3')
                        pygame.mixer.music.set_volume(0.15)
                        pygame.mixer.music.play()
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Закрытие диалогового окна по Escape
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()


def first_minigame():
    surface = pygame.display.set_mode((1024, 1024))
    background_image = pygame.image.load("sprites/jungle.png").convert()
    background_image = pygame.transform.scale(background_image, (1024,1024))
    hp = pygame.image.load("sprites/hp.png").convert_alpha()
    hpt = pygame.transform.rotozoom(hp, 0, 0.05)
    hpcrush = pygame.image.load("sprites/hpc.png").convert_alpha()
    hptcrush = pygame.transform.rotozoom(hpcrush, 0, 0.3)
    hero = pygame.image.load("sprites/geni_right.png").convert_alpha()
    enemy = pygame.image.load("sprites/enemy.png").convert_alpha()
    enemy = pygame.transform.scale(enemy, (128,128))
    bullet_img = pygame.image.load('sprites/arrow.png')
    bulletp = pygame.transform.rotozoom(bullet_img, -90, 0.1)
    enemy_b = pygame.transform.rotozoom(bullet_img, 90, 0.1)
    running = True
    hero_x, hero_y = 100, HEIGHT // 2
    enemy_x, enemy_y = 800, HEIGHT // 2
    bullets = []
    bullets_enemy = []
    my_hp = 2
    enemy_hp = 10
    player_speed = 10
    # Таймер для стрельбы врага
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    

    while running:
        tick = clock.tick(FPS) / 1000  # Время в секундах

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    bullets.append([hero_x + 50, hero_y])  # Пуля игрока
            if event.type == timer_event:
                enemy_y = random.randint(50, 850)
                bullets_enemy.append([enemy_x, enemy_y])  # Пуля врага

        # Движение игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            hero_y -= player_speed
        if keys[pygame.K_DOWN]:
            hero_y += player_speed

        # Обновление позиций пуль
        for bullet in bullets[:]:  
            bullet[0] += 500 * tick  # Двигаем пулю вправо
            if bullet[0] > WIDTH:
                bullets.remove(bullet)
            elif enemy_x < bullet[0] < enemy_x + 50 and enemy_y < bullet[1] < enemy_y + 128:
                enemy_hp -= 1
                bullets.remove(bullet)

        for bullet in bullets_enemy[:]:  
            bullet[0] -= 500 * tick  # Двигаем пулю влево
            if bullet[0] < 0:
                bullets_enemy.remove(bullet)
            elif hero_x < bullet[0] < hero_x + 50 and hero_y < bullet[1] < hero_y + 128:
                my_hp -= 1
                bullets_enemy.remove(bullet)

        # Отрисовка
        surface.fill((0, 0, 0))
        surface.blit(background_image, (0, 0))
        surface.blit(hero, (hero_x, hero_y))
        surface.blit(enemy, (enemy_x, enemy_y))

        for bullet in bullets:
            surface.blit(bulletp, (bullet[0], bullet[1]))

        for bullet in bullets_enemy:
            surface.blit(enemy_b, (bullet[0], bullet[1]))

        # Отображение HP
        if my_hp > 0:
            surface.blit(hpt, (hero_x, 150))
            hp_text = pygame.font.Font(None, 36).render(str(my_hp), True, (255, 255, 255))
            surface.blit(hp_text, (hero_x - 30, 150))
        else:
            surface.blit(hptcrush, (hero_x, 150))
            pygame.display.flip()
            pygame.time.delay(1000)
            you_lose()
            return

        if enemy_hp > 0:
            surface.blit(hpt, (enemy_x, 150))
            hp_text = pygame.font.Font(None, 36).render(str(enemy_hp), True, (255, 255, 255))
            surface.blit(hp_text, (enemy_x - 30, 150))
        else:
            surface.blit(hptcrush, (enemy_x, 100))
            pygame.display.flip()
            pygame.time.delay(1000)
            you_win()
            return

        pygame.display.flip()

def you_win():
    shape_surf = pygame.Surface(pygame.Rect((0, 0, WIDTH, HEIGHT)).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, (0, 0, 0, 240), shape_surf.get_rect())
    title_font = pygame.font.Font(None, 62)
    title_font1 = pygame.font.Font(None, 48)
    title_text = title_font.render('YOU WIN', True, (255, 255, 255))
    title_ok = title_font1.render('OK', True, (255, 255, 255))
    screen.blit(shape_surf, (0, 0, WIDTH, HEIGHT))
    screen.blit(title_text, (1024 // 2 - 100, 1024 // 4))
    screen.blit(title_ok, (1024 // 2 - 25, 1024 // 2))
    running = 1
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN: 
                    game_loop(350, 2250)
                    running = 0

        pygame.display.flip()
    pygame.quit()
    sys.exit()


def you_lose():
    shape_surf = pygame.Surface(pygame.Rect((0, 0, WIDTH, HEIGHT)).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, (0, 0, 0, 240), shape_surf.get_rect())
    title_font = pygame.font.Font(None, 62)
    title_font1 = pygame.font.Font(None, 48)
    title_text = title_font.render('YOU LOSE', True, (255, 255, 255))
    title_ok = title_font1.render('RETURN', True, (255, 255, 255))
    screen.blit(shape_surf, (0, 0, WIDTH, HEIGHT))
    screen.blit(title_text, (1024 // 2 - 100, 1024 // 4))
    screen.blit(title_ok, (1024 // 2 - 55, 1024 // 2))
    running = 1
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN: 
                    first_minigame()
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
    pygame.quit()
    sys.exit()

def game_loop(x, y):
    pygame.mixer.music.unload()
    # Загрузка карты
    tmx_data = pytmx.load_pygame("pygame_map/map.tmx")
    TILE_SIZE = tmx_data.tilewidth * SCALE  # Увеличиваем тайлы

    global show_dialog

    #portals
    ANIMATION_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(ANIMATION_EVENT, 100)
    toilet = pygame.image.load("sprites/door.jpg").convert_alpha()
    toilet = pygame.transform.scale(toilet, (75,75))
    portal1 = pygame.image.load("sprites/portal1.png").convert_alpha()
    portal1 = pygame.transform.scale(portal1, (40, 65))
    portal2 = pygame.image.load("sprites/portal2.png").convert_alpha()
    portal2 = pygame.transform.scale(portal2, (40, 65))
    portal3 = pygame.image.load("sprites/portal3.png").convert_alpha()
    portal3 = pygame.transform.scale(portal3, (40, 65))
    portal4 = pygame.image.load("sprites/portal4.png").convert_alpha()
    portal4 = pygame.transform.scale(portal4, (40, 65))
    portal5 = pygame.image.load("sprites/portal5.png").convert_alpha()
    portal5 = pygame.transform.scale(portal5, (40, 65))
    portal_frames = [portal1, portal2, portal3, portal4, portal5]
    for i in range(len(portal_frames)):
        portal_frames[i].set_colorkey((255, 255, 255))

    #ghoul
    npc1 = pygame.image.load("sprites/ghoul.png").convert_alpha()
    npc1 = pygame.transform.scale(npc1, (250, 75))

    portal_index = 0  # Индекс текущего кадра
    portal_x, portal_y = 427, 2335  # Координаты портала

    # Игрок
    player_size = TILE_SIZE
    player_x, player_y = x, y  # Стартовая позиция игрока
    player_speed = 4 * SCALE  # Скорость игрока тоже увеличиваем
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

    # print(f"Загружено стен: {len(collision_tiles)}")
    # print(f"Стартовая позиция: {player_x}, {player_y}")

    # Функция проверки столкновений
    def check_collision(new_x, new_y):
        player_rect = pygame.Rect(new_x, new_y, player_size, player_size)
        for wall_rect in collision_tiles:
            if player_rect.colliderect(wall_rect):
                return True
        return False

    

    # Основной цикл
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((30, 30, 30))
        # print(player_x, player_y)
        if (player_x > 426 and player_y > 2332) and (player_x < 480 and player_y < 2390):
            first_minigame()
        if player_x == 2722 and player_y == 900:
            pass
        if player_x > 3586 and player_y > 2132:
            show_credits()
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ANIMATION_EVENT:
                portal_index = (portal_index + 1) % len(portal_frames)

        # Движение
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

        # Проверка коллизий
        if not check_collision(player_x + dx, player_y + dy):
            player_x += dx
            player_y += dy

        if abs(player_x - npc_x) < 50 and abs(player_y - npc_y) < 50 and not show_dialog:
            show_dialog = True
            run_dialog()
            player_x -= 2
            player_y -= 2
            show_dialog = False  # Возвращаем контроль игроку после диалога

        # Камера: центрируем игрока
        camera_x = max(0, min(player_x - WIDTH // 2, tmx_data.width * TILE_SIZE - WIDTH))
        camera_y = max(0, min(player_y - HEIGHT // 2, tmx_data.height * TILE_SIZE - HEIGHT))

        # Отрисовка карты с зумом
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        scaled_tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
                        screen.blit(scaled_tile, (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))

        # screen.blit(npc_image, (npc_x - camera_x, npc_y - camera_y))

        # Отрисовка игрока
        print(player_x, player_y)
        screen.blit(toilet, (3705 - camera_x, 2135 - camera_y))
        screen.blit(end_img, (2498 - camera_x, 2244 - camera_y))
        screen.blit(npc1, (2590 - camera_x, 850 - camera_y))
        screen.blit(current_player_image, (player_x - camera_x, player_y - camera_y))
        screen.blit(portal_frames[portal_index], (portal_x - camera_x, portal_y - camera_y))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
