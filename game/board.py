
N_ROWS=5 # Rows in baghchal board
N_COLUMNS=N_ROWS # Columns in baghchal board
TOTAL_INTERSECTIONS = N_ROWS*N_COLUMNS

# Number of baghs and goat
TOTAL_BAGHS=4
TOTAL_GOATS=20

# Letter Notations
BAGH_LETTER='B'
GOAT_LETTER='G'

# Numeric Notations
BAGH_NUMBER=2
GOAT_NUMBER=1
EMPTY_NUMBER=0

# Initial baghs squares
INITIAL_BAGH_SQ=[0,4,20,24]

#phases
PHASES={
    'PLACEMENT':0,
    'MOVEMENT':1
}
PLACEMENT = TOTAL_GOATS * 2 -1

#action space
ACTION_SIZE = 331

class Conversion:
    def to_coordinate(n): # Examples: 0 = (1,1) ; 1 = (1,2) ; ... ; 9 = (2,5) ; 21 = (5,2)
        n+=1
        return (n-1)//5 +1, n-((n-1)//5 * 5)

    def to_serial(xy):
        return (xy[0]-1)*5 + xy[1] -1

def mid_point(coordinate1,coordinate2):
    x1,y1,x2,y2=coordinate1[0],coordinate1[1],coordinate2[0],coordinate2[1]
    return [int((x1+x2)/2),int((y1+y2)/2)]

def connections():
    return_dict={}
    for n in range(0,TOTAL_INTERSECTIONS):
        return_dict[n]=[]
        i,j=Conversion.to_coordinate(n)

        if (i+j)%2 == 0: # Even sum: slanted connections too
            for ij in [[i-1,j],[i+1,j],[i,j-1],[i,j+1],[i-1,j-1],[i+1,j+1],[i-1,j+1],[i+1,j-1]]: #upto 8 possible
                if 0 < ij[0] <= N_ROWS and 0 < ij[1] <= N_COLUMNS: #filter those out of range
                    return_dict[n].append(Conversion.to_serial([ij[0],ij[1]]))

            
        else: #Odd sum: no slanted connections
            for ij in [[i-1,j],[i+1,j],[i,j-1],[i,j+1]]: #upto 4 possible
                if 0 < ij[0] <= N_ROWS and 0 < ij[1] <= N_COLUMNS:
                    return_dict[n].append(Conversion.to_serial([ij[0],ij[1]]))
    
    return return_dict

def jump_connections():
    return_dict={}
    for n in range(0,TOTAL_INTERSECTIONS):
        return_dict[n]=[]
        i,j=Conversion.to_coordinate(n)

        if (i+j)%2 == 0: # Even sum: slanted connections too
            for ij in [[i-2,j],[i+2,j],[i,j-2],[i,j+2],[i-2,j-2],[i+2,j+2],[i-2,j+2],[i+2,j-2]]: #upto 8 possible
                if 0 < ij[0] <= N_ROWS and 0 < ij[1] <= N_COLUMNS: #filter those out of range
                    return_dict[n].append({
                        'jump_destination': Conversion.to_serial([ij[0],ij[1]]),
                        'jump_over': Conversion.to_serial(mid_point([ij[0],ij[1]],[i,j]))
                        })
            
        else: #Odd sum: no slanted connections
            for ij in [[i-2,j],[i+2,j],[i,j-2],[i,j+2]]: #upto 4 possible
                if 0 < ij[0] <= N_ROWS and 0 < ij[1] <= N_COLUMNS:
                    return_dict[n].append({
                        'jump_destination': Conversion.to_serial([ij[0],ij[1]]),
                        'jump_over': Conversion.to_serial(mid_point([ij[0],ij[1]],[i,j]))
                        })

    return return_dict

# Look up values
CONNECTIONS=connections()
JUMP_CONNECTIONS=jump_connections()

class Board:
    def __init__(self):
        self.board_array=[EMPTY_NUMBER]*TOTAL_INTERSECTIONS
        self.bagh_occupancy=[0,4,20,24]
        self.goat_occupancy=[]

        # initialize baghs
        for square in [0,4,20,24]:
            self.board_array[square]=BAGH_NUMBER

        self.phase=PHASES['PLACEMENT']
        self.position_string = self.stringify_position()

        self.captured_goats=0
        self.turn=GOAT_NUMBER


        self.history={
            'positions':[],
            'pgn':[]
        }
        

        self.repetitions={}
        self.thrice_repetition=False

        self.draw = False
        self.victor=None
        self.game_end=False

        self.bagh_moves=self.legal_bagh_moves()
        self.goat_moves=self.legal_goat_moves()
        self.legal_moves=[]
        self.legal_moves_function()

             
        

    def switch_turn(self):
        if self.turn == BAGH_NUMBER:
            self.turn = GOAT_NUMBER
        else:
            self.turn = BAGH_NUMBER

        if len(self.history['pgn']) >= PLACEMENT:
            self.phase = PHASES['MOVEMENT']
        else:
            self.phase = PHASES['PLACEMENT']

    def check_repetitions(self):
        if self.position_string in self.history['positions']:
            if self.position_string not in self.repetitions:
                self.repetitions[self.position_string] = 1
            else:
                self.repetitions[self.position_string] += 1
                # is this third time?
                if self.repetitions[self.position_string] >= 3:
                    self.thrice_repetition = True

    def uncheck_repetition(self):
        if self.position_string in self.repetitions:
            if self.repetitions[self.position_string] == 1:
                del self.repetitions[self.position_string]
            else:
                self.repetitions[self.position_string] -= 1                
                self.thrice_repetition = False #for both 3 and 2

    def stringify_position(self):
        return ''.join(str(i) for i in self.board_array)
        
    def put_bagh(self,square):
        self.board_array[square]=BAGH_NUMBER
        self.bagh_occupancy.append(square)

    def put_goat(self,square):
        self.board_array[square]=GOAT_NUMBER
        self.goat_occupancy.append(square)

    def remove_bagh(self,square):
        self.board_array[square]=EMPTY_NUMBER
        self.bagh_occupancy.remove(square)

    def remove_goat(self,square):
        self.board_array[square]=EMPTY_NUMBER
        self.goat_occupancy.remove(square)

    def legal_goat_moves(self):
        return_l =[]    
        if self.turn==GOAT_NUMBER:          
          if self.phase == PHASES['PLACEMENT']:            
              for square in range(len(self.board_array)):
                  if self.board_array[square] == EMPTY_NUMBER:
                      return_l.append(GOAT_LETTER+f"{square:02d}")            
          else:
              for square in self.goat_occupancy:
                  for connection in CONNECTIONS[square]:
                      if self.board_array[connection] == EMPTY_NUMBER:
                          return_l.append(GOAT_LETTER+f"{connection:02d}"+f"{square:02d}")
        self.goat_moves=return_l
        return return_l

    def legal_bagh_moves(self):
        return_l=[]
        if self.turn==BAGH_NUMBER:
          for square in self.bagh_occupancy:
              for connection in CONNECTIONS[square]:
                  if self.board_array[connection] == EMPTY_NUMBER:
                      return_l.append(BAGH_LETTER+f"{connection:02d}"+f"{square:02d}")                    
              for jump_connection in JUMP_CONNECTIONS[square]:
                  if self.board_array[jump_connection['jump_destination']] == EMPTY_NUMBER and self.board_array[jump_connection['jump_over']] == GOAT_NUMBER:
                      return_l.append(BAGH_LETTER+f"{jump_connection['jump_destination']:02d}"+f"{square:02d}"+f"{jump_connection['jump_over']:02d}")                    
        self.bagh_moves=return_l
        return return_l

    

    def bagh_victory(self):
        if self.captured_goats >= 5:
            self.victor = BAGH_NUMBER
            self.game_end=True

    def goat_victory(self):
        if  self.turn==BAGH_NUMBER and len(self.bagh_moves)==0:
            self.victor = GOAT_NUMBER
            self.game_end=True

    def is_draw(self):
        if (self.turn==GOAT_NUMBER and len(self.goat_moves) == 0) or self.thrice_repetition == True:
            self.draw = True
            self.game_end=True

    def legal_moves_function(self):
      self.legal_goat_moves()
      self.legal_bagh_moves()

      if self.turn==GOAT_NUMBER:
        self.legal_moves= self.goat_moves
      else:
        self.legal_moves= self.bagh_moves

      self.bagh_victory()
      self.goat_victory()
      self.is_draw()

      if self.game_end:
        self.legal_moves=[]

    def move_bagh(self,move):
        if move[0]==BAGH_LETTER:
            self.remove_bagh(int(move[3:5]))
            self.put_bagh(int(move[1:3]))
            if move[5:7]:
                self.remove_goat(int(move[5:7]))
                self.captured_goats += 1

    def move_goat(self,move):
        if move[0]==GOAT_LETTER:
            self.put_goat(int(move[1:3]))
            if move[3:5]:
                self.remove_goat(int(move[3:5])) 


    def make_move(self,move):
        if move[0]==BAGH_LETTER:
            self.move_bagh(move)
        else:
            self.move_goat(move)
        self.switch_turn()
        self.legal_moves_function()
        
        #add history
        self.position_string = self.stringify_position()
        self.check_repetitions() #before updating history 
        self.history['pgn'].append(move)
        self.history['positions'].append(self.position_string)

    def move_back(self):
        self.uncheck_repetition() #this happens before history is reverted
        move = self.history['pgn'].pop()  
        
        if move[0] == BAGH_LETTER:
            self.remove_bagh(int(move[1:3]))
            self.put_bagh(int(move[3:5]))
            if move[5:7]:
                self.put_goat(int(move[5:7]))
                self.captured_goats -= 1

        else:
            self.remove_goat(int(move[1:3]))
            if move[3:5]:
                self.put_goat(int(move[3:5]))        
        
        self.switch_turn()
        self.legal_moves_function()
        self.game_end=False

        self.history['positions'].remove(self.position_string)
        self.position_string = self.stringify_position() #revert to previous string

        