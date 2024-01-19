from Node import Node
import math
import re
import tkinter as tk
import random
import time

# Initializing AStar enviromint
class AStar:

    # Base AStar class constructor
    def __init__(self, robotEnviromint, size):
        self.robotEnviromint = robotEnviromint
        self.fring = []
        self.expandedNodes = []
        currentNode = None

        # Create a Tkinter window
        self.window = tk.Tk()
        self.window.title("Artificial Intelligence")
        self.window.geometry('720x720')
        self.window.resizable(True, True)

        # Define the size of each cell in pixels
        cell_size = size * size

        # Create a canvas to display the map grid
        canvas = tk.Canvas(self.window, width=len(robotEnviromint[0]) * 50, height=len(robotEnviromint) * 50)
        canvas.pack()

        # Call the draw_robotEnviromint function to initially draw the map grid
        self.draw_robotEnviromint(robotEnviromint, canvas, None, None)

        def generateObstacles(robotEnviromint, canvas, initial, goal, multiplie):
            self.resetBoard(canvas)
            for obs in range(0, size * multiplie[0]):
                x = random.randint(0, size - 1)
                y = random.randint(0, size - 1)
                obs_pos = [x, y]
                flag = False
                while flag == False: 
                    if obs_pos == goal or obs_pos == initial:
                        x = random.randint(0, size - 1)
                        y = random.randint(0, size - 1)
                        obs_pos = (x, y)
                    else: 
                        flag = True
                robotEnviromint[x][y] = 1

            self.draw_robotEnviromint(robotEnviromint, canvas, initial, goal)

        # Create buttons and text fields
        text1 = tk.Entry(self.window)
        text1.pack()

        text2 = tk.Entry(self.window)
        text2.pack()

        text3 = tk.Entry(self.window)
        text3.pack()

        button1 = tk.Button(self.window, text="Generate Obstacles", command = (lambda: generateObstacles(robotEnviromint, canvas, text1.get(), text2.get(), self.extract_numbers(text3.get()))))
        button1.pack()

        button2 = tk.Button(self.window, text="Start", command= (lambda: self.search(self.extract_numbers(text1.get()), self.extract_numbers(text2.get()), canvas)))
        button2.pack()

        # button2 = tk.Button(self.window, text="Reset", command = (lambda: self.resetBoard(canvas)))
        # button2.pack()

        # Start the Tkinter event loop
        self.window.mainloop()

    # A* search algorithm
    def search(self, initState, goalState, canvas):
        self.fring = []
        self.expandedNodes = []
        currentNode = None
        
        initNode = Node(initState[0], initState[1])
        goalNode = Node(goalState[0], goalState[1])
        self.fring.append(initNode)
        
        while len(self.fring) > 0:
            currentNode = min(self.fring, key = lambda node: node.f())

            if currentNode.x == goalNode.x and currentNode.y == goalNode.y:
                pathToGoal = []
                costToPath = currentNode.g
                while currentNode.parent is not None:
                    pathToGoal.append((currentNode.x, currentNode.y))
                    currentNode = currentNode.parent
                    
                pathToGoal.append((initState[0], initState[1]))
                pathToGoal.reverse()
                self.change_color(canvas, self.robotEnviromint, goalNode.x, goalNode.y, "red")
                self.change_color(canvas, self.robotEnviromint, self.expandedNodes[len(self.expandedNodes) - 1].x, self.expandedNodes[len(self.expandedNodes) - 1].y, "blue")
                for i in pathToGoal:
                    if i != pathToGoal[len(pathToGoal) - 1]:
                        self.change_color(canvas, self.robotEnviromint, i[0], i[1], 'yellow')
                print(pathToGoal)
                return

            else:
                self.change_color(canvas, self.robotEnviromint, currentNode.x, currentNode.y, "red")

            if len(self.expandedNodes) != 0:
                self.change_color(canvas, self.robotEnviromint, self.expandedNodes[len(self.expandedNodes) - 1].x, self.expandedNodes[len(self.expandedNodes) - 1].y, "blue")
            time.sleep(0.1)
            self.window.update()

            self.fring.remove(currentNode)
            self.expandedNodes.append(currentNode)

            for xCoordinates in range(-1, 2):

                for yCoordinates in range(-1, 2):
                    
                    if xCoordinates == 0 and yCoordinates == 0:
                        continue

                    x = currentNode.x + xCoordinates
                    y = currentNode.y + yCoordinates

                    if x < 0 or x >= len(self.robotEnviromint) or y < 0 or y >= len(self.robotEnviromint[0]):
                        continue

                    if self.robotEnviromint[x][y] == 1:
                        continue

                    if xCoordinates == 0 or yCoordinates == 0:
                        cost = 1
                    else:
                        cost = math.sqrt(2)

                    neighborNode = Node(x, y, currentNode.g + cost)

                    b = False
                    for i in self.expandedNodes:
                        if i.x == neighborNode.x and i.y == neighborNode.y:
                            a = True
                            continue
                    
                    if b is True:
                        continue

                    a = False
                    for i in self.fring:
                        if i.x == neighborNode.x and i.y == neighborNode.y:
                            a = True
                            continue
                    
                    if a is True:
                        continue

                    if neighborNode not in self.fring:
                        neighborNode.h = self.heuristic(neighborNode, goalNode)
                        neighborNode.parent = currentNode
                        self.fring.append(neighborNode)
                    else:
                            
                        if neighborNode.g < currentNode.g:
                            neighborNode.g = currentNode.g + costToPath
                            neighborNode.parent = currentNode
                    
        return None
    #  Euclidean distance formula
    def heuristic(self, node, goalState):
        dx = abs(node.x - goalState.x)
        dy = abs(node.y - goalState.y)
        return math.sqrt(dx * dx + dy * dy) + (math.sqrt(2) - 2) * min(dx, dy)

    def extract_numbers(self, string):
        numbers = re.findall(r'\d+', string)
        numbers = [int(num) for num in numbers]
        return numbers

    def draw_robotEnviromint(self, robotEnviromint, canvas, initial, goal):
        
        canvas.delete("all")  # Clear the canvas
        for row in range(len(robotEnviromint)):
            for col in range(len(robotEnviromint[row])):
                if robotEnviromint[row][col] == 0:
                    color = "white"
                else:
                    color = "black"
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        if initial is not None:

            # Set the initial state to
            x1 = self.extract_numbers(initial)[1] * 50
            y1 = self.extract_numbers(initial)[0] * 50
            x2 = x1 + 50
            y2 = y1 + 50
            canvas.create_rectangle(x1, y1, x2, y2, fill="red")

            # Set the goal state to  
            x1 = self.extract_numbers(goal)[1] * 50
            y1 = self.extract_numbers(goal)[0] * 50
            x2 = x1 + 50
            y2 = y1 + 50
            canvas.create_rectangle(x1, y1, x2, y2, fill="green")

    def change_color(self, canvas, robotEnviromint, row, col, color):
        x1 = col * 50
        y1 = row * 50
        x2 = x1 + 50
        y2 = y1 + 50
        canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def resetBoard(self, canvas):
        for i in range(len(self.robotEnviromint)):
            for y in range(len(self.robotEnviromint[i])):
                self.robotEnviromint[i][y] = 0

        canvas.delete("all")  # Clear the canvas
        for row in range(len(self.robotEnviromint)):
            for col in range(len(self.robotEnviromint[row])):
                if self.robotEnviromint[row][col] == 0:
                    color = "white"
                else:
                    color = "black"
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    