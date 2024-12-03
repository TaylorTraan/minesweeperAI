# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import queue
from collections import Counter

class MyAI(AI):

    def __init__(self, rows, cols, totalMines, startX, startY):
        self.rows = rows
        self.cols = cols
        self.totalMines = totalMines
        self.currentX = startX
        self.currentY = startY
        self.totalSafeCells = (rows * cols) - totalMines
        self.exploredCount = 0
        
        self.safeQueue = queue.Queue()
        self.visitedCells = []

        self.board = []
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                row.append(-100)
            self.board.append(row)

        self.sussyLevels = []  # -100 = unexplored
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                row.append(-100)
            self.sussyLevels.append(row)


    def isValid(self, x, y):
        return (0 <= x < self.rows) and (0 <= y < self.cols)
    

    def removeFromSafeQueue(self, x, y):
        """Remove a specific cell from the safe queue."""
        newQueue = queue.Queue()
        while not self.safeQueue.empty():
            item = self.safeQueue.get()
            if item != (x, y):
                newQueue.put(item)
        self.safeQueue = newQueue


    def handleZero(self, number):
        self.uncoverNeighborCells(self.currentX, self.currentY, number)

        for row in range(self.rows):
            for col in range(self.cols):
                if (self.sussyLevels[row][col] == 0 and (row, col) not in self.visitedCells and (row, col) not in self.safeQueue.queue):
                    self.safeQueue.put((row, col))
                    continue

                if self.board[row][col] == -100:
                    continue

                result = self.processEmptyCells(row, col)
                if result:
                    return result

                flaggedCount = len(self.findNeighborCells(row, col)[1])
                if self.board[row][col] == flaggedCount:
                    self.markSafeCells(row, col)

        if not self.safeQueue.empty():
            coordinate = self.safeQueue.get()
            return coordinate[0], coordinate[1], AI.Action.UNCOVER
        else:
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if self.isValid(row, col) and self.board[row][col] == -100:
                        return row, col, AI.Action.UNCOVER
            
            return 1, 1, AI.Action.LEAVE


    def markSafeCells(self, row, col):
        """Mark all neighbors of a cell as safe if they are unflagged."""
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i == row and j == col) or not self.isValid(i, j):
                    continue
                self.sussyLevels[i][j] = 0
                if (i, j) not in self.visitedCells and (i, j) not in self.safeQueue.queue:
                    self.safeQueue.put((i, j))

    def getAction(self, number: int) -> Action:
        if self.exploredCount == self.totalSafeCells:
            return Action(AI.Action.LEAVE, 1, 1)
        
        x, y = self.currentX, self.currentY
        self.board[x][y] = number
        self.sussyLevels[x][y] = 0
        
        self.currentX, self.currentY, actionType = self.handleZero(number)

        if actionType != AI.Action.FLAG:
            self.exploredCount += 1
        self.visitedCells.append((self.currentX, self.currentY))
        return Action(actionType, self.currentX, self.currentY)
    
    
    def uncoverNeighborCells(self, x, y, number):
        """Mark neighbors as safe if applicable."""
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i == x and j == y) or not self.isValid(i, j):
                    continue
                if (i, j) not in self.visitedCells and (i, j) not in self.safeQueue.queue:
                    if number == 0:
                        self.sussyLevels[i][j] = 0
                        self.safeQueue.put((i, j))
                    elif self.sussyLevels[i][j] != 0:
                        self.sussyLevels[i][j] = max(1, self.sussyLevels[i][j] + 1)
                        
    
    def processEmptyCells(self, row, col):
        """Handle empty cells around a given cell."""
        vacant, flagged = self.findNeighborCells(row, col)
        if vacant and len(vacant) == self.board[row][col] - len(flagged):
            vacantX, vacantY = vacant.pop(0)
            self.reduceProbabilityAround(row, col)
            self.removeFromSafeQueue(vacantX, vacantY)
            return vacantX, vacantY, AI.Action.FLAG
        return None
    
    
    def reduceProbabilityAround(self, row, col):
        """Reduce probability values of neighbors around a given cell."""
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i == row and j == col) or not self.isValid(i, j):
                    continue
                if self.sussyLevels[i][j] > 0:
                    self.sussyLevels[i][j] -= 1
    
    
    def findNeighborCells(self, row, col):
        """Identify vacant and flagged neighbors around a given cell."""
        vacant, flagged = [], []
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i == row and j == col) or not self.isValid(i, j):
                    continue
                if self.board[i][j] == -100:
                    vacant.append((i, j))
                elif self.board[i][j] == -1:
                    flagged.append((i, j))
        return vacant, flagged

	
 