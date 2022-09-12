import sys, os
sys.path.insert(0, os.path.dirname(os.getcwd()))
from board import Board
brd=Board()

import pygame
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 0.7 * SCREEN_WIDTH
MARGIN={
    "left": SCREEN_WIDTH*0.35,
    "right":SCREEN_WIDTH*0.1,
    "top":SCREEN_HEIGHT*0.1,
    "bottom": SCREEN_HEIGHT*0.1
}

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
class Bagh(pygame.sprite.Sprite):
    def __init__(self):
        super(Bagh, self).__init__()
        self.surf = pygame.image.load("img/bagh.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

class Goat(pygame.sprite.Sprite):
    def __init__(self):
        super(Goat, self).__init__()
        self.surf = pygame.image.load("img/goat.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

baghs = pygame.sprite.Group()
goats = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()




def main():
    
    picture = pygame.image.load('img/board.svg')
    picture = pygame.transform.scale(picture, (SCREEN_WIDTH-MARGIN["left"]-MARGIN["right"], 
        SCREEN_HEIGHT-MARGIN["top"]-MARGIN["bottom"]))
    rect = picture.get_rect()
    rect = rect.move((MARGIN["left"], MARGIN["top"]))

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(picture, rect)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        pygame.display.flip() 
        clock.tick(30)

if __name__ == '__main__':
    main()