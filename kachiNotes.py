from queue import PriorityQueue
import copy
# Maybe we can have gridColumns be a pointer to a boardstate, and then the functions won't
# all have to change to iterate over the nested lists in frontier[][]. 

# Some global variables
# --------------------------------------------------------------------- #
islandList = set()
frontier = []
maxConnections = 0
adjacentPairs = set()

step = 1

boardSize = 7

# The grid that we place all of our cells into
gridColumns = []


#-------------------------------------------------------------------------------
# Name:        Create algorithm to solve Hachihokakero
# Purpose:
#
# Author:      fossp
#
# Created:     30/09/2019
# Copyright:   (c) fossp 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

##### RANDOM NOTES

# The heuristic we are using the measure the 'fit' of a child node will be that
#

# Bridges left:
# Num of adjacent nodes: int (priority #1)
# Curr num of bridges: int
#

# There is also

# Logically, finding a node with the least number of nodes first, is important.
# Coords : required bridges, num adjacent nodes.

# set 'n' rows/columns for a squre grid....(tbc)

####################################
class gridCell:

    # Optional parameters come last. There are three general states that a gridCell
    # can have: island, bridge, or neither. Islands can be connected to and have
    # other important attribites. bridges simply serve as a state of connection
    # between two gridCells and block other connections from crossing. If a grid
    # cell is NEITHER, than it can possibly become a bridge.

    def __init__ (self, isIsland, column, row,
    maxBridges=0, adjacentIslands = set(), isBridge=False, board=gridColumns):

        if isIsland == True:
            self.isIsland = True
            self.maxBridges = maxBridges
            self.initialMB = maxBridges
            self.adjacentIslands = adjacentIslands
            self.isBridge = False
            board[column][row] = self
        else:
            self.isIsland = False
            self.maxBridges = maxBridges
            self.adjacentIslands = adjacentIslands

        self.isBridge = isBridge
        self.adjacentIslands = set()
        self.connectedIslands = []
        self.column = column
        self.row = row

    def create(self, maxBridges):
        self.isIsland = True
        self.maxBridges = maxBridges

    def printCoords(self):
        return(str(self.column)+ " " + str(self.row))

    def printAdjacents(self):
        for island in self.adjacentIslands:
            island.printCoords()

    def setIsland(self, maxBridges):
        self.maxBridges = maxBridges
        self.isIsland = True

    def currBridges(self):
        return len(self.connectedIslands)

    def isCompleteIsland(self):
        if self.maxBridges == 0:
            return True
        else:
            return False

    def makeBridge(self):
        if self.isIsland == True:
            print("Can't create bridge. This is an island")
            return False
        if self.isBridge == True:
            print("This is already a bridge")
            return False
        else:
            self.isBridge = True

    def connect(self, otherCell, board):
    ######################################################################
    # Preliminary Checking

        # Make sure the subject is an island
        if (self.isIsland == False):
            print("Subject is not an island.")
            return False

        # Make sure target is an island
        if (otherCell.isIsland == False):
            print("Target is not an island.")
            return False

        # Make sure island doesn't connect to itself
        if (self == otherCell):
            print("Can't connect island to itself.")
            return False

        # Make sure we don't exceeed max connections
        if (self.connectedIslands.count(otherCell) > 1):
            print("Can't connect again. Already have two connections.")
            self.printCoords()
            otherCell.printCoords()
            return False

        # Make sure the island isn't full
        if self.maxBridges <= 0:
            return False

        # Make sure they are adjacent
        if otherCell.row != self.row and otherCell.column != self.column:
            print("ERROR: Node not adjacent")
            print( "Subject Row: " + str(self.row) + ". Column: " + str(self.column) )
            print( "Target  Row: " + str(otherCell.row) + ". Column: " + str(otherCell.column) )
            return False

        # If they're already connected once, go ahead do it again.
        if (self.connectedIslands.count(otherCell) == 1 and otherCell.maxBridges > 0):

            otherCell.connectedIslands.append(self)
            otherCell.maxBridges = otherCell.maxBridges - 1
            self.connectedIslands.append(otherCell)
            self.maxBridges = self.maxBridges - 1

            print("Added a second connection.")
            return True


        #############################################################
        # Actual connecting...

        # All the nodes between will need to become bridges if the
        # connection is possible.
        toBeBridges = []

        # If they are adjacent by the same row...
        if otherCell.row == self.row:
            print(" --- same row --- ")
            smallerColumn = min(self.column, otherCell.column)
            largerColumn = max(self.column, otherCell.column)

            # Now check nodes between them for obstacles
            for column in range(smallerColumn+1, largerColumn):
                currCell = board[column][self.row]
                # print(str(currCell.column) + " " + str(currCell.row) )
                if (currCell.isIsland or currCell.isBridge):
                    print("we hit something. can't connect")
                    print(currCell.column, currCell.row)
                    print("currCell is bridge: " + str(currCell.isBridge))
                    print("currCell is island: " + str(currCell.isIsland))
                    return False
                else:
                    toBeBridges.append(currCell)

        # If they are adjacent by the same COLUMN...
        if otherCell.column == self.column:
            print(" --- same column --- ")
            smallerRow = min(self.row, otherCell.row)
            largerRow = max(self.row, otherCell.row)

            # Now check nodes between them for obstacles
            for row in range(smallerRow+1, largerRow):
                currCell = board[self.column][row]
                if (currCell.isIsland or currCell.isBridge):
                    print("we hit something. can't connect")
                    print(currCell.column, currCell.row)
                    print("currCell is bridge: " + str(currCell.isBridge))
                    print("currCell is island: " + str(currCell.isIsland))
                    return False
                else:
                    toBeBridges.append(currCell)

        # If all went well, turn the between cells into bridges
        for cell in toBeBridges:
            cell.isBridge = True

        # Now add each island to the other's connect list.
        if otherCell.maxBridges > 0:
            otherCell.connectedIslands.append(self)
            otherCell.maxBridges = otherCell.maxBridges - 1

            self.connectedIslands.append(otherCell)
            self.maxBridges = self.maxBridges - 1

            print("Connect succesful")
            return True



    def disconnect(self, otherCell, board):
    ########################################################################

        # They are not connected at all.
        if (self.connectedIslands.count(otherCell) < 1):
            print("They aren't even connected.")
            return False

        # They are connected once.
        if (self.connectedIslands.count(otherCell) == 2):
            print("Disconnect success. 1 left.")

            self.connectedIslands.remove(otherCell)
            self.maxBridges = self.maxBridges + 1

            otherCell.connectedIslands.remove(self)
            otherCell.maxBridges = otherCell.maxBridges + 1
            return True

        # They are connected twice.
        # self case requires turn cells from bridges back into empty.
        if (self.connectedIslands.count(otherCell) == 1):

            if otherCell.row == self.row:
                smallerColumn = min(self.column, otherCell.column)
                largerColumn = max(self.column, otherCell.column)
                 # Now check nodes between them for obstacles
                for column in range(smallerColumn+1, largerColumn):
                    currCell = board[column][self.row]
                    print(str(currCell.column) + " " + str(currCell.row) )
                    if (currCell.isBridge):
                        currCell.isBridge = False
                        print("dismantling bridge")
                    else:
                        print("There should be a bridge here...but there isn't")
                        print("Is it a bridge? " + currCell.isBridge)
                        print("Is it an island? " + currCell.isIsland)

            if otherCell.column == self.column:
                smallerRow = min(self.row, otherCell.row)
                largerRow = max(self.row, otherCell.row)
                # Now check nodes between them for obstacles
                for row in range(smallerRow+1, largerRow):
                    currCell = board[self.column][row]
                    print(str(currCell.column) + " " + str(currCell.row) )
                    if (currCell.isBridge):
                        currCell.isBridge = False
                        print("dismantling bridge")
                    else:
                        print("There should be a bridge here...but there isn't")
                        print("Is it a bridge? " + currCell.isBridge)
                        print("Is it an island? " + currCell.isIsland)

        print("Disconnect success. 0 left.")
        self.connectedIslands.remove(otherCell)
        self.maxBridges = self.maxBridges + 1

        otherCell.connectedIslands.remove(self)
        otherCell.maxBridges = otherCell.maxBridges + 1
        return True

    def makeBridge():
        if isIsland == True:
            print("Can't create bridge. This is an island")
            return False
        if isBridge == True:
            print("This is already a bridge")
            return False
        else:
            isBridge = True

    def getAdjacents(self, board):
        # Find adjacent islands in same column
        # Above
        for y in range(self.row-1, -1, -1):
            if (board[self.column][y].isIsland and (board[self.column][y].maxBridges > 0)):
                print("Found island above.")
                print( str(self.column) + " " + str(y))
                currIsland = board[self.column][y]
                print(currIsland.maxBridges)
                self.adjacentIslands.add(currIsland)
                break
        # Below
        for y in range(self.row+1, boardSize):
            if (board[self.column][y].isIsland and (board[self.column][y].maxBridges > 0)):
                print("Found island below.")
                print( str(self.column) + " " + str(y))
                currIsland = board[self.column][y]
                self.adjacentIslands.add(currIsland)
                break

        # Left
        for x in range(self.column-1, -1, -1):
            if (board[x][self.row].isIsland and (board[x][self.row].maxBridges > 0)):
                print("Found island to the left.")
                print( str(x) + " " + str(self.row))
                currIsland = board[x][self.row]
                self.adjacentIslands.add(currIsland)
                break
        # Right
        for x in range(self.column+1, boardSize):
            if (board[x][self.row].isIsland and (board[x][self.row].maxBridges > 0)):
                print("Found island to the right.")
                print( str(x) + " " + str(self.row))
                currIsland = board[x][self.row]
                self.adjacentIslands.add(currIsland)
                break

### Now let's populate the grid itself.
def populateGrid():
    global a
    global b
    global c
    global d
    global e
    global f
    global g
    global h
    global i
    global j
    global k
    global l
    global m
    gridColumns.clear()
    for i in range(0, boardSize):
        gridColumns.append([])
    for i in range(0, boardSize):
        for j in range(0, boardSize):
            gridColumns[i].append(gridCell(False,
            column = i, row=j)
            )
    a = gridCell(True, 0, 0, 2)
    b = gridCell(True, 0, 3, 4)
    c = gridCell(True, 0, 6, 3)
    d = gridCell(True, 2, 1, 2)
    e = gridCell(True, 2, 3, 6)
    f = gridCell(True, 2, 5, 1)
    g = gridCell(True, 4, 0, 5)
    h = gridCell(True, 4, 3, 5)
    i = gridCell(True, 4, 5, 1)
    j = gridCell(True, 6, 0, 4)
    k = gridCell(True, 6, 2, 2)
    l = gridCell(True, 6, 4, 1)
    m = gridCell(True, 6, 6, 2)

populateGrid()
# Test Puzzle
# a = gridCell(True, 0, 0, 2)
# b = gridCell(True, 0, 2, 4)
# c = gridCell(True, 0, 4, 4)
# d = gridCell(True, 0, 6, 2)

# This is our puzzle
# --------------------------------------------------------------------- #
a = gridCell(True, 0, 0, 2)
b = gridCell(True, 0, 3, 4)
c = gridCell(True, 0, 6, 3)
d = gridCell(True, 2, 1, 2)
e = gridCell(True, 2, 3, 6)
f = gridCell(True, 2, 5, 1)
g = gridCell(True, 4, 0, 5)
h = gridCell(True, 4, 3, 5)
i = gridCell(True, 4, 5, 1)
j = gridCell(True, 6, 0, 4)
k = gridCell(True, 6, 2, 2)
l = gridCell(True, 6, 4, 1)
m = gridCell(True, 6, 6, 2)
# --------------------------------------------------------------------- #

def printMaxBridges():
    maxBList = []
    total = 0
    for island in islandList:
        x = island.printCoords()
        y = island.maxBridges
        maxBList.append([x, y])
        total = total + y
        # print(island.printCoords() + ": ")
        # print(island.maxBridges)
    print(total)
    print(maxBList)

def printIslandList():
    for island in islandList:
        island.printCoords()

def populateIslandList(board):
    global islandList
    islandList.clear()
    for column in board:
        for cell in column:
             if cell.isIsland:
                 islandList.add(cell)

def populateAdjacencyList(board):
    for island in islandList:
        island.adjacentIslands.clear()
        if island.maxBridges > 0:
            island.getAdjacents(board)

# Removes completed islands from the adjacency lists of other islands.
def removeCompletedIslands():
    for island in islandList:
        if island.isCompleteIsland():
            island.adjacentIslands.clear()
        else:
            for x in island.adjacentIslands.copy():
                if x.isCompleteIsland():
                    island.adjacentIslands.remove(x)

def checkSolved(board):
    populateIslandList(board)
    counter = 0
    for island in islandList:
        counter += island.maxBridges
    # print(counter)
    return(counter == 0)

def checkIllegalMove(island, board):
    boardCopy = copy.deepcopy(board)
    islandInBoard = board[island.column][island.row]
    CIL = islandInBoard.connectedIslands
    for x in CIL:
        if x.isCompleteIsland():
            CIL.remove(x)
            x.connectedIslands.remove(islandInBoard)
            return(checkIllegalMove(x, board))
        else:
            return False
    return True

def calculateMaxConnections():
    global maxConnections
    for island in islandList:
        maxConnections += island.maxBridges

# The frontier needs to be sorted twice
def sortFrontier():
    global frontier
    frontier = sorted(frontier, key=lambda tup: tup[1])
    # frontier = sorted(frontier, key=lambda tup: tup[1[0]])

# Iterate over all of the islands and add pairs to the adjacentPairs set in order to 
# make connections based on pairs of islands and not on individual islands.
# Putting them in a set makes sure that no pair of islands exists twice
def populatePairs(board):
    adjacentPairs.clear()
    populateAdjacencyList(board)
    for island in islandList:
        copy = island.adjacentIslands.copy()
        while (len(copy) > 0):
            a = set()
            popped = copy.pop()
            # print("Found pair:")
            # island.printCoords()
            # popped.printCoords()
            a.add(island)
            a.add(popped)
            b = frozenset(a)
            adjacentPairs.add(b)



# Calculate the "value" of each available move in the board.
def calculateHeuristic(board):
    print("Calculating Heuristic:")
    scores = []
    print("Populating islandList:")
    populateIslandList(board)
    print("Populating pairs:")
    populatePairs(board)
    print("Creating scores:")
    for pair in adjacentPairs:
        # print(pair)
        heuristic = 0
        for island in pair:
            if len(island.adjacentIslands) > 0:
                numAdj = len(island.adjacentIslands)
                weight = island.maxBridges
                heuristic =+ numAdj + weight
        scores.append([pair, heuristic])
    # This sorts the scores[[a, b]] by their b, much in the way a priority queue would
    return sorted(scores, key=lambda tup: tup[1])

maxH = 0
# Make a copy of the board at a given state and save it in frontier
def makeChildren(scores, board, prevHeuristic):
    global maxH
    print("Making Children:")
    # Make a copy of the board 
    x = copy.deepcopy(board)
    if len(frontier) > 0:
        frontier.pop(0)
    while (len(scores) > 0):
        y = scores.pop(0)
        z = list(y[0])
        a = z[0]
        b = z[1]
        for i in range(0, boardSize):
            for j in range(0, boardSize):
                # Each node at (i, j) is equal to a, b, or neither. By the time each row and column has been iterated over,
                # a and b should be stored as the frontier.
                if ((x[i][j].column == a.column) & (x[i][j].row ==  a.row)):
                    copyA = x[i][j]
                if ((x[i][j].column == b.column) & (x[i][j].row ==  b.row)):
                    copyB = x[i][j]
        # print("A: ", copyA)
        # print("A column: ", copyA.column, "\n", "A row: ", copyA.row)
        # print("B ", copyB)
        # print("B column: ", copyB.column, "\n", "B row: ", copyB.row)
        # The nodes can then be connected and the copy can be stored finally
        copyA.connect(copyB, x)
        # Illegal moves don't get added to the frontier
        if checkIllegalMove(copyA, board):
            newBoard = copy.deepcopy(x)
            # print("Previous Heuristic: ", prevHeuristic)
            # print("Added Heuristic: ", y[1])
            if prevHeuristic[1] > maxH:
                maxH = prevHeuristic[1]
            newHeuristic = prevHeuristic[1] + y[1]
            # print("New Heuristic: ", newHeuristic)
            frontier.append([newBoard, [-step, newHeuristic]])
    sortFrontier()

# Populate frontier[][] and place board states into the priority queue.
def initializeFrontier():
    print("Initializing the frontier:")
    makeChildren(calculateHeuristic(gridColumns), gridColumns, [0,0])


def nearlySolve():
    frontier[0][0][0][0].connect(frontier[0][0][0][3], frontier[0][0])
    frontier[0][0][0][6].connect(frontier[0][0][0][3], frontier[0][0])
    frontier[0][0][0][6].connect(frontier[0][0][0][3], frontier[0][0])
    frontier[0][0][0][6].connect(frontier[0][0][6][6], frontier[0][0])
    frontier[0][0][6][4].connect(frontier[0][0][6][6], frontier[0][0])
    frontier[0][0][0][0].connect(frontier[0][0][4][0], frontier[0][0])
    frontier[0][0][6][0].connect(frontier[0][0][4][0], frontier[0][0])
    frontier[0][0][6][0].connect(frontier[0][0][4][0], frontier[0][0])
    frontier[0][0][6][0].connect(frontier[0][0][6][2], frontier[0][0])
    frontier[0][0][6][0].connect(frontier[0][0][6][2], frontier[0][0])
    populateIslandList(frontier[0][0])

# This function conducts the search, like the "grid search" example.
def search(runs):
    global step
    for i in range(runs):
        if checkSolved(frontier[0][0]):
            print("Solved!!")
            break    
        makeChildren(calculateHeuristic(frontier[0][0]), frontier[0][0], frontier[0][1])
        i = i + 1
        step = step + 1
        print("This was run #",i)
        print(maxH)

# Finds all of the guaranteed connections in the board. This should probably return a boardstate and a small 
# value for a heuristic, but right now it just connects islands in gridColumns.
# def findGuaranteedConnections():
#     for island in islandList:
#         if ((len(island.adjacentIslands) > 0) and (len(island.adjacentIslands) == 1 or len(island.adjacentIslands) == island.maxBridges/2)):
#             print("-------------------------------------------------")
#             print("         Attempting to Connect Islands         ")
#             print("Island Found: ")
#             island.printCoords()
#             print("Connecting Islands.")
#             while (len(island.adjacentIslands) > 0):
#                 poppedIsland = island.adjacentIslands.pop()
#                 print("Popped Island:")
#                 poppedIsland.printCoords()
#                 island.connect(poppedIsland)
#                 island.connect(poppedIsland)
#                 print("Connected Islands. \n")

# The beginning of our heuristic function?
def findNextConnection():
    # Find solo islands
    # findGuaranteedConnections()
    removeCompletedIslands()

def setup():
    global step
    step = 0
    frontier.clear()
    populateGrid()
    populateIslandList(gridColumns)
    populateAdjacencyList(gridColumns)
    populatePairs(gridColumns)
    calculateMaxConnections()
    initializeFrontier()

def main():
    setup()
    if __name__== "__main__" :
        main()