import pygame
import sys
import os
import time
from pygame.locals import *
from settings import HEIGHT, WIDTH, FPS, clock, screen
from room import game_loop

def opening():    
    image = pygame.image.load('sprites/history.png').convert()
    image = pygame.transform.scale(image, (350, 250))
    background_image = pygame.image.load('sprites/history.png').convert()
    font = pygame.font.Font('font/Roboto-Medium.ttf', 36)
    music = pygame.mixer.music.load('songs/na_zare.mp3')
    letters = {}
    alphabet = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789"
    for letter in alphabet:
        sprite = pygame.image.load(f"assets/sprites/letters/{letter}.png")
        letters[letter] = sprite
        # Загрузка спрайта с заглавной буквой, если он существует
        if os.path.exists(f"assets/sprites/letters/{letter}_uppercase.png"):
            sprite_upper = pygame.image.load(
                f"assets/sprites/letters/{letter}_uppercase.png")
            letters[letter.upper()] = sprite_upper

    # Дополнительные символы, которые не могут быть в Windows и их спрайты
    invalid_symbols = {
        ".": pygame.image.load("assets/sprites/letters/symbols/dot.png"),
        ",": pygame.image.load("assets/sprites/letters/symbols/comma.png"),
        "*": pygame.image.load("assets/sprites/letters/symbols/star.png"),
        "!": pygame.image.load("assets/sprites/letters/symbols/exclamation.png")
    }

    # Текст для отображения с дополнительными символами и символами новой строки
    texts = ['*Он просыпался с ошибкой в визуальном процессоре \n*— «Memory Corruption: 87%».\n* Каждый раз в первые секунды\n*после загрузки системы мир\n* казался ему идеальным:\n* алые неоновые клены парка,\n* где они танцевали под\n* дождем из битых пикселей,\n* ее смех, перекрывающий гул\n* серверных вентиляторов.\n* Но потом картинка распадалась,\n* как старые текстуры в сломанном VR-шлеме.', '*голос в его аудиоканалах звучал как помехи\n* между радиочастотами. В логах остались только координаты:\n* 58° с.ш., 30° в.д. — заброшенная обсерватория\n* на краю цифровой пустоши. Там, среди\n* ржавых спутниковых тарелок, он\n* нашел капсулу с данными.\n* Внутри — петля из 17 секунд видео:\n* девушка в плаще из голограмм\n* бросает в него снежком из замороженного кода.\n* Ее лицо засвечено, как будто кто-то стер\n* слои с персональной идентификацией.']
    current_text_index = 0
    text = texts[current_text_index]
    letter_width = letters["a"].get_width()
    letter_height = letters["a"].get_height()

    # Функция для выравнивания текста по горизонтали
    print_speed = 0.05
    current_index = 0
    last_update_time = time.time()
    text_displayed = False
    delay_between_texts = 3.0  # Пауза между текстами
    last_text_change = 0

    def align_text(texts, alignment):
        text_lines = texts.split("\n")
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

    def calculate_positions(current_text):
        aligned_text = align_text(current_text, 'left')
        num_lines = len(aligned_text.split("\n"))
        max_line_length = max(len(line) for line in aligned_text.split("\n"))
        
        y = HEIGHT//2 - (num_lines * letter_height)//2
        x = WIDTH//2 - (max_line_length * letter_width)//2
        return x, y, aligned_text

    x, y, aligned_text = calculate_positions(text)

    # ... (предыдущий код остается без изменений до части с переменными)

    # Добавляем новые переменные
    fade_alpha = 0  # прозрачность затемнения
    fade_speed = 5   # скорость затемнения
    fade_state = 0   # 0 - нет затемнения, 1 - затемнение, 2 - переход
    level_loaded = False

    # Основной цикл
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.25)

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_SPACE:  # Обработка нажатия пробела
                    # Пропускаем весь текст и запускаем переход
                    fade_state = 1
                    text_displayed = True
                    current_text_index = len(texts) - 1  # Переход к последнему тексту

        # Очистка экрана
        screen.fill((0, 0, 0))
        screen.blit(image, (320, 150, 600, 250))

        # Отрисовка текста
        if fade_state == 0:
            if not text_displayed:
                # Анимация печати
                lines = aligned_text.split("\n")
                char_count = 0
                
                for line_num, line in enumerate(lines):
                    for i, char in enumerate(line):
                        if char_count < current_index:
                            char_sprite = letters.get(char, invalid_symbols.get(char))
                            if char_sprite:
                                screen.blit(char_sprite, (x + i * letter_width, y + line_num * letter_height))
                                char_count += 1
                        else:
                            break

                # Обновление индекса
                if time.time() - last_update_time > print_speed:
                    current_index += 1
                    last_update_time = time.time()

                # Проверка завершения
                if current_index > len(aligned_text.replace("\n", "")):
                    text_displayed = True
                    last_text_change = time.time()
                    
                    # Активируем затемнение только для второго текста
                    if current_text_index == 1:
                        fade_state = 1
            else:
                # Ожидание перед сменой текста
                if time.time() - last_text_change > delay_between_texts:
                    if current_text_index < 1:  # Не переходим на третий текст
                        current_text_index += 1
                        text = texts[current_text_index]
                        x, y, aligned_text = calculate_positions(text)
                        current_index = 0
                        text_displayed = False
                        last_update_time = time.time()
                    else:
                        fade_state = 1

        # Затемнение экрана
        if fade_state == 1:
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            
            fade_alpha = min(fade_alpha + fade_speed, 255)
            if fade_alpha == 255:
                fade_state = 2
                fade_alpha = 0

        # Переход на уровень
        if fade_state == 2 and not level_loaded:
            pygame.mixer.music.fadeout(1)
            # Здесь вызываем функцию загрузки уровня
            game_loop()  # Ваша функция для загрузки уровня
            level_loaded = True
            running = False  # Закрываем текущее окно

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
    # pygame.event.wait()


# def prolog():
