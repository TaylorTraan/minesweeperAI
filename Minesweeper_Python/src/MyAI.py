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
from collections import deque
import random


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines
		self.startX, self.startY = startX, startY
  
		self.currentTile = (startX, startY)
  
		self.safeTiles = deque()
		self.flaggedTiles = set()
		self.explored = set()
		self.unexplored = {(i, j) for i in range(rowDimension) for j in range(colDimension)}
		self.unexplored.remove((startX, startY))


	def getNeighbors(self, x, y):
     
		neighbors = []
		for i in [-1, 0, 1]:
			for j in [-1, 0, 1]:
				if i == 0 and j == 0:
					continue
				neighbor = (x+i, y+j)
				if  (0 <= neighbor[0] < self.rowDimension and 
    				0 <= neighbor[1] < self.colDimension and 
        			neighbor not in self.explored and 
           			neighbor not in self.flaggedTiles):
					neighbors.append(neighbor)
		return neighbors

				

	def getAction(self, number: int) -> Action:

		self.explored.add(self.currentTile)
		self.unexplored.discard(self.currentTile)
  
		neighbors = self.getNeighbors(self.currentTile[0], self.currentTile[1])
  
		if number > 0:
			if number == len(neighbors):
				for neighbor in neighbors:
					self.flaggedTiles.add(neighbor)
     
		if self.flaggedTiles:
			toFlag = self.flaggedTiles.pop()
			return Action(AI.Action.FLAG, toFlag[0], toFlag[1])
		
		if number == 0:
			#get surrounding tiles and add to safeTiles
			for neighbor in neighbors:
				if neighbor not in self.explored and neighbor not in self.safeTiles:
					self.safeTiles.append(neighbor) #(X, Y)

		#if there are tiles in safeTiles, then we can go through and uncover them
		if self.safeTiles:
			nextTile = self.safeTiles.popleft()
			self.currentTile = nextTile
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])


		#if not safe tiles in queue, pop a random unexplored tile
		if self.unexplored:
			nextTile = min(self.unexplored, key=lambda t: self.getDistance(self.currentTile, t))
			self.unexplored.remove(nextTile)
			self.currentTile = nextTile
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])
			
  
		if not self.safeTiles and not self.flaggedTiles and not self.unexplored:
			return Action(AI.Action.LEAVE)
		
