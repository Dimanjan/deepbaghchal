
import  sys, os
sys.path.insert(0, os.path.dirname(os.getcwd()))
from board import *
brd=Board()

import pygame
pygame.init()
from pygame.locals import *
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



SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 0.7 * SCREEN_WIDTH


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

baghWidth=boardWidth/(N_ROWS+1)
baghHeight=boardHeight/(N_COLUMNS+1)
goatWidth=baghWidth*0.7
goatHeight=baghHeight*0.7

GAME={
    'running':True,
    'moveBackX':SCREEN_WIDTH*0.5,
    'moveBackY':SCREEN_HEIGHT*0.02,
    'moveBackWidth':SCREEN_WIDTH*0.24,
    'moveBackHeight':SCREEN_HEIGHT*0.1

}

dragDict={
    "drag":False,
    "piece":BAGH_NUMBER,
    "index":100,
}

GAME["screen"] = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Bagh(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bagh.png")
        self.image=pygame.transform.scale(self.image, (baghWidth,baghHeight))

    def update(self,bx,by):
        self.rect=self.image.get_rect(topleft = (bx,by))
        GAME["screen"].blit(self.image, (bx,by))

class Goat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/goat.png")
        self.image=pygame.transform.scale(self.image, (goatWidth,goatHeight))

    def update(self,bx,by):
        self.rect=self.image.get_rect(topleft = (bx,by))
        GAME["screen"].blit(self.image, (bx,by))

def drawBoard():
    picture = pygame.image.load('img/board.svg')
    picture = pygame.transform.scale(picture, (boardWidth, boardHeight))
    GAME["screen"].blit(picture, (MARGIN["left"], MARGIN["top"]))

def drawBagh(sq):
    i,j=indToIJ(sq)
    bagh=Bagh()
    x=MARGIN["left"]+i*boardWidth/4 - baghWidth/2
    y=MARGIN["top"]+j*boardHeight/4 - baghHeight/2
    bagh.update(x,y)

def drawGoat(sq):
    i,j=indToIJ(sq)
    goat=Goat()
    x=MARGIN["left"]+i*boardWidth/4 - goatWidth/2
    y=MARGIN["top"]+j*boardHeight/4 - goatHeight/2
    goat.update(x,y)

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
    if brd.turn == BAGH_NUMBER and dragDict["piece"]==BAGH_NUMBER:
        difference=abs(int(fromSq)-int(toSq))
        if difference != 1 and difference !=5 and difference!= 6:
            for d1 in JUMP_CONNECTIONS[int(fromSq)]:
                if d1["jump_destination"]==int(toSq):
                    jump= f'{d1["jump_over"]:02d}'
                    move_code+=jump
    if move_code in brd.legal_moves:
        brd.make_move(move_code)

pygame.font.init()
game_end_font_size=int(SCREEN_WIDTH * 0.04)
game_end_font = pygame.font.SysFont('Comic Sans MS', game_end_font_size)

def isRemGoatDrag(mx,my):
    if brd.turn==GOAT_NUMBER and brd.phase==PHASES["PLACEMENT"] and mx > (remainingGoatX - goatWidth*0.2) and mx < (remainingGoatX + goatWidth*1.2) and my > (remainingGoatY - goatWidth*0.2)  and my < (remainingGoatY + goatHeight*1.2):
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
        if move_code in brd.legal_moves:
            brd.make_move(move_code)
        REM_GOAT['drag']=False

def drawMoveBack():
    WHITE=(255,255,255)
    BLUE=(0,0,255)
    pygame.draw.rect(GAME["screen"],BLUE,(GAME['moveBackX'],GAME['moveBackY'],GAME['moveBackWidth'],GAME['moveBackHeight']))
    mbText = game_end_font.render('Move Back', False, WHITE)
    GAME["screen"].blit(mbText, (GAME['moveBackX']*1.04,GAME['moveBackY']))

def moveBackEvent(mx,my):
    if mx >GAME['moveBackX'] and my > GAME['moveBackY'] and mx<GAME['moveBackX']+GAME['moveBackWidth'] and my<GAME['moveBackY']+GAME['moveBackHeight']:
        brd.move_back()
