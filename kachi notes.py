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
            currCell.column = column
            currCell.row = row
            currCell.isBridge = False
        else:
            currCell.isIsland = False
            currCell.maxBridges = maxBridges
            currCell.adjacentIslands = adjacentIslands

        currCell.isBridge = isBridge
        adjacentIsland = []
        currBridges = 0

    def connect(otherCell):
        if otherCell.row != row or otherCell.column != column:
            print("ERROR: Node not adjacent")
            print( "Row: " + row + ". Column: " + column)
            return False


### Now let's populate the grid itself.

n = 4
gridColumns = []

for i in range(0, 7):
    gridColumns.append([])
for i in range(0, 7):
    for j in range(0, 7):
        gridColumns[i].append(gridCell(False,
        column = gridColumns[i], row=j)
        )











