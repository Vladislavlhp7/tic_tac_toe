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

board = ["-"]*9
print_board(board)