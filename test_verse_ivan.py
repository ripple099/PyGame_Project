import pygame
import random
import math

# Настройки
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
PLAYER_SPEED = 5

# Цвета
DARK_GREY = (40, 40, 50)
LIGHT_BLUE = (100, 200, 255)

class Camera:
    def update(self, target):
        # Ограничиваем камеру границами карты
        x = -target.rect.x + SCREEN_WIDTH // 2
        y = -target.rect.y + SCREEN_HEIGHT // 2
        
        # Не даем камере выйти за левую/верхнюю границу
        x = min(0, x)
        y = min(0, y)
        
        # Не даем камере выйти за правую/нижнюю границу
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)
        
        self.camera = pygame.Rect(x, y, self.width, self.height)

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        super().__init__()
        self.tile_type = tile_type
        self.image = self.create_tile()
        self.rect = self.image.get_rect(topleft=(x*TILE_SIZE, y*TILE_SIZE))
        
    def create_tile(self):
        texture = {
            'wall': self.create_wall(),
            'floor': self.create_floor(),
            'door': self.create_door(),
            'water': self.create_water(),
            'decor': self.create_decor()
        }
        return texture[self.tile_type]
    
    def create_wall(self):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        base_color = (random.randint(80,100), random.randint(80,100), random.randint(80,100))
        surf.fill(base_color)
        
        # Текстура камня
        for _ in range(20):
            x = random.randint(2, TILE_SIZE-2)
            y = random.randint(2, TILE_SIZE-2)
            shade = random.randint(-20, 20)
            color = tuple(min(255, max(0, c + shade)) for c in base_color)
            pygame.draw.circle(surf, color, (x,y), random.randint(1,3))
        return surf
    
    def create_floor(self):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        base_color = (random.randint(100,120), random.randint(90,110), random.randint(80,100))
        surf.fill(base_color)
        
        # Трещины и узоры
        if random.random() < 0.3:
            start = (random.randint(5, TILE_SIZE-5), random.randint(5, TILE_SIZE-5))
            end = (start[0]+random.randint(-10,10), start[1]+random.randint(-10,10))
            pygame.draw.line(surf, (base_color[0]-30, base_color[1]-30, base_color[2]-30), 
                           start, end, 2)
        return surf
    
    def create_water(self):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        for i in range(10):
            x = random.randint(0, TILE_SIZE)
            y = random.randint(0, TILE_SIZE)
            alpha = random.randint(100, 200)
            pygame.draw.circle(surf, (70, 120, 200, alpha), (x,y), random.randint(3,6))
        return surf
    
    def create_door(self):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        # Основа двери
        door_color = (90, 60, 40)  # Темно-коричневый
        pygame.draw.rect(surf, door_color, (4, 2, TILE_SIZE-8, TILE_SIZE-4))
        
        # Текстура дерева
        for i in range(6):
            x = 6 + i * 4
            shade = random.randint(-15, 15)
            strip_color = (
                door_color[0] + shade,
                door_color[1] + shade,
                door_color[2] + shade
            )
            pygame.draw.line(surf, strip_color, (x, 4), (x, TILE_SIZE-6), 2)
        
        # Металлическая фурнитура
        pygame.draw.circle(surf, (180, 180, 180), 
                         (TILE_SIZE-10, TILE_SIZE//2), 3)  # Ручка
        pygame.draw.rect(surf, (150, 150, 150), (6, TILE_SIZE//2-8, 6, 16))  # Петли
        
        # Тень для объема
        pygame.draw.line(surf, (40, 40, 40), (4, 2), (4, TILE_SIZE-4), 2)
        return surf

    def create_decor(self):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        decor_type = random.choice(['plant', 'crystal', 'rune'])
        colors = {
            'plant': (30, 120, 50),
            'crystal': (200, 220, 255),
            'rune': (180, 40, 60)
        }
        pygame.draw.circle(surf, colors[decor_type], 
                         (TILE_SIZE//2, TILE_SIZE//2), random.randint(4,8))
        return surf

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE-4, TILE_SIZE-4))
        self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect(center=(x*TILE_SIZE, y*TILE_SIZE))
        
    def update(self, keys):
        dx = dy = 0
        if keys[pygame.K_a]: dx -= PLAYER_SPEED
        if keys[pygame.K_d]: dx += PLAYER_SPEED
        if keys[pygame.K_w]: dy -= PLAYER_SPEED
        if keys[pygame.K_s]: dy += PLAYER_SPEED
        
        self.rect.x += dx
        self.rect.y += dy
        self.check_collisions(dx, dy)

    def check_collisions(self, dx, dy):
        map_width = len(WORLD_MAP[0]) * TILE_SIZE
        map_height = len(WORLD_MAP) * TILE_SIZE
        # Проверяем границы карты
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > map_width:
            self.rect.right = map_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > map_height:
            self.rect.bottom = map_height

        # Проверяем коллизии со стенами
        for y, row in enumerate(WORLD_MAP):
            for x, char in enumerate(row):
                if char == 'W':
                    wall = Wall(x, y)
                    walls.add(wall)
                    all_sprites.add(wall)

# Инициализация
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Создание карты
WORLD_MAP = [
    "WWWWWWWWWWDDDDDWWWWWWWW",
    "W...~~.~~.......~~...W",
    "W.~~~~.~~.d.d.~~.~~.W",
    "W..d..........d.....dW",
    "W....~~.~~.~~.~~....W",
    "WWD.................WW",
    "WW....d.d.d.d.d....WW",
    "WWW.......D.......WWW",
    "WWWWWWWWWWWWWWWWWWWWW"
]

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()

for y, row in enumerate(WORLD_MAP):
    for x, char in enumerate(row):
        if char == 'W':
            tile = Tile(x, y, 'wall')
        elif char in '.d':
            tile = Tile(x, y, 'floor')
            if char == 'd' and random.random() < 0.7:
                decor = Tile(x, y, 'decor')
                all_sprites.add(decor)
        elif char == '~':
            tile = Tile(x, y, 'water')
        elif char == 'D':
            tile = Tile(x, y, 'door')
        
        if char in 'WD~':
            all_sprites.add(tile)
            if char == 'W':
                walls.add(tile)

player = Player(5, 5)
all_sprites.add(player)
camera = Camera(len(WORLD_MAP[0])*TILE_SIZE, len(WORLD_MAP)*TILE_SIZE)

# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    keys = pygame.key.get_pressed()
    player.update(keys)
    camera.update(player)
    
    # Отрисовка
    screen.fill(DARK_GREY)
    
    # Рисуем все спрайты
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))
    
    # Добавляем световой эффект
    light_mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    radius = 150
    pygame.draw.circle(light_mask, (255, 255, 255, 50), 
                      camera.apply(player).center, radius)
    screen.blit(light_mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()