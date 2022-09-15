import sys, os
from tkinter import N
from turtle import Screen, width
sys.path.insert(0, os.path.dirname(os.getcwd()))
from board import *
brd=Board()

def indToIJ(n):
    i=n // 5 
    j=n%5
    return i,j

def ijToInd(i,j):
    return int(j*5 + i)

def xyToInd(x,y):
    i=x-MARGIN["left"]
    i=int((i/(boardWidth) ) * 5)

    j= y-MARGIN["top"]
    j=int((j/boardHeight)*5)

    return ijToInd(i,j)

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
boardWidth=SCREEN_WIDTH-MARGIN["left"]-MARGIN["right"]
boardHeight=SCREEN_HEIGHT-MARGIN["top"]-MARGIN["bottom"]

def drawBoard():
    picture = pygame.image.load('img/board.svg')
    
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
    i,j=indToIJ(sq)
    i=4-i
    j=4-j
    bagh=Bagh()
    x=MARGIN["left"]+i*boardWidth/4 - baghWidth/2
    y=MARGIN["top"]+j*boardHeight/4 - baghHeight/2
    bagh.update(x,y)

def drawGoat(sq):
    i,j=indToIJ(sq)
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
        b.make_move(choosen_move)

        if b.game_end==True:
            return np.array(b.victor),np.array(b.history['positions'])

simulate_game(52)

dragDict={
    "drag":False,
    "piece":BAGH_NUMBER,
    "index":0,
}

def dragPiece():
    if dragDict["drag"]:
        mx,my=pygame.mouse.get_pos()
        if dragDict["piece"]==GOAT_NUMBER:
            piece=Goat()
        else:
            piece=Bagh()
        piece.update(mx,my)

#def moveCoder():
    
def dropPiece():
    move_code=''
    if dragDict["piece"]==GOAT_NUMBER:
        move_code=GOAT_LETTER
    else:
        move_code=BAGH_LETTER
    fromSq=str(dragDict["index"])
    mx,my=pygame.mouse.get_pos()
    toSq=xyToInd(mx,my)
    if toSq<0 or toSq>24: #check what happens if outside board, we should prob break if toSq< 0 or > 24
        return
    toSq=f"{toSq:02d}"  
    
    if len(toSq)==1:
        toSq='0'+toSq
    move_code=move_code+toSq+fromSq
    if b.turn == BAGH_NUMBER:
        difference=abs(int(fromSq)-int(toSq))
        if difference == 1 and difference !=5 and difference!= 6:
            for d1 in JUMP_CONNECTIONS[int(fromSq)]:
                for d2 in JUMP_CONNECTIONS[int(toSq)]:
                    if d1["jump_over"]==d2["jump_over"]:
                        #then there is a jump move
                        jump= f'{d1["jump_over"]:02d}'
                        move_code+=jump

                    


    if move_code in b.legal_moves:
        b.make_move(move_code)


def main():

    

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((255,255,255))
        drawBoard()
        for sq in b.bagh_occupancy:
            drawBagh(sq)
        for sq in b.goat_occupancy:
            drawGoat(sq)
        dragPiece()


        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx,my=pygame.mouse.get_pos()
                    index=xyToInd(mx,my)
                    if index in b.bagh_occupancy and b.turn==BAGH_NUMBER:
                        dragDict["piece"]=BAGH_NUMBER
                    if index in b.goat_occupancy and b.turn==GOAT_NUMBER: #phase == movement
                        dragDict["piece"]=GOAT_NUMBER
                    dragDict["drag"]=True
                    dragDict["index"]=index
            # elif event.type == pygame.MOUSEMOTION:
            #     if dragDict["drag"]:
            #         dragPiece()
            elif event.type == pygame.MOUSEBUTTONUP:
                dragDict["drag"]=False
                dragDict["index"]=100
                dropPiece()

        pygame.display.flip() 
        clock.tick(5)

if __name__ == '__main__':
    main()