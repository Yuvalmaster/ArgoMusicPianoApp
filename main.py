import pygame
import piano_lists as pl
from pygame import mixer

# Set system settings
pygame.init()
pygame.mixer.set_num_channels(50)

font            = pygame.font.SysFont(None, 48)
medium_font     = pygame.font.SysFont(None, 28)
small_font      = pygame.font.SysFont(None, 16)
real_small_font = pygame.font.SysFont(None, 10)


# Set keyboard settings
white_sounds  = []
black_sounds  = []
active_whites = []
active_blacks = []

left_oct  = 4
right_oct = 5

piano_notes  = pl.piano_notes
white_notes  = pl.white_notes
black_notes  = pl.black_notes
black_labels = pl.black_labels

# Set App settings
fps    = 60
timer  = pygame.time.Clock()
HEIGHT = 380
WIDTH = 1280
screen = pygame.display.set_mode([WIDTH, HEIGHT])

pygame.display.set_caption("ARGO MUSIC")

# Setup sound files
for i in range(len(white_notes)):
    white_sounds.append(mixer.Sound(f'assets\\notes\\{white_notes[i]}.wav'))

for i in range(len(black_notes)):
    black_sounds.append(mixer.Sound(f'assets\\notes\\{black_notes[i]}.wav'))


def draw_title_bar():
    img = pygame.transform.scale(pygame.image.load('assets/Logo.png'), [150, 70])
    screen.blit(img, (500, 0))
    title_text = font.render('MUSIC', True, 'gray')
    screen.blit(title_text, (500+128, 18))
    title_text = font.render('MUSIC', True, 'orange')
    screen.blit(title_text, (500+130, 20))


def draw_piano(whites, blacks, black_notes, white_notes, black_labels):
    # Set white rectangles
    white_rects = []
    white_width = int(WIDTH / (len(white_notes)))
    
    for i in range(len(white_notes)):
        # Create white keys
        rect = pygame.draw.rect(screen, 'white',
                                [i * white_width, HEIGHT - 300, white_width, 300],
                                0, 2)
        
        white_rects.append(rect)

        # Create black surround for each key
        pygame.draw.rect(screen, 'black',
                         [i * white_width, HEIGHT - 300, white_width, 300],
                         2, 2)

        # Set white keys labels and location
        key_label = small_font.render(white_notes[i], True, 'black')
        screen.blit(key_label, (i * white_width + 3, HEIGHT - 20))


    black_width = int(white_width / 2)
    skip_count = 0
    last_skip = 2
    skip_track = 2
    black_rects = []

    for i in range(len(black_notes)):
        # Set black keys
        rect = pygame.draw.rect(screen, 'black',
                                [32 + (i * white_width) + (skip_count * white_width) - (black_width / 2), HEIGHT - 300, black_width*1.3, 200],
                                0, 2)

        for q in range(len(blacks)):
            if blacks[q][0] == i:
                if blacks[q][1] > 0:
                    pygame.draw.rect(screen, 'green',
                                     [32 + (i * white_width) + (skip_count * white_width) - (black_width / 2), HEIGHT - 300, black_width*1.3, 200],
                                     2, 2)

                    blacks[q][1] -= 1

        key_label = real_small_font.render(black_labels[i], True, 'white')
        screen.blit(key_label, (35 + (i * white_width) + (skip_count * white_width) - (black_width / 2), HEIGHT - 120))
        black_rects.append(rect)

        skip_track += 1

        if last_skip == 2 and skip_track == 3:
            last_skip = 3
            skip_track = 0
            skip_count += 1

        elif last_skip == 3 and skip_track == 2:
            last_skip = 2
            skip_track = 0
            skip_count += 1

    for i in range(len(whites)):
        if whites[i][1] > 0:
            j = whites[i][0]

            pygame.draw.rect(screen, 'green',
                             [j * white_width, HEIGHT - 100, white_width, 100],
                             2, 2)

            whites[i][1] -= 1

    return white_rects, black_rects, whites, blacks



# Run application
run = True
while run:
    timer.tick(fps)
    screen.fill('white')
    
    white_keys, black_keys, active_whites, active_blacks = draw_piano(active_whites, active_blacks, black_notes, white_notes, black_labels)
    draw_title_bar()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            black_key = False
            
            for i in range(len(black_keys)):
                if black_keys[i].collidepoint(event.pos):
                    black_sounds[i].play(0, 1000)
                    black_key = True
                    active_blacks.append([i, 30])
                    
            for i in range(len(white_keys)):
                if white_keys[i].collidepoint(event.pos) and not black_key:
                    white_sounds[i].play(0, 1500)
                    active_whites.append([i, 30])
 
        pygame.display.flip()
pygame.quit()
