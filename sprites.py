import pygame
from settings import *

# --- Загрузка спрайтов ---
player_image_left = pygame.image.load("sprites/geni_left.png").convert_alpha()
player_image_left = pygame.transform.scale(player_image_left, (32, 32))
player_image_right = pygame.image.load("sprites/geni_right.png").convert_alpha()
player_image_right = pygame.transform.scale(player_image_right, (32, 32))
player_image_back = pygame.image.load("sprites/geni_back.png").convert_alpha()
player_image_back = pygame.transform.scale(player_image_back, (32, 32))
player_image_front = pygame.image.load("sprites/geni_front.png").convert_alpha()
player_image_front = pygame.transform.scale(player_image_front, (32, 32))

player_images = {
    "left": player_image_left,
    "right": player_image_right,
    "up": player_image_back,
    "down": player_image_front
}

current_player_image = player_image_front
player_rect = current_player_image.get_rect()
player_rect.topleft = (WIDTH // 2, HEIGHT // 2)

background_image = pygame.image.load("sprites/background_1.png").convert_alpha()