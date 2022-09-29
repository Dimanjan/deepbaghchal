import re

import  sys
sys.path.append('..')
from game.boardLogic import *
print(N_COLUMNS)

import numpy as np
class Game():
    """
    This class specifies the base Game class. To define your own game, subclass
    this class and implement the functions below. This works when the game is
    two-player, adversarial and turn-based.

    Use 1 for player1 and -1 for player2.

    See othello/OthelloGame.py for an example implementation.
    """
    def __init__(self):
        pass

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        b=Board()
        return np.array(b.board_array)

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return (N_ROWS,N_COLUMNS)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return 331 # only for 5*5 board

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        if action in board.legal_moves:
            board.make_move(action)
        return (board,-player)

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        if len(board.legal_moves)==0:
            if board.turn==BAGH_NUMBER:
                return np.in1d(board.action_space, ['nomovebagh'])
            else:
                return np.in1d(board.action_space, ['nomovegoat'])
        return np.in1d(board.action_space, board.legal_moves)

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        if not board.game_end:
            return 0
        if board.draw:
            return 0.0000001
        if board.victor==board.turn:
            return 1
        else:
            return -1

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        return board.turn*np.array(board.board_array) #+[board.turn,board.phase])

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        nr=np.reshape(board.board_array,(N_ROWS,N_COLUMNS))
        return [(nr,0),(np.fliplr(nr),1),(np.flip(nr),2),(np.flipud(nr),2)] #sends 2d but 1 maybe?

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return board.position_string
