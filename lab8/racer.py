import pygame
import random
import sys
import time
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# colors RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen_height = 600
screen_width = 400
speed = 5
score = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab8\images\AnimatedStreet.png')


screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((255, 255, 255))
pygame.display.set_caption("Car Racing Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab8\images\Enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), 0)

    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if (self.rect.bottom > 600):
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, screen_width - 40), 0)
    
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab8\images\Player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
        
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right <  screen_width:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
    
    #def draw(self, surface):
        #surface.blit(self.image, self.rect)
        
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

INC_speed = pygame.USEREVENT + 1
pygame.time.set_timer(INC_speed, 1000)



while True:
    for event in pygame.event.get():
        if event.type == INC_speed:
            speed += 0.5
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    screen.blit(background, (0, 0))
    scores = font_small.render(str(score), True, BLACK)
    screen.blit(scores, (10, 10))
    
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()
        
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab8\sounds\crash.wav').play()
        time.sleep(0.5)
        
        screen.fill(RED)
        screen.blit(game_over, (30, 250))
        
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()
        
    pygame.display.update()
    FramePerSec.tick(FPS)
    
    