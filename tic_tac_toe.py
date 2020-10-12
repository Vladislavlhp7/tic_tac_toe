import numpy as np

class Turn:
		
	def __init__(self, id):
		self.id = id
		self.value = 0
		self.next = [None]*8

def deleteTurn(turn):
	if turn is not None:
		for i in range(8):
			deleteTurn(turn.next[i])
			turn.next[i] = None

#def insertTurns(turn):
    


def minimax(turn, depth):
    possibilities = []
    if depth == 0:
        return turn.id
    elif turn % 2 == 1:
        for node in turn.next:
            possibilities.append(minimax(node, depth-1))
        return max(possibilities)
    else:
        for node in turn.next:
            possibilities.append(minimax(node, depth-1))
        return min(possibilities)
        

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

def points(board, player):
	value = 10
	sum_rows = 0
	sum_cols = 0
	sum_diagonal = 0
	matrix = [[0 for i in range(3)] for j in range(3)]

	for i, tile in enumerate(board):
		temp = []
		if(tile == 'x'):
			matrix[int(i/3)][i%3] = 1
		elif(tile == 'o'):
			matrix[int(i/3)][i%3] = -1
	print(matrix)

	# Check if 3 same tiles are on the same row
	for row in matrix:
		sum_rows = sum(row)
		if(sum_rows == 3 or sum_rows == -3):
			if player == 1:
				return value
			else:
				return value*(-1)

	# Check if 3 same tiles are on the same col
	for j in range(3):
		sum_cols = 0
		for i in range(3):
			sum_cols += matrix[i][j]
		if(sum_cols == 3 or sum_cols == -3):
			if player == 1:
				return value
			else:
				return value*(-1)
	# Check if 3 same tiles are on the same diagonal
	sum_diagonal = matrix[0][0]+matrix[1][1]+matrix[2][2]
	if(sum_diagonal == 3 or sum_diagonal == -3):
		if player == 1:
			return value
		else:
			return value*(-1)
	# Check if 3 same tiles are on the same diagonal
	sum_diagonal = matrix[2][0]+matrix[1][1]+matrix[0][2]
	if(sum_diagonal == 3 or sum_diagonal == -3):
		value = 10
		if player == 1:
			return value
		else:
			return value*(-1)

# Some variables
board = ["-"]*9
num = -1
str_in = " "
_turn = 0
game_not_won = True

# The AI
turn = Turn(0)

print_board(board)

# Let it be that the standard player uses 'x'
# He is also represented with the boolean value of 1

# Start game
while(game_not_won):
	while(_turn == 0):
		try:
			num = int(input("Choose a tile [from 0 to 8]:"))
		except ValueError:
			print(str_in)
			while(len(str_in) > 1 or ord(str_in) < 48 or ord(str_in) > 57):
				str_in = input("Choose a valid tile [from 0 to 8]:")
			num = int(str_in)

		if num >= 0 and num <= 8:
			if tile_free(board, num):
				board[num] = 'x'
				_turn = 1
		print_board(board)
		print(points(board, 1))

	while(_turn == 1):
		_turn = 0
		break;
	# points(board_to_matrix(board), 1)
