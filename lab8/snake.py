import pygame
import time
import random
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("snake task")
FPS = pygame.time.Clock()


# snake settings
snake_speed = 13
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# fruit settings
fruit_pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10, random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
fruit_spawn = True

# game settings
tiles = 40
tile_size = SCREEN_WIDTH / tiles
direction = 'RIGHT'
score = 0
level = 1
level_up = False

def show_text(text, color, font, size, x, y):
    text_font = pygame.font.SysFont(font, size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, text_rect)

def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(f'Score: {score}', True, 'red')
    game_over_surface_2 = my_font.render(f'Highest Level: {level}', True, 'red')

    game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    game_over_rect_2 = game_over_surface_2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

    screen.fill('black')
    screen.blit(game_over_surface, game_over_rect)
    screen.blit(game_over_surface_2, game_over_rect_2)
    pygame.display.update()
    pygame.time.delay(2000)

    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # dont let snake go in opposite direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
    
    # move snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10
    
    # grow snake
    snake_body.insert(0, list(snake_pos))
    
    # check if snake eats fruit
    if snake_pos == fruit_pos:
        score += 1
        fruit_spawn = False
    else:
        snake_body.pop()
    
    # level up and increase speed
    if score >= 5 * level:
        level += 1
        snake_speed += 2

    if score < 5:
        level_up = False
    
    
    if not fruit_spawn:
        fruit_pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10, random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
    fruit_spawn = True
    
    # screen settings
    screen.fill(pygame.Color('white'))

    for x in range(tiles):
        for y in range(tiles):
            pygame.draw.rect(screen, 'lightgray', (x * tile_size, y * tile_size, tile_size, tile_size), 1)
    
    # draw snake and fruit
    for pos in snake_body:
        pygame.draw.rect(screen, pygame.Color('green'), pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(screen, pygame.Color('red'), pygame.Rect(fruit_pos[0], fruit_pos[1], 10, 10))
    
    # check game over conditions
    if snake_pos[0] < 0 or snake_pos[0] >= SCREEN_WIDTH or snake_pos[1] < 0 or snake_pos[1] >= SCREEN_HEIGHT:
        game_over() 

    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    show_text(f'Score: {score}', 'black', 'Arial', 20, 10, 10)
    show_text(f'Level: {level}', 'black', 'Arial', 20, SCREEN_WIDTH - 100, 10)

    pygame.display.update()
    FPS.tick(snake_speed)