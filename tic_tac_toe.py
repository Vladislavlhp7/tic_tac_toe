import numpy as np
from operator import itemgetter

class TurnNode:
	def __init__(self):
		self.next = [None]*9
		self.value = 0
		self.isEnd = False

	def is_it_End(self):
		return self.isEnd

	def getValue(self):
		return self.value		

# Turn will implement Trie data structure
class Turn:

	def __init__(self):
		self.root = self.getNode()

	def getRoot(self):
		return self.root

	def getNode(self):
		return TurnNode()

	# The value of each combination will be computed as well as the insertion functionality
	def insert(self, turns):
		iterator = self.root
		value, index, turns = evaluate_turn(turns)
		for turn in turns:
			if not iterator.next[turn]:
				iterator.next[turn] = self.getNode()
			iterator = iterator.next[turn]
		iterator.isEnd = True
		iterator.value = value

	def search(self, turns):
		iterator = self.root
		for turn in turns:
			if iterator.next[turn] == None:
				return False
			iterator = iterator.next[turn]
		
		return iterator != None and iterator.isEnd

def evaluate_turn(turns):
	value = 0
	min_num = 5 				# A winner is selected upon at least 5 numbers of turns and max 9
	for num in range(min_num, 9):
		value = points(list_to_board(turns[:num+1]))
		if(value != 0):
			return value, num, turns[:num+1]
	return value, num, turns 	# No better move than a one leading to equal


def minimax_val(node, player):
	possibilities = []
	if node.is_it_End():
		return node.getValue()
	elif player == 1:
		for _node in node.next:
			if(_node):
				possibilities.append(minimax_val(_node, 0))
		return max(possibilities)
	else:
		for _node in node.next:
			if(_node):
				possibilities.append(minimax_val(_node, 1))
		return min(possibilities)
		

def ai_choose(history, turn):
	possibilities = []
	decision = []
	node = turn.getRoot() 			# Root is empty
	for x in range(0,len(history)):	# Move until last history entry is reached
		if(node):	
			node = node.next[history[x]]
	if len(history) % 2 == 1:
		for x, _node in enumerate((node.next)):
			if(_node):
				possibilities.append([minimax_val(_node, 1)] + [x])
				# print("Possibilities:", possibilities)
	decision = max(possibilities, key=itemgetter(0))
	# print(decision)
	return decision[1]


def print_board(board):
	line = 0
	for elem in board:
		print(elem, end="")
		if line == 2:
			line = -1
			print()
		else:
			print('|', end="")
		line += 1

def tile_free(board, num):
	if board[num] == '-':
		return True
	return False

def permutations(arr, start, end, num, outcomes):	
	if(start == end):
		outcomes.append([num] + arr) 	# num holds the first move
		return
	for i in range(start, end+1):
		arr[i], arr[start] = arr[start], arr[i]
		permutations(arr, start+1, end, num, outcomes)
		arr[i], arr[start] = arr[start], arr[i]

def list_to_board(arr):
	board = ["-"]*9
	for index, cell in enumerate(arr):
		if(index%2): 		# AI first
			board[cell] = 'o' 
		else:
			board[cell] = 'x'
	return board

# AI points are positive, whereas human player ones are negative
# This is important for the selection of the optimal move
def points(board):
	value = 10
	sum_rows = 0
	sum_cols = 0
	sum_diagonal = 0
	matrix = [[0 for i in range(3)] for j in range(3)]

	for i, tile in enumerate(board):
		if(tile == 'o'):
			matrix[int(i/3)][i%3] = 1
		elif(tile == 'x'):
			matrix[int(i/3)][i%3] = -1

	# Check if 3 same tiles are on the same row
	for row in matrix:
		sum_rows = sum(row)
		if(sum_rows == 3):
			return value
		if(sum_rows == -3):
			return value*(-1)

	# Check if 3 same tiles are on the same col
	for j in range(3):
		sum_cols = 0
		for i in range(3):
			sum_cols += matrix[i][j]
		if(sum_cols == 3):
			return value
		if(sum_cols == -3):
			return value*(-1)

	# Check if 3 same tiles are on the same diagonal
	sum_diagonal = matrix[0][0]+matrix[1][1]+matrix[2][2]
	if(sum_diagonal == 3 or sum_diagonal == -3):
		if(sum_diagonal == 3):
			return value
		if(sum_diagonal == -3):
			return value*(-1)

	# Check if 3 same tiles are on the same diagonal
	sum_diagonal = matrix[2][0]+matrix[1][1]+matrix[0][2]
	if(sum_diagonal == 3 or sum_diagonal == -3):
		if(sum_diagonal == 3):
			return value
		if(sum_diagonal == -3):
			return value*(-1)

	# Equal for both players
	return 0


board = ["-"]*9	# Create board
num = -1		# num will hold each move we input
str_in = " "	# Variable for validation
_turn = 0		# To keep player or ai turn
start_ai = True # After first turn update trie with permutations
outcomes = []	# List to hold all permutations
history = [] 	# To hold all played turns
game_not_won = True

# Let it be that the standard player uses 'x'

# Start game
while(game_not_won):
	print_board(board)
	# Human player starts first
	while(_turn == 0):
		# Validate input
		try:
			num = int(input("Choose a tile [from 0 to 8]:"))
		except ValueError:
			print(str_in)
			while(len(str_in) > 1 or ord(str_in) < 48 or ord(str_in) > 57):
				str_in = input("Choose a valid tile [from 0 to 8]:")
			num = int(str_in)
		# Input is valid
		if num >= 0 and num <= 8:
			if tile_free(board, num):
				board[num] = 'x' 		# Update board
				history.append(num)		# Add move to 'played moves'
				_turn = 1				# Enable AI move
				if(start_ai): 			# If it is first turn only, permute, update trie ds
					# The AI
					turn = Turn()
					# Since move one has been played, there are 7 more moves to be permuted
					permutations([x for x in range(0, 8+1) if x != num], 0, 7, num ,outcomes)
					for outcome in outcomes:
						turn.insert(outcome)
					start_ai = False	# Disable re-intiation of AI knowledge base
				if(points(board)!=0 or len(history)==9):
					game_not_won = False
					_turn = 0 				# Disable AI move
					break

	if(_turn == 1):
		history.append(ai_choose(history, turn))
		board[history[len(history)-1]] = 'o'
		_turn = 0
		if(points(board)!=0 or len(history)==9):
			game_not_won = False
