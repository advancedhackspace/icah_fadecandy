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
			print "calcPixelArrayPos(",x,",",y,") =",calcPixelArrayPos(x,y)
			pixels[calcPixelArrayPos(x,y)] = pixelMatrix[x][y]


def updatePixelMatrixWithList(s):
	for i in range(len(s)):
		pixelMatrix[s[i][0]][s[i][1]] = s[i][2]

# for i in range(len(pixelMatrix[0])):
	# pixelMatrix[i][i] = (255,255,255)
pixelMatrix[33][31] = (255,255,255)



matrixToArray(pixelMatrix)
client.put_pixels(pixels)

