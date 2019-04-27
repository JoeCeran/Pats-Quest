#importings
import pygame
import time
import scipy
from random import randrange
from skimage.transform import resize


screen = pygame.display.set_mode((900,700))
pygame.mixer.pre_init(44100, -16, 2, 2048) 
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('assets/music/title.mp3')
pygame.mixer.music.play(0)

title = pygame.image.load("assets/img/title.png").convert()
title = pygame.transform.scale(title, (900,700))

finished = False
pressedKeys = pygame.key.get_pressed()

def fade(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(5)

while finished == False: #While game is not finished
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    
    screen.blit(title, (0,0))
    pygame.display.flip()

    pressedKeys = pygame.key.get_pressed()
    
    if pressedKeys[pygame.K_SPACE]:
        effect = pygame.mixer.Sound('assets/sounds/Select.wav')
        effect.play()
        pygame.mixer.music.fadeout(500)
        fade(900,700)
        import patquestsecond
        

    