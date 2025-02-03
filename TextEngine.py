import pygame
import os
import time

# Инициализация Pygame
pygame.init()

# Размер окна
width, height = 640, 480

# Создание окна
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("TextEngine")

# Загрузка спрайтов букв
letters = {}
alphabet = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789"
for letter in alphabet:
    sprite = pygame.image.load(f"assets/sprites/letters/{letter}.png")
    letters[letter] = sprite
    # Загрузка спрайта с заглавной буквой, если он существует
    if os.path.exists(f"assets/sprites/letters/{letter}_uppercase.png"):
        sprite_upper = pygame.image.load(f"assets/sprites/letters/{letter}_uppercase.png")
        letters[letter.upper()] = sprite_upper

# Дополнительные символы, которые не могут быть в Windows и их спрайты
invalid_symbols = {
    ".": pygame.image.load("assets/sprites/letters/symbols/dot.png"),
    ",": pygame.image.load("assets/sprites/letters/symbols/comma.png"),
    "*": pygame.image.load("assets/sprites/letters/symbols/star.png"),
    "!": pygame.image.load("assets/sprites/letters/symbols/exclamation.png")
}

# Текст для отображения с дополнительными символами и символами новой строки
text = "* Hello, world!\n* This is just a test, lmao."
letter_width = letters["a"].get_width()
letter_height = letters["a"].get_height()

# Функция для выравнивания текста по горизонтали
def align_text(text, alignment):
    text_lines = text.split("\n")
    max_line_length = max(len(line) for line in text_lines)
    aligned_text = []
    for line in text_lines:
        if alignment == 'left':
            offset = 0
        elif alignment == 'right':
            offset = max_line_length - len(line)
        aligned_line = ' ' * offset + line
        aligned_text.append(aligned_line)
    return '\n'.join(aligned_text)

text = align_text(text, 'left')

# Координаты для начала отрисовки текста
y = height // 2 - (len(text.split("\n")) * letter_height) // 2
x = width // 2 - (max(len(line) for line in text.split("\n")) * letter_width) // 2

# Переменные для контроля скорости печати и индекса текущей буквы
print_speed = 0.05  # Задержка между буквами в секундах
current_index = 0  # Текущий индекс для отображения буквы
last_update_time = time.time()

# Опциональная анимация печати текста
print_animation = True

# Основной цикл программы
running = True
text_displayed = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0, 0, 0))  # Очистка экрана

    if not text_displayed:
        # Отрисовка текста по буквам
        if print_animation:
            lines = text.split("\n")
            char_count = 0
            for line_num, line in enumerate(lines):
                for i, char in enumerate(line):
                    if char_count < current_index:
                        if char in letters:
                            char_sprite = letters[char]
                        elif char in invalid_symbols:
                            char_sprite = invalid_symbols[char]
                        else:
                            continue
                        window.blit(char_sprite, (x + i * letter_width, y + line_num * letter_height))
                        char_count += 1
                    else:
                        break
                if char_count >= current_index:
                    break
        else:
            # Показываем весь текст сразу, если анимация отключена
            lines = text.split("\n")
            for line_num, line in enumerate(lines):
                for i, char in enumerate(line):
                    if char in letters:
                        char_sprite = letters[char]
                    elif char in invalid_symbols:
                        char_sprite = invalid_symbols[char]
                    else:
                        continue
                    window.blit(char_sprite, (x + i * letter_width, y + line_num * letter_height))

        if print_animation:
            if time.time() - last_update_time > print_speed:
                current_index += 1  # Увеличиваем индекс для отображения следующей буквы
                last_update_time = time.time()

            if current_index > len(text.replace("\n", "")):
                text_displayed = True  # Останавливаем печать после полного отображения текста
    else:
        # Показываем весь текст сразу, если он уже был отображен
        lines = text.split("\n")
        for line_num, line in enumerate(lines):
            for i, char in enumerate(line):
                if char in letters:
                    char_sprite = letters[char]
                elif char in invalid_symbols:
                    char_sprite = invalid_symbols[char]
                else:
                    continue
                window.blit(char_sprite, (x + i * letter_width, y + line_num * letter_height))

    pygame.display.flip()

pygame.quit()