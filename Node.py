# Initializing node class that will be implemented in each pos in the map(grid)
class Node:

    # Base node class constructor
    def __init__(self, x, y, g = 0, h = 0, parent = None):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.parent = parent

    # Calculate the f(n) function
    def f(self):
        return self.g + self.h
