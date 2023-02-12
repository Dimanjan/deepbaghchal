import random
import time

class MCTS:
    def __init__(self, brd, timeout=3.0):
        self.brd = brd
        self.timeout = timeout

    def search(self):
        start_time = time.time()
        root = Node(None, 1)

        while time.time() - start_time < self.timeout:
            node = root
            brd_copy = self.brd.clone()
            print('cloned')

            # Selection
            while not node.is_leaf():
                print('selection')
            

                node = node.select_child()
                brd_copy.make_move(node.move)

                if brd_copy.game_end:
                    break

            # Expansion
            if not brd_copy.game_end:
                print('expansion')
                node.expand(brd_copy)
                print('expanded')

                node = node.select_child()
                print('child selected')

                brd_copy.make_move(node.move)

            # Simulation
            while not brd_copy.game_end:
                print('simulation')

                brd_copy.make_move(random.choice(brd_copy.legal_moves))

            # Backpropagation
            while node is not None:
                print('backpropagation')

                result = brd_copy.victor
                node.update_stats(result)
                node = node.parent

        # Choose the move with the highest number of wins
        best_move = root.most_visited_child().move
        return best_move

from math import log, sqrt
class Node:
    def __init__(self, parent, move=None):
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0

    def is_leaf(self):
        return not self.children

    def select_child(self):
        total_visits = sum(child.visits for child in self.children)
        print('total_visits',total_visits)

        exploration_constant = 1.0 / (2 * log(total_visits + 1+ 1e-10))

        def uct(node):
            print(log(total_visits) , (node.visits + 1e-10))
            return node.wins / (node.visits + 1e-10) + exploration_constant * sqrt(log(total_visits) / (node.visits + 1e-10))

        return max(self.children, key=uct)

    def expand(self, brd):
        for move in brd.legal_moves:
            self.children.append(Node(self, move))

    def update_stats(self, result):
        self.visits += 1
        self.wins += result
    
    def most_visited_child(self):
        return max(self.children, key=lambda x: x.visits)

import  sys
sys.path.append('..')
from game.boardLogic import *

brd = Board() # create an instance of the board game
mcts = MCTS(brd) # create an instance of the MCTS algorithm

while not brd.game_end and not brd.draw:
    if brd.turn == BAGH_NUMBER:
        print('bagh turn')

        # Bagh's turn
        move = mcts.search()
        brd.make_move(move)
    else:
        print('goat turn')
        # Goat's turn
        #move = input("Enter your move (format: 'row col'): ")
        print('searching on mcts')
        move = mcts.search()
        
        brd.make_move(move)

result = brd.victor
if result == 1:
    print("Bagh wins!")
elif result == -1:
    print("Goat wins!")
else:
    print("It's a draw.")
