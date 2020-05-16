import TicTacToe_AI as t3
import curses


menuOptions = ['Play 1st', 'Play 2nd', 'Exit']
p = [True, True, True]


def dispBoard(stdscr, h, w):
	"""Displaying the board"""
	stdscr.clear()

	for i in range(3):
		for j in range(3):
			stdscr.addstr(h//2 - 2 + 2*i, w//2 - 3 + 3*j, t3.bDict[t3.board[i][j]])

	stdscr.refresh()


def playerUpdate(stdscr, h, w):
	"""Updating the board according to the player's input"""
	stdscr.addstr(h//2 - 10, w//2 - 5, 'Your Move?')
	while True:
		stdscr.refresh()
		try:
			x = stdscr.getch()
			if x == 27:
				break
			elif x == curses.KEY_MOUSE:
				_, j, i, _, _ = curses.getmouse()
				i = abs((i - (h//2 - 2))//2)
				j = abs(( j - (w//2 - 3))//3)
				x = 3*i + j + 1

			else:
				x  -= 48
			assert x in list(range(1,10))
		except:
			stdscr.addstr(h//2 - 11, w//2 - 15, 'Enter a number between 1 and 9')
		else:
			i = (x - 1) // 3
			j = (x - 1) % 3
			if t3.board[i][j] == 0:
				t3.board[i][j] = -1
				break
			else:
				stdscr.addstr(h//2 - 11, w//2 - 15, 'Illegal move! Please try again')
	exit()


def dispMenu(stdscr, k, h, w):
	"""Displaying the menu"""
	stdscr.addstr(h//2 - 10, w//2 - 14, 'Hello & Welcome to TicTacToe')

	for i, j in enumerate(menuOptions):
		x = w//2 - len(j)//2
		y = h//2 - len(menuOptions)//2 + i
		if i == k:
			stdscr.attron(curses.color_pair(1))
		if p[i]:
			stdscr.addstr(y, x, j)
		stdscr.attroff(curses.color_pair(1))

	stdscr.refresh()


def menu(stdscr):
	"""Initial menu screen"""
	global p
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	h, w = stdscr.getmaxyx()

	sel = 0
	dispMenu(stdscr, sel, h, w)

	while True:
		key = stdscr.getch()
		stdscr.clear()

		if key == curses.KEY_UP:
			sel = max(sel-1, 0)
		elif key == curses.KEY_DOWN:
			sel = min(sel+1, 2)
		elif key == curses.KEY_ENTER or key in [10, 13]:
			break
		elif key == curses.KEY_MOUSE:
			_, x, y, _, _ = curses.getmouse()
			if (x in range(w//2 - 4, w//2 + 4) and y in [h//2 - 1, h//2] or
				x in range(w//2 - 2, w//2 + 2) and y == h//2 + 1):
				sel = y - h//2 + 1
				break

		dispMenu(stdscr, sel, h, w)

	p[sel] = False
	p = [not _ for _ in p]
	dispMenu(stdscr, sel, h, w)
	return sel, h, w


def main(stdscr):
	"""Handles the flow of the game"""
	curses.curs_set(0)
	curses.mousemask(1)

	ch, h, w = menu(stdscr)
	if ch == 2:
		exit()
	else:
		player = {0: 1, 1: -1}[ch]

	stdscr.clear()
	dispBoard(stdscr, h, w)
	while t3.available():
		player *= -1
		t3.aiUpdate() if player == 1 else playerUpdate(stdscr, h, w)
		dispBoard(stdscr, h, w)
		x = t3.over(t3.board)
		if x:
			break
	
	y = t3.pDict[x]
	stdscr.addstr(h//2 + 10, w//2 - len(y)//2, y)
	stdscr.addstr(h//2 + 11, w//2 - 10, 'Press ant key to quit')
	stdscr.refresh()
	stdscr.getch()


curses.wrapper(main)