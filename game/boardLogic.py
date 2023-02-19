
N_ROWS=5 # Rows in baghchal board
N_COLUMNS=N_ROWS # Columns in baghchal board
TOTAL_INTERSECTIONS = N_ROWS*N_COLUMNS

# Number of baghs and goat
TOTAL_BAGHS=4
TOTAL_GOATS=20

# Letter Notations
BAGH_LETTER='B'
GOAT_LETTER='g'

# Numeric Notations
GOAT_NUMBER=1
BAGH_NUMBER= -GOAT_NUMBER
EMPTY_NUMBER=0

# Initial baghs squares
INITIAL_BAGH_SQ=[0,4,20,24]

#phases
PHASES={
    'PLACEMENT':-1, # inside board logic, it is also referred to as 0 (for stringify purpose)
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

ALL_MOVES=['G00','G01', 'G02', 'G03','G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10',
       'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19','G20',
       'G21', 'G22', 'G23','G24',
       'G0500', 'G0100', 'G0600', 'G0601', 'G0001', 'G0201', 'G0702',
       'G0102', 'G0302', 'G0802', 'G0602', 'G0803', 'G0203', 'G0403',
       'G0904', 'G0304', 'G0804', 'G0005', 'G1005', 'G0605', 'G0106',
       'G1106', 'G0506', 'G0706', 'G0006', 'G1206', 'G0206', 'G1006',
       'G0207', 'G1207', 'G0607', 'G0807', 'G0308', 'G1308', 'G0708',
       'G0908', 'G0208', 'G1408', 'G0408', 'G1208', 'G0409', 'G1409',
       'G0809', 'G0510', 'G1510', 'G1110', 'G1610', 'G0610', 'G0611',
       'G1611', 'G1011', 'G1211', 'G0712', 'G1712', 'G1112', 'G1312',
       'G0612', 'G1812', 'G0812', 'G1612', 'G0813', 'G1813', 'G1213',
       'G1413', 'G0914', 'G1914', 'G1314', 'G0814', 'G1814', 'G1015',
       'G2015', 'G1615', 'G1116', 'G2116', 'G1516', 'G1716', 'G1016',
       'G2216', 'G1216', 'G2016', 'G1217', 'G2217', 'G1617', 'G1817',
       'G1318', 'G2318', 'G1718', 'G1918', 'G1218', 'G2418', 'G1418',
       'G2218', 'G1419', 'G2419', 'G1819', 'G1520', 'G2120', 'G1620',
       'G1621', 'G2021', 'G2221', 'G1722', 'G2122', 'G2322', 'G1622',
       'G1822', 'G1823', 'G2223', 'G2423', 'G1924', 'G2324', 'G1824',
       'nomovegoat',
       'B0500', 'B0100', 'B0600', 'B0601', 'B0001', 'B0201', 'B0702',
       'B0102', 'B0302', 'B0802', 'B0602', 'B0803', 'B0203', 'B0403',
       'B0904', 'B0304', 'B0804', 'B0005', 'B1005', 'B0605', 'B0106',
       'B1106', 'B0506', 'B0706', 'B0006', 'B1206', 'B0206', 'B1006',
       'B0207', 'B1207', 'B0607', 'B0807', 'B0308', 'B1308', 'B0708',
       'B0908', 'B0208', 'B1408', 'B0408', 'B1208', 'B0409', 'B1409',
       'B0809', 'B0510', 'B1510', 'B1110', 'B1610', 'B0610', 'B0611',
       'B1611', 'B1011', 'B1211', 'B0712', 'B1712', 'B1112', 'B1312',
       'B0612', 'B1812', 'B0812', 'B1612', 'B0813', 'B1813', 'B1213',
       'B1413', 'B0914', 'B1914', 'B1314', 'B0814', 'B1814', 'B1015',
       'B2015', 'B1615', 'B1116', 'B2116', 'B1516', 'B1716', 'B1016',
       'B2216', 'B1216', 'B2016', 'B1217', 'B2217', 'B1617', 'B1817',
       'B1318', 'B2318', 'B1718', 'B1918', 'B1218', 'B2418', 'B1418',
       'B2218', 'B1419', 'B2419', 'B1819', 'B1520', 'B2120', 'B1620',
       'B1621', 'B2021', 'B2221', 'B1722', 'B2122', 'B2322', 'B1622',
       'B1822', 'B1823', 'B2223', 'B2423', 'B1924', 'B2324', 'B1824',
       'B100005', 'B020001', 'B120006', 'B110106', 'B030102', 'B120207',
       'B000201', 'B040203', 'B140208', 'B100206', 'B130308', 'B010302',
       'B140409', 'B020403', 'B120408', 'B150510', 'B070506', 'B160611',
       'B080607', 'B180612', 'B170712', 'B050706', 'B090708', 'B180813',
       'B060807', 'B160812', 'B190914', 'B070908', 'B001005', 'B201015',
       'B121011', 'B221016', 'B021006', 'B011106', 'B211116', 'B131112',
       'B021207', 'B221217', 'B101211', 'B141213', 'B001206', 'B241218',
       'B041208', 'B201216', 'B031308', 'B231318', 'B111312', 'B041409',
       'B241419', 'B121413', 'B021408', 'B221418', 'B051510', 'B171516',
       'B061611', 'B181617', 'B081612', 'B071712', 'B151716', 'B191718',
       'B081813', 'B161817', 'B061812', 'B091914', 'B171918', 'B102015',
       'B222021', 'B122016', 'B112116', 'B232122', 'B122217', 'B202221',
       'B242223', 'B102216', 'B142218', 'B132318', 'B212322', 'B142419',
       'B222423', 'B122418',
       'nomovebagh']

import numpy as np
import copy 


class Board:
    def __init__(self):
        self.board_array=np.array([EMPTY_NUMBER]*TOTAL_INTERSECTIONS)
        self.bagh_occupancy=[0,4,20,24]
        self.goat_occupancy=[]

        # initialize baghs
        for square in [0,4,20,24]:
            self.board_array[square]=BAGH_NUMBER

        self.captured_goats=0
        self.turn=GOAT_NUMBER

        self.phase=PHASES['PLACEMENT']
        self.position_string = self.stringify_position()



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

        self.action_space=ALL_MOVES



    def update_phase(self):
        if len(self.history['pgn']) >= PLACEMENT:
            self.phase = PHASES['MOVEMENT']
            #self.board_array[TOTAL_INTERSECTIONS:]=PHASES['MOVEMENT']
        else:
            self.phase = PHASES['PLACEMENT']
            #self.board_array[TOTAL_INTERSECTIONS:]=PHASES['PLACEMENT']

        

    def switch_turn(self):
        self.turn = -self.turn

        self.update_phase()
        

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
        returnStr=''
        for i in list(self.board_array):
            
            if i == BAGH_NUMBER:
                returnStr+=BAGH_LETTER
            elif i == GOAT_NUMBER:
                returnStr+=GOAT_LETTER
            else: 
                returnStr+='0'
        if self.phase == -1:
            returnStr+='0'
        else:
            returnStr+='1'

        if self.turn == BAGH_NUMBER:
            returnStr+=BAGH_LETTER
        else:
            returnStr+=GOAT_LETTER

        return returnStr
            
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

    def clone(self):
        return copy.deepcopy(self)

    def reset(self):
        self.board_array=np.array([EMPTY_NUMBER]*TOTAL_INTERSECTIONS)
        self.bagh_occupancy=[0,4,20,24]
        self.goat_occupancy=[]

        # initialize baghs
        for square in [0,4,20,24]:
            self.board_array[square]=BAGH_NUMBER

        self.captured_goats=0
        self.turn=GOAT_NUMBER

        self.phase=PHASES['PLACEMENT']
        self.position_string = self.stringify_position()

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

        self.action_space=ALL_MOVES



