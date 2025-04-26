import pygame
import random
import sys
import time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Game settings
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Screen dimensions
screen_height = 600
screen_width = 400

# Initial settings
speed = 5
score = 0
coins_collected = 0

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background image
background = pygame.image.load(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab8\images\AnimatedStreet.png')

# Set up display
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(WHITE)
pygame.display.set_caption("Car Racing Game")

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab8\images\Enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), 0)

    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if self.rect.bottom > screen_height:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, screen_width - 40), 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab8\images\Player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < screen_width:
            self.rect.move_ip(5, 0)

# Coin class (moves toward player)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.respawn()

    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height:
            self.respawn()

    def respawn(self):
        self.rect.center = (random.randint(40, screen_width - 40), 0)

# Create game objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Groups
enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))

    # Show score & coins
    scores = font_small.render(f"Score: {score}", True, BLACK)
    coins_text = font_small.render(f"Coins: {coins_collected}", True, BLACK)
    screen.blit(scores, (10, 10))
    screen.blit(coins_text, (10, 30))

    # Move & draw all sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # Collision with enemy
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

    # Collision with coin
    if pygame.sprite.spritecollideany(P1, coins):
        coins_collected += 1
        speed += 0.5
        C1.respawn()

    pygame.display.update()
    FramePerSec.tick(FPS)
