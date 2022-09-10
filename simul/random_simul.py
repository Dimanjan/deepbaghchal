
from pathlib import Path

import sys
sys.path.insert(0, str(Path().absolute())+'/game')
 
from board import Board



import numpy as np

import random
def random_chooser(lst):
  return random.choice(lst)
  

def simulate_game():
  b= Board()
  while True:
    available_moves=b.legal_moves
    choosen_move=random_chooser(available_moves)
    print(choosen_move)
    b.make_move(choosen_move)

    if b.game_end==True:
      return np.array(b.victor),np.array(b.history['positions'])

simulate_game()