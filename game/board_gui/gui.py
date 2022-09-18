import sys, os
sys.path.insert(0, os.path.dirname(os.getcwd()))
from board import *
brd=Board()

def indToIJ(n):
    j=n // 5
    i=n%5
    return i,j

def ijToInd(i,j):
    if i>4 or j>4:
        return 100
    return int(j*5 + i)

def xyToInd(x,y):
    dx=x-MARGIN["left"]+squareWidth/2
    i=int((dx//(squareWidth) ) )

    dy= y-MARGIN["top"]+squareHeight/2
    j=int((dy//squareHeight))

    if i>4 or j>4:
        return 100
    return ijToInd(i,j)

import pygame
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 0.7 * SCREEN_WIDTH
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((255,255,255))

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 0.7 * SCREEN_WIDTH

REM_GOAT={
    'drag':False
}

MARGIN={
    "left": SCREEN_WIDTH*0.38,
    "right":SCREEN_WIDTH*0.2,
    "top":SCREEN_HEIGHT*0.2,
    "bottom": SCREEN_HEIGHT*0.2
}
boardWidth=SCREEN_WIDTH-MARGIN["left"]-MARGIN["right"]
boardHeight=SCREEN_HEIGHT-MARGIN["top"]-MARGIN["bottom"]

squareWidth=boardWidth/4
squareHeight=boardHeight/4

remainingGoatX=SCREEN_WIDTH*0.12
remainingGoatY=SCREEN_HEIGHT*0.3

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
    # i=4-i
    # j=4-j
    bagh=Bagh()
    x=MARGIN["left"]+i*boardWidth/4 - baghWidth/2
    y=MARGIN["top"]+j*boardHeight/4 - baghHeight/2
    bagh.update(x,y)

def drawGoat(sq):
    i,j=indToIJ(sq)
    # i=4-i
    # j=4-j
    goat=Goat()
    x=MARGIN["left"]+i*boardWidth/4 - goatWidth/2
    y=MARGIN["top"]+j*boardHeight/4 - goatHeight/2
    goat.update(x,y)

dragDict={
    "drag":False,
    "piece":BAGH_NUMBER,
    "index":100,
}

def dragPiece():
    if dragDict["drag"]:
        mx,my=pygame.mouse.get_pos()
        if dragDict["piece"]==GOAT_NUMBER:
            piece=Goat()
            mx,my=mx-goatWidth/2,my-goatHeight/2
        else:
            piece=Bagh()
            mx,my=mx-baghWidth/2,my-baghHeight/2
        piece.update(mx,my)

def dropPiece():
    move_code=''
    if dragDict["piece"]==GOAT_NUMBER:
        move_code=GOAT_LETTER
    else:
        move_code=BAGH_LETTER
    fromSq=f'{dragDict["index"]:02d}'
    mx,my=pygame.mouse.get_pos()
    toSq=xyToInd(mx,my)
    if toSq<0 or toSq>24: #check what happens if outside board, we should prob break if toSq< 0 or > 24
        return
    toSq=f"{toSq:02d}"

    move_code=move_code+toSq+fromSq

    #check if its a jump move by bagh
    if b.turn == BAGH_NUMBER and dragDict["piece"]==BAGH_NUMBER:
        difference=abs(int(fromSq)-int(toSq))
        if difference != 1 and difference !=5 and difference!= 6:
            for d1 in JUMP_CONNECTIONS[int(fromSq)]:
                if d1["jump_destination"]==int(toSq):
                    jump= f'{d1["jump_over"]:02d}'
                    move_code+=jump
    if move_code in b.legal_moves:
        b.make_move(move_code)


pygame.font.init()

game_end_font_size=int(SCREEN_WIDTH * 0.04)
game_end_font = pygame.font.SysFont('Comic Sans MS', game_end_font_size)

def updateDetails():
    #Remaining Goats
    remaining_goats=20-b.captured_goats-len(b.goat_occupancy)
    if remaining_goats > 1 or (remaining_goats==1 and not REM_GOAT['drag']):
        goat=Goat()
        goat.update(remainingGoatX,remainingGoatY)

    font_size=int(SCREEN_HEIGHT*0.04)
    my_font = pygame.font.SysFont('Comic Sans MS', font_size)
    text_surface = my_font.render('Remaining Goats: '+ str(remaining_goats), False, (0, 0, 0))
    screen.blit(text_surface, (remainingGoatX*0.4,remainingGoatY+ 2*font_size))

    # Captured Goats
    text_surface = my_font.render('Captured Goats: '+ str(b.captured_goats), False, (0, 0, 0))
    screen.blit(text_surface, (remainingGoatX*0.4,remainingGoatY+4*font_size))

    # PHASE
    if b.phase==PHASES["PLACEMENT"]:
        phase='Placement'
    else:
        phase='Movement'
    text_surface = my_font.render('Phase: '+ phase, False, (0, 0, 0))
    screen.blit(text_surface, (remainingGoatX*0.4,remainingGoatY+6*font_size))

    # Turn
    if b.turn==BAGH_NUMBER:
        turn='BAGH'
    else:
        turn='goat'
    text_surface = my_font.render('Turn: '+ turn, False, (0, 0, 0))
    screen.blit(text_surface, (remainingGoatX*0.6,remainingGoatY+8*font_size))

    if b.game_end:
        if b.victor==BAGH_NUMBER:
            winner='BAGH'
        elif b.victor==GOAT_NUMBER:
            winner='goat'
        game_end_text = game_end_font.render('Winner: '+ winner, False, (0, 0, 0))
        screen.blit(game_end_text, (SCREEN_WIDTH*0.3,SCREEN_HEIGHT*0.4))

def isRemGoatDrag(mx,my):
    if b.turn==GOAT_NUMBER and b.phase==PHASES["PLACEMENT"] and mx > (remainingGoatX - goatWidth*0.2) and mx < (remainingGoatX + goatWidth*1.2) and my > (remainingGoatY - goatWidth*0.2)  and my < (remainingGoatY + goatHeight*1.2):
        return True
    else:
        return False
def dragFromRemainingGoats():

    if REM_GOAT['drag']:
        mx,my=pygame.mouse.get_pos()
        goat=Goat()

        mx,my=mx-goatWidth/2,my-goatHeight/2
        goat.update(mx,my)


def dropFromRemainingGoats():
    if REM_GOAT['drag']:
        mx,my=pygame.mouse.get_pos()
        toSq=xyToInd(mx,my)
        if toSq<0 or toSq>24: #check what happens if outside board, we should prob break if toSq< 0 or > 24
            return
        toSq=f"{toSq:02d}"
        move_code='G'+toSq
        if move_code in b.legal_moves:
            b.make_move(move_code)
        REM_GOAT['drag']=False
b=Board()



# import numpy as np

# import random
# def random_chooser(lst):
#   return random.choice(lst)

# def simulate_game(n_moves):
#     count=0
#     while n_moves>count:
#         count+=1
#         available_moves=b.legal_moves
#         choosen_move=random_chooser(available_moves)
#         b.make_move(choosen_move)

#         if b.game_end==True:
#             return np.array(b.victor),np.array(b.history['positions'])

def screenDraw():
    screen.fill((255,255,255))
    drawBoard()
    for sq in b.bagh_occupancy:
        if sq!= dragDict["index"]:
            drawBagh(sq)
    for sq in b.goat_occupancy:
        if sq!= dragDict["index"]:
            drawGoat(sq)
    dragPiece()
    updateDetails()
    dragFromRemainingGoats()

GAME={
    'running':True
}
def evenHandler():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                GAME["running"] = False
        elif event.type == QUIT:
            GAME["running"] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx,my=pygame.mouse.get_pos()
                index=xyToInd(mx,my)
                if index in b.bagh_occupancy and b.turn==BAGH_NUMBER:
                    dragDict["piece"]=BAGH_NUMBER
                    dragDict["drag"]=True
                    dragDict["index"]=index
                if index in b.goat_occupancy and b.turn==GOAT_NUMBER and b.phase == PHASES["MOVEMENT"]:
                    dragDict["piece"]=GOAT_NUMBER
                    dragDict["drag"]=True
                    dragDict["index"]=index

                if isRemGoatDrag(mx,my):
                    REM_GOAT['drag']=True
                    dragFromRemainingGoats()

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragDict["drag"]:
                dropPiece()
            dragDict["drag"]=False
            dragDict["index"]=100

            dropFromRemainingGoats()

def main():
    #simulate_game(20)
    
    clock = pygame.time.Clock()
    while GAME["running"]:
        screenDraw()
        evenHandler()
        pygame.display.flip()
        clock.tick(20)



if __name__ == '__main__':
    main()