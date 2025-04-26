import pygame

pygame.init()
pygame.mixer.init()

screen_length = 500
screen_width = 300

screen = pygame.display.set_mode((screen_length, screen_width))
pygame.display.set_caption("music player task")

icon = pygame.image.load(r'C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab7\note.png')
pygame.display.set_icon(icon)

# List of songs
playlist = [
    r"C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab7\Сплин - моё сердце.mp3",
    r"C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab7\Queen - another one bites the dust.mp3",
    r"C:\Users\Admin\Desktop\PP2_FORLABS\labs\lab7\Skillet - monster.mp3"
]

# Track index
current_track = 0

# Load first track
pygame.mixer.music.load(playlist[current_track])

# Play music
def play_music():
    pygame.mixer.music.play()

running = True
while running:

    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                
                # pause and unpouse music
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            
            # start music
            elif event.key == pygame.K_s:
                play_music()

            # next and previous track
            elif event.key == pygame.K_RIGHT:
                current_track = (current_track + 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_track])
                play_music()
            elif event.key == pygame.K_LEFT:
                current_track = (current_track - 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_track])
                play_music()


        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()