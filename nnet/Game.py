import re

import  sys
sys.path.append('..')
from game.boardLogic import *

a=np.arange(N_COLUMNS*N_ROWS)
a.shape=(5,5)
a_ud=np.flipud(a)
SYMMETRY_MOVES_DCT={}
S_CODES=['90','180','270','u_0','u_90','u_180','u_270']
from scipy.ndimage import rotate
for s_code in S_CODES:
    #[rotate(a, angle=90),rotate(a, angle=180),rotate(a, angle=270),a_ud,rotate(a_ud, angle=90),rotate(a_ud, angle=180),rotate(a_ud, angle=270)]:
    a=np.arange(25)
    a.shape=(5,5)
    if 'u' in s_code:
        a=np.flipud(a)
    a=rotate(a,angle=int(s_code.split('_')[-1]))
    flat_symmetry=a.flatten()
    dct={}

    for move in ALL_MOVES:
        s=str(move)
        i,j=1,3
        if move[:2]!='no': # filter nomoves
            pick=int(move[i:j])
            s=s[:i] + f"{flat_symmetry[pick]:02}" + s[j:] #f"{a:02}"

            i,j=3,5
            if move[i:j]: 
                pick=int(move[i:j])
                s=s[:i] + f"{flat_symmetry[pick]:02}" + s[j:]

                i,j=5,7
                if move[i:j]: 
                    pick=int(move[i:j])
                    s=s[:i] + f"{flat_symmetry[pick]:02}" + s[j:]
        dct[s]=move
    SYMMETRY_MOVES_DCT[s_code]=dct

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
        return b

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
        return np.concatenate(player*np.array(board.board_array) , N_COLUMNS*N_ROWS*[board.phase])

    def getSymmetries(self, board, pi): #does this board also include phase information?
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        PI_dct=dict(zip(ALL_MOVES, list(pi)))
        PI_dct_modifiable=dict(zip(ALL_MOVES, list(pi)))

        return_list=[]
        for s_code in S_CODES:
            #symmetric PI
            for move in ALL_MOVES:
                corresp_move=SYMMETRY_MOVES_DCT[s_code][move]
                val=PI_dct[move]
                PI_dct_modifiable[corresp_move]=val
            PI_symmetry=np.array(list(PI_dct_modifiable.values()))
            #symmetric board
            brd_array=board.board_array 
            arr=brd_array
            arr=np.shape(N_ROWS,N_COLUMNS)
            if 'u' in s_code:
                arr=np.flipud(a)
            arr=rotate(arr,angle=int(s_code.split('_')[-1]))
            flat_symmetry=arr.flatten()
            board_symmetry=np.concatenate(flat_symmetry,N_INTERSECTIONS*[board.phase])
            return_list.append((flat_symmetry,PI_symmetry))

        return return_list
        
    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return board.board_string
