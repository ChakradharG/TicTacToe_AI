from numpy import prod


def dispBoard():
	"""Displaying the board"""
	for i in range(3):
		for j in range(3):
			print(bDict[board[i][j]], end=' ')
		print('\n')
	print()


def available():
	"""Checking if there is space on the board"""
	x = prod(board)
	return not x


def playerUpdate():
	"""Updating the board according to the player's input"""
	while True:
		try:
			x = int(input('Your Move: '))
			assert x in list(range(1,10))
		except:
			print('Enter a number between 1 and 9\n')
		else:
			i = (x - 1) // 3
			j = (x - 1) % 3
			if board[i][j] == 0:
				board[i][j] = -1
				break
			else:
				print('Illegal move! Please try again\n')


def over(b):
	"""Checking if the game is over by win or not"""
	#Checking rows
	for i in b:
		x = sum(i)
		if abs(x) == 3:
			return x//3

	#Checking columns
	for i in range(3):
		x = 0
		for j in range(3):
			x += b[j][i]
		if abs(x) == 3:
			return x//3

	#Checking diagonals
	x, y = 0, 0
	for i in range(3):
		x += b[i][i]	#Diagonal 1
		y += b[i][2-i]	#Diagonal 2
	if abs(x) == 3:
		return x//3
	if abs(y) == 3:
		return y//3

	#No winner (yet)
	return 0


def getKey(b):
	"""Representing the board as a string for hashing"""
	k = ''
	for i in b:
		for j in i:
			k += str(j)
	return k


def evaluate(tBoard, t):
	"""Implementing the Minimax algorithm"""
	try:
		return util[getKey(tBoard)]

	except:
		y = over(tBoard)
		if y:
			return y

		if not available():
			return 0

		moves = {}
		for i in range(3):
			for j in range(3):
				if tBoard[i][j] == 0:
					tBoard[i][j] = t
					x = evaluate(tBoard, -t)
					key = getKey(tBoard)
					util[key] = x
					moves[i, j] = x
					tBoard[i][j] = 0	
		
		value = max(moves.values()) if t == 1 else min(moves.values())
		return value


def aiUpdate():
	"""Finding the optimal move"""
	tBoard = board[:]
	moves = {}
	for i in range(3):
		for j in range(3):
			if tBoard[i][j] == 0:
				tBoard[i][j] = 1
				moves[evaluate(tBoard, -1)] = i, j
				tBoard[i][j] = 0
	
	i, j = moves[max(moves.keys())]
	board[i][j] = 1
	if __name__ == '__main__':
		print('CPU\'s Move:', (3*i) + j+1)


def main():
	"""Handles the flow of the game"""
	print('Hello & Welcome to TicTacToe')
	ch = input('Do you want to play first? (y for yes): ')
	print()
	player = 1 if ch == 'y' or ch == 'Y' else -1

	while available():
		player *= -1
		aiUpdate() if player == 1 else playerUpdate()
		dispBoard()
		x = over(board)
		if x:
			break
	
	print(pDict[x])


board = [[0 for i in range(3)] for j in range(3)]
bDict = {-1:'O', 0: '_', 1:'X'}
pDict = {-1:'Human wins! Good job', 0: 'It is a tie', 1:'AI wins! Better luck next time'}
util = {}

if __name__ == '__main__':
	main()
