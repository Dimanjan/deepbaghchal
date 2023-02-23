import  sys
sys.path.append('..')
from boardLogic import *



import random
def random_chooser(lst):
  return random.choice(lst)
  
baghWinList=[]
goatWinList=[]
drawList=[]

def simulate_game():
  b= Board()
  while not b.game_end:
    available_moves=b.legal_moves
    #print(b.captured_goats,available_moves)
    choosen_move=random_chooser(available_moves)
    b.make_move(choosen_move)
        
    if b.game_end==True:
      if b.victor==1:
        goatWinList.append(b.history['positions'])
      elif b.victor==-1:
        baghWinList.append(b.history['positions'])
      else:
        drawList.append(b.history['positions'])

game_counter=1
for i in range(100000):
  print('Game ',game_counter)
  game_counter+=1

  simulate_game()




def writeToTXT(lst, filename):

  with open('data/'+filename+'.txt', 'w') as file:
    for item in lst:
        file.write(str(item) + '\n')


writeToTXT( sum(goatWinList, []), 'goatWinList')

writeToTXT(sum(baghWinList[:len(goatWinList)], []) , 'baghWinList')

writeToTXT(sum(drawList, []), 'drawList')
