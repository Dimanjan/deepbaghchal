import  sys
sys.path.append('deepbaghchal/game/')
from boardLogic import *



import random
def random_chooser(lst):
  return random.choice(lst)

#load model
import tensorflow as tf
# Load the saved model from file
loaded_model = tf.keras.models.load_model('deepbaghchal/game/nnet/my_model.h5')

def pos_parse(pos):
    my_list = list(pos[:25])

    bagh = np.array([1 if x == 'B' else 0 for x in my_list])
    goat = np.array([1 if x == 'g' else 0 for x in my_list])
    if pos[25]=='0':
        phase=np.zeros(25)
    else:
        phase=np.ones(25)

    if pos[26]=='B':
        turn=np.zeros(25)
    else:
        turn=np.ones(25)
    
    concatenated=np.concatenate([bagh,goat,turn,phase])
    return concatenated

def ModelChoice(brd):
    valDict={}
    for move in brd.legal_moves:
        brd.make_move(move)
        pos=brd.history['positions'][-1]

        val=loaded_model.predict(np.array([pos_parse(pos)]), verbose=0)
        valDict[move]=val[0][0]

        brd.move_back()

    if brd.turn==GOAT_NUMBER:
        selected_move = max(valDict, key=lambda k: valDict[k])
    else:
        selected_move= min(valDict, key=lambda k: valDict[k])

    return selected_move

import random


OPENING={
    'model':True
}
MODELS_TURN=True
def random_vs_myModel():
  brd= Board()

  OPENING['model']^=1
  if OPENING['model']:
    randoms_turn=False
  else:
    randoms_turn=True

  while True:
    if randoms_turn:
        choosen_move=random_chooser(brd.legal_moves)
    else:
        choosen_move=ModelChoice(brd)
    brd.make_move(choosen_move)
    randoms_turn^=1
    if brd.game_end==True:
        if brd.victor==GOAT_NUMBER and OPENING['model'] or brd.victor==BAGH_NUMBER and not OPENING['model']:
            victory_count['model']+=1
        else:
            victory_count['random']+=1 
        return 
    

victory_count={
        'model':0,
        'random':0
    }   
for _ in range(100):
    print(victory_count)
    random_vs_myModel()

print(victory_count)