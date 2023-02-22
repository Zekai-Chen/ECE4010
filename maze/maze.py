import sys

class Node():
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action

# Please finish this stack function for DFS
class StackFrontier():

    def __init__(self):
        """
        define an empty frontier
        """
        self.frontier = []

    def add(self,node):
        """
        adds node  to the frontier
        """    
        self.frontier.append(node)
        #raise NotImplementedError

    def contains_state(self,state):
        """
        checks if the frontier contains a particular state
        """  
        return (any(node.state==state for node in self.frontier)) 
        #raise NotImplementedError

    def empty(self):
        """
        check whether the frontier is empty or not
        """  
        return (len(self.frontier)==0) 
        #raise NotImplementedError

    def remove(self):
        """
        remove node to the frontier based on stack structure
        """  
        if not self.empty():
            node=self.frontier[-1]
            self.frontier=self.frontier[:-1]
            #Last in First out
            return node  
        else:
            raise Exception("The Frontier Is Empty")
        #raise NotImplementedError


# Please finish this queue function for BFS
class QueueFrontier(StackFrontier):
    def remove(self):
        """
        remove node to the frontier based on queue structure
        """    
        if not self.empty():
            node=self.frontier[0]
            self.frontier=self.frontier[1:]
            #First in First out
            return node
        else:
            raise Exception("The Frontier Is Empty")
        #raise NotImplementedError

class Maze():
    def __init__(self,filename):

        # Read file and set height and width of maze 
        with open(filename) as f:
            contents = f.read()

        # validate start and goal
        if contents.count("A")!=1:
            raise Exception("maze must have exactly one start point")

        if contents.count("B")!=1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i,j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i,j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("▊", end="")
                elif (i,j) == self.start:
                    print("A", end="")
                elif (i,j) == self.goal:  
                    print("B", end="")
                elif solution is not None and (i ,j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self,state):
        row, col = state

        # All possible actions
        candidates = [
            ("up", (row -1, col)),
            ("down", (row+1, col)),
            ("left", (row, col -1)),
            ("right", (row, col +1))
        ]

        # Ensure action are valid 
        result = []
        for action, (r,c) in candidates:
            try:
                if not self.walls[r][c] and (r > -1) and (c > -1):
                    result.append((action, (r,c)))
            except IndexError:
                continue
        return result

    # plese finish the solve function that help the machine to figure out how to actually get from point A to point B
    def solve(self):
        """ Finds a solution to maze, if one exists, '"""

        # Record the number of explored states 
        self.Explored_Num = 0

        #Revised Approach in Slide1 
        #Start with a frontier that contains the initial state
        start = Node(state=self.start,parent=None,action=None)
        #Frontier = StackFrontier() 
        Frontier = QueueFrontier() 

        Frontier.add(start)
        self.Explored = set()

        """
        finish the rest of code based on the pseudocode we talked in the class 
        """    

        #Repeat
        while True:
            # If the frontier is empty, then no solution
            if Frontier.empty():
                sys.exit("No Solution Exist")     
                
            # Remove a node from the frontier according to BFS or DFS
            node = Frontier.remove()
            self.Explored_Num += 1

            # If node contains goal state, return the solution
            if node.state==self.goal:
                cells  = []
                actions= []
                while node.parent is not None:
                    cells.append(node.state)
                    actions.append(node.action)
                    node = node.parent
                cells.reverse()
                actions.reverse()
                self.solution=(actions,cells)
                return

            #Add the node to the explored set
            self.Explored.add(node.state)

            #Expand node
            for action,state in self.neighbors(node.state):
                #Adding resulting node to the frontier if
                #they are not already in the frontier or the explored set
                if (state not in self.Explored) and (not Frontier.contains_state(state)):
                    ChildNode = Node(state=state,parent=node,action=action)
                    Frontier.add(ChildNode)
        #raise NotImplementedError


    def output_image(self, filename, show_solution = True, show_explored= False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a black canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height *cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self. solution[1] if self.solution is not None else None

        print(self.Explored)

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40,40,40)

                # Start
                elif (i,j) == self.start:
                    fill = (255, 0 ,0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0,171,28)


                #Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220,235,113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.Explored:
                    fill = (212,97,85)
                
                # Empty cell
                else:
                    fill = (237, 240, 252)


                # Draw cell
                draw.rectangle(
                    ([ ( j*cell_size + cell_border,  i*cell_size + cell_border ),
                       ( (j+1)*cell_size - cell_border, (i+1)*cell_size - cell_border  ) ]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) !=2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.Explored_Num)
print("Solution:")
m.print()
#m.output_image("maze.png")
m.output_image("maze.png", show_explored = True)
    













        



            


