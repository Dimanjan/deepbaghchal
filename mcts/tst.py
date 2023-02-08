import sys
import os
path_to_game= os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "game")
print(path_to_game)
sys.path.append(path_to_game)