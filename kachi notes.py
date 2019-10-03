#-------------------------------------------------------------------------------
# Name:        create df with pandas
# Purpose:
#
# Author:      fossp
#
# Created:     15/06/2019
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

    def __init__(currCell, isIsland, column, row,
    maxBridges=0, adjacentIslands = [], isBridge=False):

        if isIsland == True:
            currCell.isIsland = True
            currCell.maxBridges = maxBridges
            currCell.adjacentIslands = adjacentIslands
            currCell.isBridge = False
        else:
            currCell.isIsland = False
            currCell.maxBridges = maxBridges
            currCell.adjacentIslands = adjacentIslands

        currCell.isBridge = isBridge
        currCell.adjacentIslands = []
        currCell.connectedIslands = []
        currCell.column = column
        currCell.row = row

    def setIsland(this, maxBridges):
        this.maxBridges = maxBridges
        this.isIsland = True

    def currBridges(this):
        return len(this.connectedIslands)




    def connect(this, otherCell):

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
            this.connectedIslands.append(otherCell)
            print("Added a second connection.")
            return True

        # If they are adjacent, and in the same row...
        if otherCell.row == this.row:
            smallerColumn = min(this.column, otherCell.column)
            largerColumn = max(this.column, otherCell.column)

            # Now check nodes between them for obstacles
            for column in range(smallerColumn+1, largerColumn):
                currCell = gridColumns[column][this.row]
                print(str(currCell.column) + " " + str(currCell.row) )
                if (currCell.isIsland or currCell.isBridge):
                    print("we hit something. can't connect")
                    return False
                else:
                    currCell.isBridge = True

            otherCell.connectedIslands.append(this)
            this.connectedIslands.append(otherCell)
            print("Connect succesful")
            return True

    def disconnect(this, otherCell):

        if (this.connectedIslands.count(otherCell) < 1):
            print("They aren't even connected.")
            return False
        if (this.connectedIslands.count(otherCell) == 2):
            print("Disconnect success. 1 left.")
            this.connectedIslands.remove(otherCell)
            otherCell.connectedIslands.remove(this)
            return True
        else:
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
                        print("Is it a bridge? " + currCell.isBrdige)
                        print("Is it an island? " + currCell.isIsland)

            print("Disconnect success. 0 left.")
            this.connectedIslands.remove(otherCell)
            otherCell.connectedIslands.remove(this)
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







### Now let's populate the grid itself.

n = 4
gridColumns = []

for i in range(0, n):
    gridColumns.append([])
for i in range(0, n):
    for j in range(0, n):
        gridColumns[i].append(gridCell(False,
        column = i, row=j)
        )
gridColumns[3][0].isIsland = True
gridColumns[2][1].isIsland = True
gridColumns[1][0].isIsland = True











