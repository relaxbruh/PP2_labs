import pygame
import time

pygame.init()

screen_length = 1000
screen_width = 800

screen = pygame.display.set_mode((screen_length, screen_width))
pygame.display.set_caption("clock task")

icon = pygame.image.load(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab7\mickeyclock1.png')
pygame.display.set_icon(icon)

# clock
clock = pygame.image.load(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab7\mickeyclock1.png').convert_alpha()
second_arrow = pygame.image.load(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab7\hand1.png').convert_alpha()
minute_arrow = pygame.image.load(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab7\hand2.png').convert_alpha()

x = (screen_length - clock.get_width()) // 2
y = (screen_width - clock.get_height()) // 2

# find the center of the clock
clock_center = (x + clock.get_width() // 2, y + clock.get_height() // 2)


running = True
while running:

    screen.fill(('white'))

    # placing clock
    screen.blit(clock, (x, y))

    # system time
    current_time = time.localtime()
    seconds = time.localtime().tm_sec
    minutes = time.localtime().tm_min

    # Calculate angles
    angle1 = -seconds * 6
    angle2 = -minutes * 6

    # Rotate the hands
    rotated_second_arrow = pygame.transform.rotate(second_arrow, angle1)
    rotated_minute_arrow = pygame.transform.rotate(minute_arrow, angle2)

    # position the hand in the center of the watch
    second_arrow_rect = rotated_second_arrow.get_rect()
    minute_arrow_rect = rotated_minute_arrow.get_rect()
    second_arrow_rect.center = (clock_center[0], clock_center[1])
    minute_arrow_rect.center = (clock_center[0], clock_center[1])

    # Offset up so that the beginning is in the center
    screen.blit(rotated_second_arrow, second_arrow_rect.topleft)
    screen.blit(rotated_minute_arrow, minute_arrow_rect.topleft)
    pygame.display.flip()
    pygame.time.delay(1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()