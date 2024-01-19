from array import *
from AStar import AStar

# Grid
size = 10
robotEnviromint = [[0]*size for _ in range(size)]
print()
AStar(robotEnviromint, size)
