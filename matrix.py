font = pygame.font.SysFont('Consolas', 20)
text_color = pygame.Color('green')
text_symbols = ['0', '1']
text_pos = [(random.randint(0, window_size[0]), 0) for i in range(50)]
text_speed = [(0, random.randint(1, 5)) for i in range(50)]
text_surface_list = []


button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(button_pos, button_size),
    text=button_text,
    manager=gui_manager
)

while True:
    time_delta = pygame.time.Clock().tick(60) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            text_surface_list = []
            for i in range(50):
                text_symbol = random.choice(text_symbols)
                text_surface = font.render(text_symbol, True, text_color)
                text_surface_list.append(text_surface)

        gui_manager.process_events(event)

    gui_manager.update(time_delta)

    window.fill(pygame.Color('black'))

    for i in range(50):
        text_pos[i] = (text_pos[i][0], text_pos[i][1] + text_speed[i][1])
        if text_pos[i][1] > window_size[1]:
            text_pos[i] = (random.randint(0, window_size[0]), -20)
        if len(text_surface_list) > i:
            window.blit(text_surface_list[i], text_pos[i])

    gui_manager.draw_ui(window)
    pygame.display.update()