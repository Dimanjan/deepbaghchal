from base import *

def updateDetails():
    #Remaining Goats
    remaining_goats=20-brd.captured_goats-len(brd.goat_occupancy)
    if remaining_goats > 1 or (remaining_goats==1 and not REM_GOAT['drag']):
        goat=Goat()
        goat.update(remainingGoatX,remainingGoatY)

    font_size=int(SCREEN_HEIGHT*0.04)
    my_font = pygame.font.SysFont('Comic Sans MS', font_size)
    text_surface = my_font.render('Remaining Goats: '+ str(remaining_goats), False, (0, 0, 0))
    GAME["screen"].blit(text_surface, (remainingGoatX*0.4,remainingGoatY+ 2*font_size))

    # Captured Goats
    text_surface = my_font.render('Captured Goats: '+ str(brd.captured_goats), False, (0, 0, 0))
    GAME["screen"].blit(text_surface, (remainingGoatX*0.4,remainingGoatY+4*font_size))

    # PHASE
    if brd.phase==PHASES["PLACEMENT"]:
        phase='Placement'
    else:
        phase='Movement'
    text_surface = my_font.render('Phase: '+ phase, False, (0, 0, 0))
    GAME["screen"].blit(text_surface, (remainingGoatX*0.4,remainingGoatY+6*font_size))

    # Turn
    if brd.turn==BAGH_NUMBER:
        turn='BAGH'
    else:
        turn='goat'
    text_surface = my_font.render('Turn: '+ turn, False, (0, 0, 0))
    GAME["screen"].blit(text_surface, (remainingGoatX*0.6,remainingGoatY+8*font_size))

    if brd.game_end:
        if brd.victor==BAGH_NUMBER:
            winner='BAGH'
        elif brd.victor==GOAT_NUMBER:
            winner='goat'
        elif brd.draw:
            winner = 'Draw'
        game_end_text = game_end_font.render('Winner: '+ winner, False, (0, 0, 0))
        GAME["screen"].blit(game_end_text, (SCREEN_WIDTH*0.3,SCREEN_HEIGHT*0.4))

def screenDraw():
    GAME["screen"].fill((255,255,255))
    drawBoard()
    drawMoveBack()
    for sq in brd.bagh_occupancy:
        if sq!= dragDict["index"]:
            drawBagh(sq)
    for sq in brd.goat_occupancy:
        if sq!= dragDict["index"]:
            drawGoat(sq)
    dragPiece()
    updateDetails()
    dragFromRemainingGoats()

# import numpy as np

# import random
# def random_chooser(lst):
#   return random.choice(lst)

# def simulate_game(n_moves):
#     count=0
#     while n_moves>count:
#         count+=1
#         available_moves=brd.legal_moves
#         choosen_move=random_chooser(available_moves)
#         brd.make_move(choosen_move)

#         if brd.game_end==True:
#             return np.array(brd.victor),np.array(brd.history['positions'])



def eventHandler():
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
                
                if index in brd.bagh_occupancy and brd.turn==BAGH_NUMBER:
                    dragDict["piece"]=BAGH_NUMBER
                    dragDict["drag"]=True
                    dragDict["index"]=index
                

                if index in brd.goat_occupancy and brd.turn==GOAT_NUMBER and brd.phase == PHASES["MOVEMENT"]:
                    dragDict["piece"]=GOAT_NUMBER
                    dragDict["drag"]=True
                    dragDict["index"]=index

                if isRemGoatDrag(mx,my):
                    REM_GOAT['drag']=True
                    dragFromRemainingGoats()

                moveBackEvent(mx,my)


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
        eventHandler()
        
        pygame.display.flip()
        clock.tick(20)



if __name__ == '__main__':
    main()