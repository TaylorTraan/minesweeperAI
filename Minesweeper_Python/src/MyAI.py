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
from collections import deque, Counter
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
		
		self.susTiles = Counter() #key = tile coordinate, value = how many times the sustile has been hit {increases probability}


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

	
	def markSus(self):
		pass


	def getAction(self, number: int) -> Action:

		#print(f'Exploring {self.currentTile}')
		self.explored.add(self.currentTile)
		self.unexplored.discard(self.currentTile)
  
		neighbors = self.getNeighbors(self.currentTile[0], self.currentTile[1])
		#print(f'Got current neighbors: {neighbors}')
  
		unflagged_neighbors = [n for n in neighbors if n not in self.flaggedTiles] #tbf getNeighbors already filters out flagged tiles, but this is another precaution
		#print(f"unflagged Neighbors: {unflagged_neighbors}")

		if number == len(unflagged_neighbors):
			for neighbor in unflagged_neighbors:
				if neighbor not in self.flaggedTiles:
					self.flaggedTiles.add(neighbor)
					self.unexplored.discard(neighbor)
			#print(f"adding these neighbors to flaggedTiles: {unflagged_neighbors}")
   

		if number > 0:
			for neighbor in neighbors:
				self.susTiles[neighbor] += 1
     
		if self.flaggedTiles:
			toFlag = self.flaggedTiles.pop()
			#print(f"flagging {toFlag}")
			return Action(AI.Action.FLAG, toFlag[0], toFlag[1])

		# Only flag tiles when there are no safe moves, and suspicion is strong enough
		if not self.safeTiles and len(self.flaggedTiles) < self.totalMines:
			highest_sus_tiles = sorted(
				self.susTiles.items(), key=lambda item: -item[1]
			)[:self.totalMines - len(self.flaggedTiles)]
			
			for tile, count in highest_sus_tiles:
				if tile not in self.flaggedTiles:
					self.flaggedTiles.add(tile)
					# return Action(AI.Action.FLAG, tile[0], tile[1])
		
		if number == 0:
			#get surrounding tiles and add to safeTiles; remove any tiles from sus tiles if in
			for neighbor in neighbors:
				if neighbor in self.susTiles:
					del self.susTiles[neighbor]
				if neighbor not in self.explored and neighbor not in self.safeTiles:
					self.safeTiles.append(neighbor) #(X, Y)
			#print(f"Adding these tiles to safeTiles: {neighbors}")

		for neighbor in neighbors:
			neighbor_neighbors = self.getNeighbors(neighbor[0], neighbor[1])
			unflagged_neighbors = [n for n in neighbor_neighbors if n not in self.flaggedTiles]
			if len(unflagged_neighbors) == 1 and number == 1:
				self.flaggedTiles.add(unflagged_neighbors[0])
				return Action(AI.Action.FLAG, unflagged_neighbors[0][0], unflagged_neighbors[0][1])


		#if there are tiles in safeTiles, then we can go through and uncover them
		if self.safeTiles:
			nextTile = self.safe_uncover()
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])

		#if not safe tiles in queue, pop a random unexplored tile
		if self.unexplored:
			nextTile = self.random_uncover()
			return Action(AI.Action.UNCOVER, nextTile[0], nextTile[1])
			
		#print("Leaving")
		return Action(AI.Action.LEAVE)


	def safe_uncover(self):
		nextTile = self.safeTiles.popleft()
		self.currentTile = nextTile
		#print(f"uncovering {nextTile}")
		return nextTile


	def random_uncover(self):
		# Convert unexplored tiles to a list
		unexplored_list = list(self.unexplored)
		random.shuffle(unexplored_list)  # Shuffle for randomness among equally suspicious tiles

		# Select the tile with the lowest suspicion count, using distance as a tiebreaker
		nextTile = min(
			unexplored_list,
			key=lambda t: (self.susTiles.get(t, 0), self.getDistance(self.currentTile, t))
		)

		# Remove the selected tile from unexplored and set it as current
		self.unexplored.remove(nextTile)
		self.currentTile = nextTile
		return nextTile
