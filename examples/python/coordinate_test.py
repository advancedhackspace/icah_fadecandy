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
pixelMatrix[0][0] = (255,255,255)
pixelMatrix[0][1] = (255,255,255)
pixelMatrix[0][2] = (255,255,255)
pixelMatrix[0][3] = (255,255,255)
pixelMatrix[1][4] = (255,255,255)
pixelMatrix[2][4] = (255,255,255)
pixelMatrix[3][4] = (255,255,255)
pixelMatrix[4][3] = (255,255,255)
pixelMatrix[4][2] = (255,255,255)
pixelMatrix[4][1] = (255,255,255)
pixelMatrix[4][0] = (255,255,255)
pixelMatrix[1][2] = (255,255,255)
pixelMatrix[2][2] = (255,255,255)
pixelMatrix[3][2] = (255,255,255)

pixelMatrix[0+5][0] = (255,255,255)
pixelMatrix[0+5][1] = (255,255,255)
pixelMatrix[0+5][2] = (255,255,255)
pixelMatrix[0+5][3] = (255,255,255)
pixelMatrix[1+5][4] = (255,255,255)
pixelMatrix[2+5][4] = (255,255,255)
pixelMatrix[3+5][4] = (255,255,255)
pixelMatrix[4+5][3] = (255,255,255)
pixelMatrix[4+5][2] = (255,255,255)
pixelMatrix[4+5][1] = (255,255,255)
pixelMatrix[4+5][0] = (255,255,255)
pixelMatrix[1+5][2] = (255,255,255)
pixelMatrix[2+5][2] = (255,255,255)
pixelMatrix[3+5][2] = (255,255,255)

pixelMatrix[0+10][0] = (255,255,255)
pixelMatrix[0+10][1] = (255,255,255)
pixelMatrix[0+10][2] = (255,255,255)
pixelMatrix[0+10][3] = (255,255,255)
pixelMatrix[1+10][4] = (255,255,255)
pixelMatrix[2+10][4] = (255,255,255)
pixelMatrix[3+10][4] = (255,255,255)
pixelMatrix[4+10][3] = (255,255,255)
pixelMatrix[4+10][2] = (255,255,255)
pixelMatrix[4+10][1] = (255,255,255)
pixelMatrix[4+10][0] = (255,255,255)
pixelMatrix[1+10][2] = (255,255,255)
pixelMatrix[2+10][2] = (255,255,255)
pixelMatrix[3+10][2] = (255,255,255)

pixelMatrix[0+15][0] = (255,255,255)
pixelMatrix[0+15][1] = (255,255,255)
pixelMatrix[0+15][2] = (255,255,255)
pixelMatrix[0+15][3] = (255,255,255)
pixelMatrix[1+15][4] = (255,255,255)
pixelMatrix[2+15][4] = (255,255,255)
pixelMatrix[3+15][4] = (255,255,255)
pixelMatrix[4+15][3] = (255,255,255)
pixelMatrix[4+15][2] = (255,255,255)
pixelMatrix[4+15][1] = (255,255,255)
pixelMatrix[4+15][0] = (255,255,255)
pixelMatrix[1+15][2] = (255,255,255)
pixelMatrix[2+15][2] = (255,255,255)
pixelMatrix[3+15][2] = (255,255,255)

pixelMatrix[0+20][0] = (255,255,255)
pixelMatrix[0+20][1] = (255,255,255)
pixelMatrix[0+20][2] = (255,255,255)
pixelMatrix[0+20][3] = (255,255,255)
pixelMatrix[1+20][4] = (255,255,255)
pixelMatrix[2+20][4] = (255,255,255)
pixelMatrix[3+20][4] = (255,255,255)
pixelMatrix[4+20][3] = (255,255,255)
pixelMatrix[4+20][2] = (255,255,255)
pixelMatrix[4+20][1] = (255,255,255)
pixelMatrix[4+20][0] = (255,255,255)
pixelMatrix[1+20][2] = (255,255,255)
pixelMatrix[2+20][2] = (255,255,255)
pixelMatrix[3+20][2] = (255,255,255)

pixelMatrix[0+25][0] = (255,255,255)
pixelMatrix[0+25][1] = (255,255,255)
pixelMatrix[0+25][2] = (255,255,255)
pixelMatrix[0+25][3] = (255,255,255)
pixelMatrix[1+25][4] = (255,255,255)
pixelMatrix[2+25][4] = (255,255,255)
pixelMatrix[3+25][4] = (255,255,255)
pixelMatrix[4+25][3] = (255,255,255)
pixelMatrix[4+25][2] = (255,255,255)
pixelMatrix[4+25][1] = (255,255,255)
pixelMatrix[4+25][0] = (255,255,255)
pixelMatrix[1+25][2] = (255,255,255)
pixelMatrix[2+25][2] = (255,255,255)
pixelMatrix[3+25][2] = (255,255,255)

matrixToArray(pixelMatrix)
client.put_pixels(pixels)

