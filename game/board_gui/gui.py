import pygame
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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


running = True
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

picture = pygame.image.load('img/board.svg')
picture = pygame.transform.scale(picture, (SCREEN_WIDTH, SCREEN_HEIGHT))
rect = picture.get_rect()
print(rect)

#rect = rect.move((x, y))
#screen.blit(picture, rect)

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    
    screen.blit(picture, rect)

    # Update the display
    pygame.display.flip() 

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

