import  sys
sys.path.append('..')
from boardLogic import *



import random
def random_chooser(lst):
  return random.choice(lst)
  

def simulate_game():
  b= Board()
  while True:
    available_moves=b.legal_moves
    choosen_move=random_chooser(available_moves)
    b.make_move(choosen_move)

    if b.game_end==True:
      print(b.history)

      return b.history
      
simulate_game()