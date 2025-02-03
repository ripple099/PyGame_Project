import pygame
from first_room import game_loop
from start_window import start_screen

# --- Инициализация Pygame ---
pygame.init()
pygame.display.set_caption("Lost in Memory")


if __name__ == "__main__":
    while True:
        state = start_screen()
        if state == "game":
            game_loop()
