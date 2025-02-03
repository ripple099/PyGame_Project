# --- Управление персонажем ---
import pygame
import sys
FPS = 60
clock = pygame.time.Clock()
width, heigth = 800, 800
screen = pygame.display.set_mode((width, heigth))
image_puth = 'geni.png'
player_images = pygame.image.load(image_puth)
def handle_keys(player_rect):
    global current_player_image
    keys = pygame.key.get_pressed()
    speed = 4

    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
        current_player_image = player_images["left"]
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
        current_player_image = player_images["right"]
    if keys[pygame.K_UP]:
        player_rect.y -= speed
        current_player_image = player_images["up"]
    if keys[pygame.K_DOWN]:
        player_rect.y += speed
        current_player_image = player_images["down"]


background_image = pygame.image.load("sprites/backgrnd_5.png").convert_alpha()

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
        
        # Отрисовка уровня
        for y, row in enumerate(level):
            for x, col in enumerate(row):
                if col == '#':
                    pygame.draw.rect(screen, (255, 255, 255), (x * 32, y * 32, 32, 32))
                elif col == 'E':
                    pygame.draw.rect(screen, (255, 0, 0), (x * 32, y * 32, 32, 32))

        # Отрисовка игрока
        screen.blit(current_player_image, player_rect)

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()



# import pygame
# pygame.init()
# width, height = 800, 800
# image_path = 'geni.png'
# main_hero = pygame.image.load(image_path)
# main_hero = pygame.transform.scale(main_hero, (200, 200))
# screen = pygame.display.set_mode((width, height))
# running = True
# clock = pygame.time.Clock()
# tick = clock.tick(60)
# x, y = 0, 0


# while running:
#     events = pygame.event.get()
#     for event in events:
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             speed = 10
#             if event.key == pygame.K_w:
#                 y += speed
#             if event.key == pygame.K_a:
#                 x -= speed
#             if event.key == pygame.K_s:
#                 y += speed
#             if event.key == pygame.K_d:
#                 x += speed
#         screen.fill((0, 0, 0))
#         screen.blit(main_hero, (x, y))
#     pygame.display.flip()

