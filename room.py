from sprites import *
import pygame
import sys

def game_loop():
    global current_player_image
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
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

        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))
        screen.blit(current_player_image, player_rect)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()