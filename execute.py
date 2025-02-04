import pygame
from story import opening
from start_window import start_screen

# --- Инициализация Pygame ---
pygame.init()
pygame.display.set_caption("Lost in Memory")
icon = pygame.image.load('sprites/icon.jpeg')
pygame.display.set_icon(icon)


if __name__ == "__main__":
    while True:
        state = start_screen()
        if state == "game":
            opening()
        