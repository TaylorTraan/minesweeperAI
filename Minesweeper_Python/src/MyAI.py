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

	def getDistance(self, tile1, tile2):
		return abs(tile1[0] - tile2[0]) + abs(tile1[1] - tile2[1])

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

		print(f'Exploring {self.currentTile}')
		self.explored.add(self.currentTile)
		self.unexplored.discard(self.currentTile)
  
		neighbors = self.getNeighbors(self.currentTile[0], self.currentTile[1])
		print(f'Got current neighbors: {neighbors}')
  
		unflagged_neighbors = [n for n in neighbors if n not in self.flaggedTiles]
		print(f"unflagged Neighbors: {unflagged_neighbors}")
		if number == len(unflagged_neighbors):
			for neighbor in unflagged_neighbors:
				self.flaggedTiles.add(neighbor)
			print(f"adding these neighbors to flaggedTiles: {unflagged_neighbors}")
     
		if self.flaggedTiles:
			toFlag = self.flaggedTiles.pop()
			print(f"flagging {toFlag}")
			return Action(AI.Action.FLAG, toFlag[0], toFlag[1])
		
		if number == 0:
			#get surrounding tiles and add to safeTiles
			for neighbor in neighbors:
				if neighbor not in self.explored and neighbor not in self.safeTiles:
					self.safeTiles.append(neighbor) #(X, Y)
			print(f"Adding these tiles to safeTiles: {neighbors}")

		#if there are tiles in safeTiles, then we can go through and uncover them
		if self.safeTiles:
			nextTile = self.safeTiles.popleft()
			self.currentTile = nextTile
			print(f"uncovering {nextTile}")
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])


		#if not safe tiles in queue, pop a random unexplored tile
		if self.unexplored:
			unexplored_list = list(self.unexplored)
			random.shuffle(unexplored_list)
			nextTile = min(unexplored_list, key=lambda t: self.getDistance(self.currentTile, t))
			self.unexplored.remove(nextTile)
			self.currentTile = nextTile
			print(f"uncovering random tile {nextTile}")
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])
			
		print("Leaving")
		return Action(AI.Action.LEAVE)