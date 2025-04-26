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
snake_speed = 15
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# fruit settings
fruit_list = []
FRUIT_LIFETIME = 5000
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

def spawn_fruit():
    pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10,
           random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
    value = random.choice([1, 2, 3])  # points for the fruit
    lifetime = pygame.time.get_ticks() + FRUIT_LIFETIME  # expiration time
    fruit_list.append({'pos': pos, 'value': value, 'expire_time': lifetime})


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
    
    # check if snake eats any fruit
    ate = False
    for fruit in fruit_list:
        if snake_pos == fruit['pos']:
            score += fruit['value']
            fruit_list.remove(fruit)
            ate = True
            break
    if not ate:
        snake_body.pop()

    # remove expired fruits
    current_time = pygame.time.get_ticks()
    fruit_list = [fruit for fruit in fruit_list if fruit['expire_time'] > current_time]

    
    # level up and increase speed
    if score >= 5 * level:
        level += 1
        snake_speed += 2

    if score < 5:
        level_up = False
    
    
    if len(fruit_list) == 0:  # if no fruits left, spawn new ones
        spawn_fruit()


    
    # screen settings
    screen.fill(pygame.Color('white'))

    for x in range(tiles):
        for y in range(tiles):
            pygame.draw.rect(screen, 'lightgray', (x * tile_size, y * tile_size, tile_size, tile_size), 1)
    
    # draw snake and fruit
    for pos in snake_body:
        pygame.draw.rect(screen, pygame.Color('green'), pygame.Rect(pos[0], pos[1], 10, 10))

    for fruit in fruit_list:
        color = 'red' if fruit['value'] == 1 else 'orange' if fruit['value'] == 2 else 'gold'
        pygame.draw.rect(screen, pygame.Color(color), pygame.Rect(fruit['pos'][0], fruit['pos'][1], 10, 10))

    
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