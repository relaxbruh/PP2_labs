import pygame

pygame.init()

screen_length = 1200
screen_width = 600

screen= pygame.display.set_mode((screen_length, screen_width))
pygame.display.set_caption("Circle task")



character_speed = 20 
character_x = screen_length / 2 - 50
character_y = screen_width / 2 - 50

FPS = pygame.time.Clock()

running = True
while running:
    screen.fill(('white'))
    
    character = pygame.draw.circle(screen, (95, 56, 30), (int(character_x), int(character_y)), 25)
   
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and character_x > 0:
        character_x -= character_speed
    
    if keys[pygame.K_RIGHT] and character_x < screen_length - 100:
        character_x += character_speed
    
    if keys[pygame.K_UP] and character_y > 0:
        character_y -= character_speed
        
    if keys[pygame.K_DOWN] and character_y < screen_width - 100:
        character_y += character_speed
    
    # letters 
    if keys[pygame.K_a] and character_x > 0:
        character_x -= character_speed
        
    if keys[pygame.K_d] and character_x < screen_length - 100:
        character_x += character_speed
    
    if keys[pygame.K_w] and character_y > 0:
        character_y -= character_speed
        
    if keys[pygame.K_s] and character_y < screen_width - 100:
        character_y += character_speed
    
    
    FPS.tick(60)
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
