#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time
import random
import curses

numLEDs = 1152
numLEDsPerStrip = 32
xLEDs = 34
yLEDs = 32
client = opc.Client('localhost:7890')

pixels = [ (0,0,0) ] * numLEDs
pixelMatrix = [[(0,0,0)] * yLEDs for i in range(xLEDs)]

def calcPixelArrayPos( _x, _y):
	pos = (_x*numLEDsPerStrip) + ((_x%2)*numLEDsPerStrip) + (((_x+1)%2)*_y) + ((_x%2)*-_y) + ((_x%2)*-1)
	return pos


def matrixToArray(coords):
	for x in range(34):
		for y in range(32):
			pixels[calcPixelArrayPos(x,y)] = pixelMatrix[x][y]


def updatePixelMatrixWithList(s):
	for i in range(len(s)):
		pixelMatrix[s[i][0]][s[i][1]] = s[i][2]

def generateFoodPos():
	f=None
	while f is None:
		newfood = [[
				random.randint(1,xLEDs-2),
				random.randint(1,yLEDs-2),
				(255,0,0)
				]]
		f = newfood if newfood not in snake else None
		return f


if __name__ == '__main__':

	s = curses.initscr()
	curses.curs_set(0)
	sh, sw = s.getmaxyx()
	w = curses.newwin(sh, sw, 0, 0)
	w.keypad(1)
	w.timeout(10)
	startx = xLEDs/4
	starty = yLEDs/2

	snake = [
		[startx, 	starty, (255,255,255)],
		[startx-1, 	starty, (255,255,255)],
		[startx-2, 	starty, (255,255,255)]
	]

	food = generateFoodPos()
	key = curses.KEY_RIGHT

	while True:
		next_key = w.getch()
		key = key if next_key == -1 else next_key

		if snake[0][0] in [0, xLEDs-1] or snake[0][1] in [0, yLEDs-1] or snake[0] in snake[1:]: #need to add bit to do with colliding with itself
			print snake[0]
			print snake[1:]
			curses.endwin()
			quit()

		new_head = [snake[0][0], snake[0][1], (255,255,255)]

		if key == curses.KEY_DOWN:
			new_head[1] -= 1
		if key == curses.KEY_UP:
			new_head[1] += 1
		if key == curses.KEY_LEFT:
			new_head[0] -= 1
		if key == curses.KEY_RIGHT:
			new_head[0] += 1

		snake.insert(0, new_head)

		if (snake[0][0] == food[0][0]) and (snake[0][1] == food [0][1]):
			# pixelMatrix[food[0][0]][food[0][1]] = (255,255,255)
			food = generateFoodPos()
		else:
			tail = snake.pop()
			pixelMatrix[tail[0]][tail[1]] = (0,0,0)

		updatePixelMatrixWithList(snake)
		updatePixelMatrixWithList(food)
		matrixToArray(pixelMatrix)
		client.put_pixels(pixels)
		print len(snake)
		time.sleep(1.0/(len(snake)+1))