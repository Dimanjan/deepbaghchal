import sys, os
from tkinter import N
from turtle import Screen, width
sys.path.insert(0, os.path.dirname(os.getcwd()))
from board import *
brd=Board()

def intToIJ(n):
    i=n // 5 
    j=n%5
    return i,j

import pygame
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 0.7 * SCREEN_WIDTH
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((255,255,255))

MARGIN={
    "left": SCREEN_WIDTH*0.35,
    "right":SCREEN_WIDTH*0.1,
    "top":SCREEN_HEIGHT*0.1,
    "bottom": SCREEN_HEIGHT*0.1
}
picture = pygame.image.load('img/board.svg')
boardWidth=SCREEN_WIDTH-MARGIN["left"]-MARGIN["right"]
boardHeight=SCREEN_HEIGHT-MARGIN["top"]-MARGIN["bottom"]
picture = pygame.transform.scale(picture, (boardWidth, boardHeight))
#rect = picture.get_rect()
#rect = rect.move((MARGIN["left"], MARGIN["top"]))
screen.blit(picture, (MARGIN["left"], MARGIN["top"]))



baghWidth=boardWidth/(N_ROWS+1)
baghHeight=boardHeight/(N_COLUMNS+1)
goatWidth=baghWidth*0.7
goatHeight=baghHeight*0.7

from pygame.locals import *
class Bagh(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bagh.png")
        self.image=pygame.transform.scale(self.image, (baghWidth,baghHeight))

    def update(self,bx,by):
        self.rect=self.image.get_rect(topleft = (bx,by))
        screen.blit(self.image, (bx,by))

class Goat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/goat.png")
        self.image=pygame.transform.scale(self.image, (goatWidth,goatHeight))

    def update(self,bx,by):
        self.rect=self.image.get_rect(topleft = (bx,by))
        screen.blit(self.image, (bx,by))
baghs = pygame.sprite.Group()
goats = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

bagh=Bagh()

def drawBagh(sq):
    i,j=intToIJ(sq)
    i=4-i
    j=4-j
    bagh=Bagh()
    x=MARGIN["left"]+i*boardWidth/4 - baghWidth/2
    y=MARGIN["top"]+j*boardHeight/4 - baghHeight/2
    bagh.update(x,y)

def drawGoat(sq):
    i,j=intToIJ(sq)
    i=4-i
    j=4-j
    goat=Goat()
    x=MARGIN["left"]+i*boardWidth/4 - goatWidth/2
    y=MARGIN["top"]+j*boardHeight/4 - goatHeight/2
    goat.update(x,y)
        
import numpy as np

import random
def random_chooser(lst):
  return random.choice(lst)

b=Board()
def simulate_game(n_moves):
    count=0
    while n_moves>count:
        count+=1
        available_moves=b.legal_moves
        choosen_move=random_chooser(available_moves)
        print(choosen_move)
        b.make_move(choosen_move)

        if b.game_end==True:
            return np.array(b.victor),np.array(b.history['positions'])

simulate_game(20)


def main():

    bagh_dragging=False
    for sq in b.bagh_occupancy:
        drawBagh(sq)
    for sq in b.goat_occupancy:
        drawGoat(sq)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    bx,by=bagh.get_rect().x,bagh.get_rect().y

                    print('x,y',bx,by)   
                    print(event.pos)    
                    if bagh.get_rect().collidepoint(event.pos):
                        print('down')

                        bagh_dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = bagh.x - mouse_x
                        offset_y = bagh.y - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:            
                    bagh_dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if bagh_dragging:
                    mouse_x, mouse_y = event.pos
                    bagh.x = mouse_x + offset_x
                    bagh.y = mouse_y + offset_y

        pygame.display.flip() 
        clock.tick(5)

if __name__ == '__main__':
    main()