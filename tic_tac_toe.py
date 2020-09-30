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

# Some variables
board = ["-"]*9
num = -1
str_in = " "
turn = 0
game_not_won = True

print_board(board)

# Start game
while(game_not_won):
	while(turn == 0):
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
				turn = 1
		print_board(board)
	while(turn == 1):
		break;