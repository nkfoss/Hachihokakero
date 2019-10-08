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

    def __init__ (this, isIsland, column, row,
    maxBridges=0, adjacentIslands = set(), isBridge=False):

        if isIsland == True:
            this.isIsland = True
            this.maxBridges = maxBridges
            this.adjacentIslands = adjacentIslands
            this.isBridge = False
            gridColumns[column][row] = this
        else:
            this.isIsland = False
            this.maxBridges = maxBridges
            this.adjacentIslands = adjacentIslands

        this.isBridge = isBridge
        this.adjacentIslands = set()
        this.connectedIslands = []
        this.column = column
        this.row = row

    def create(this, maxBridges):
        this.isIsland = True
        this.maxBridges = maxBridges

    def printCoords(this):
        print(str(this.column)+ " " + str(this.row))

    def printAdjacents(this):
        for island in this.adjacentIslands:
            island.printCoords()

    def setIsland(this, maxBridges):
        this.maxBridges = maxBridges
        this.isIsland = True

    def currBridges(this):
        return len(this.connectedIslands)

    def completeIsland(this):
        if this.currBridges() == this.maxBridges:
            return True
        else:
            return False

    def makeBridge():
        if isIsland == True:
            print("Can't create bridge. This is an island")
            return False
        if isBridge == True:
            print("This is already a bridge")
            return False
        else:
            isBridge = True




    def connect(this, otherCell):
    ######################################################################
    # Preliminary Checking

        # Make sure the subject is an island
        if (this.isIsland == False):
            print("Subject is not an island.")
            return False

        # Make sure target is an island
        if (otherCell.isIsland == False):
            print("Target is not an island.")
            return False

        # Make sure island doesn't connect to itself
        if (this == otherCell):
            print("Can't connect island to itself.")
            return False

        # Make sure we don't exceeed max connections
        if (this.connectedIslands.count(otherCell) >= 2):
            print("Can't connect again. Already have two connections.")
            return False

        # Make sure they are adjacent
        if otherCell.row != this.row and otherCell.column != this.column:
            print("ERROR: Node not adjacent")
            print( "Subject Row: " + str(this.row) + ". Column: " + str(this.column) )
            print( "Target  Row: " + str(otherCell.row) + ". Column: " + str(otherCell.column) )
            return False

        # If they're already connected once, go ahead do it again.
        if (this.connectedIslands.count(otherCell) == 1):

            otherCell.connectedIslands.append(this)
            otherCell.maxBridges = otherCell.maxBridges - 1
            this.connectedIslands.append(otherCell)
            this.maxBridges = this.maxBridges - 1

            print("Added a second connection.")
            return True


        #############################################################
        # Actual connecting...

        # All the nodes between will need to become bridges if the
        # connection is possible.
        toBeBridges = []

        # If they are adjacent by the same row...
        if otherCell.row == this.row:
            print("same row")
            smallerColumn = min(this.column, otherCell.column)
            largerColumn = max(this.column, otherCell.column)

            # Now check nodes between them for obstacles
            for column in range(smallerColumn+1, largerColumn):
                currCell = gridColumns[column][this.row]
                print(str(currCell.column) + " " + str(currCell.row) )
                if (currCell.isIsland or currCell.isBridge):
                    print("we hit something. can't connect")
                    print("currCell is bridge: " + str(currCell.isBridge))
                    print("currCell is island: " + str(currCell.isIsland))
                    return False
                else:
                    toBeBridges.append(currCell)

        # If they are adjacent by the same COLUMN...
        if otherCell.column == this.column:
            print("same column")
            smallerRow = min(this.row, otherCell.row)
            largerRow = max(this.row, otherCell.row)

            # Now check nodes between them for obstacles
            for row in range(smallerRow+1, largerRow):
                currCell = gridColumns[this.column][row]
                if (currCell.isIsland or currCell.isBridge):
                    print("we hit something. can't connect")
                    print("currCell is bridge: " + str(currCell.isBridge))
                    print("currCell is island: " + str(currCell.isIsland))
                    return False
                else:
                    toBeBridges.append(currCell)

        # If all went well, turn the between cells into bridges
        for cell in toBeBridges:
            cell.isBridge = True

        # Now add each island to the other's connect list.
        otherCell.connectedIslands.append(this)
        otherCell.maxBridges = otherCell.maxBridges - 1

        this.connectedIslands.append(otherCell)
        this.maxBridges = this.maxBridges - 1

        print("Connect succesful")
        return True



    def disconnect(this, otherCell):
    ########################################################################

        # They are not connected at all.
        if (this.connectedIslands.count(otherCell) < 1):
            print("They aren't even connected.")
            return False

        # They are connected once.
        if (this.connectedIslands.count(otherCell) == 2):
            print("Disconnect success. 1 left.")

            this.connectedIslands.remove(otherCell)
            this.maxBridges = this.maxBridges + 1

            otherCell.connectedIslands.remove(this)
            otherCell.maxBridges = otherCell.maxBridges + 1
            return True

        # They are connected twice.
        # This case requires turn cells from bridges back into empty.
        if (this.connectedIslands.count(otherCell) == 1):

            if otherCell.row == this.row:
                smallerColumn = min(this.column, otherCell.column)
                largerColumn = max(this.column, otherCell.column)
                 # Now check nodes between them for obstacles
                for column in range(smallerColumn+1, largerColumn):
                    currCell = gridColumns[column][this.row]
                    print(str(currCell.column) + " " + str(currCell.row) )
                    if (currCell.isBridge):
                        currCell.isBridge = False
                        print("dismantling bridge")
                    else:
                        print("There should be a bridge here...but there isn't")
                        print("Is it a bridge? " + currCell.isBridge)
                        print("Is it an island? " + currCell.isIsland)

            if otherCell.column == this.column:
                smallerRow = min(this.row, otherCell.row)
                largerRow = max(this.row, otherCell.row)
                # Now check nodes between them for obstacles
                for row in range(smallerRow+1, largerRow):
                    currCell = gridColumns[this.column][row]
                    print(str(currCell.column) + " " + str(currCell.row) )
                    if (currCell.isBridge):
                        currCell.isBridge = False
                        print("dismantling bridge")
                    else:
                        print("There should be a bridge here...but there isn't")
                        print("Is it a bridge? " + currCell.isBridge)
                        print("Is it an island? " + currCell.isIsland)

        print("Disconnect success. 0 left.")
        this.connectedIslands.remove(otherCell)
        this.maxBridges = this.maxBridges + 1

        otherCell.connectedIslands.remove(this)
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

    def getAdjacents(this):
        # Find adjacent islands in same column
        # Above
        for y in range(this.row-1, -1, -1):
            if gridColumns[this.column][y].isIsland:
                print("Found island above.")
                print( str(this.column) + " " + str(y))
                currIsland = gridColumns[this.column][y]
                this.adjacentIslands.add(currIsland)
                break
        # Below
        for y in range(this.row+1, n):
            if gridColumns[this.column][y].isIsland:
                print("Found island below.")
                print( str(this.column) + " " + str(y))
                currIsland = gridColumns[this.column][y]
                this.adjacentIslands.add(currIsland)
                break

        # Left
        for x in range(this.column-1, -1, -1):
            if gridColumns[x][this.row].isIsland:
                print("Found island to the left.")
                print( str(x) + " " + str(this.row))
                currIsland = gridColumns[x][this.row]
                this.adjacentIslands.add(currIsland)
                break
        # Right
        for x in range(this.column+1, n):
            if gridColumns[x][this.row].isIsland:
                print("Found island to the right.")
                print( str(x) + " " + str(this.row))
                currIsland = gridColumns[x][this.row]
                this.adjacentIslands.add(currIsland)
                break

islandList = set()


def printIslandList():
    for island in islandList:
        island.printCoords()

def populateIslandList():
    for column in gridColumns:
        for cell in column:
             if cell.isIsland:
                 islandList.add(cell)

def populateAdjacencyList():
    for island in islandList:
        island.getAdjacents()

def removeCompletedIslands():
    for island in islandList:
        for x in island.adjacentIslands.copy():
            if x.completeIsland():
                island.adjacentIslands.remove(x)

def setup():
    populateIslandList()
    populateAdjacencyList()
    removeCompletedIslands()

def checkSolved():
    for island in islandList:
        if len(island.adjacentIslands) > 0:
            return False
    return True

def findNextConnection():
    findLonelyIsland()

def findLonelyIslands():
    for island in islandList:
        if ( len(island.adjacentIslands) == 1):
            poppedIsland = island.adjacentIslands.pop()
            island.connect(poppedIsland)
            island.connect(poppedIsland)



### exec(open("kachi notes").read())

### Now let's populate the grid itself.

n=7

gridColumns = []

for i in range(0, n):
    gridColumns.append([])
for i in range(0, n):
    for j in range(0, n):
        gridColumns[i].append(gridCell(False,
        column = i, row=j)
        )

a = gridCell(True, 0, 0, 2)
a1 = gridCell(True, 0, 3, 4)
b = gridCell(True, 0, 6, 3)
c = gridCell(True, 2, 1, 2)
d = gridCell(True, 2, 3, 6)
e = gridCell(True, 2, 5, 1)
f = gridCell(True, 4, 0, 5)
g = gridCell(True, 4, 3, 5)
h = gridCell(True, 4, 5, 1)
i = gridCell(True, 6, 0, 4)
j = gridCell(True, 6, 2, 2)
k = gridCell(True, 6, 4, 1)
l = gridCell(True, 6, 6, 2)
