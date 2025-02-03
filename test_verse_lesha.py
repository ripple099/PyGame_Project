import os.path
import random
import pygame

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Mountain(pygame.sprite.Sprite):
    image = load_image("mountains.png", -1)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


class Landing(pygame.sprite.Sprite):
    image = load_image("pt.png", -1)

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(0, 4)

        
size = width, height = 400, 300
screen = pygame.display.set_mode(size)
mountain = Mountain()
pygame.display.set_caption("balls")

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()

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
