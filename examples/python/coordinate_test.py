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

x=0
# for i in range(len(pixelMatrix[0])):
	# pixelMatrix[i][i] = (255,255,255)
# P
pixelMatrix[	0+5		][	0+21	] = (	255	,	255	,	255	)#P
pixelMatrix[	0+5		][	1+21	] = (	255	,	255	,	255	)
pixelMatrix[	0+5		][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	0+5		][	3+21	] = (	255	,	255	,	255	)
pixelMatrix[	0+5		][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	1+5		][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	1+5		][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	1+5		][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	1+5		][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	1+5		][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	2+5		][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	2+5		][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	2+5		][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	2+5		][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	2+5		][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	3+5		][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	3+5		][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	3+5		][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	3+5		][	3+21	] = (	255	,	255	,	255	)
pixelMatrix[	3+5		][	4+21	] = (	0	,	0	,	0	)
pixelMatrix[	4+5		][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	4+5		][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	4+5		][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	4+5		][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	4+5		][	4+21	] = (	0	,	0	,	0	)
pixelMatrix[	5+5		][	0+21	] = (	255	,	255	,	255	)#R
pixelMatrix[	5+5		][	1+21	] = (	255	,	255	,	255	)
pixelMatrix[	5+5		][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	5+5		][	3+21	] = (	255	,	255	,	255	)
pixelMatrix[	5+5		][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	6+5		][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	6+5		][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	6+5		][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	6+5		][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	6+5		][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	7+5		][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	7+5		][	1+21	] = (	255	,	255	,	255	)
pixelMatrix[	7+5		][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	7+5		][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	7+5		][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	8+5		][	0+21	] = (	255	,	255	,	255	)
pixelMatrix[	8+5		][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	8+5		][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	8+5		][	3+21	] = (	255	,	255	,	255	)
pixelMatrix[	8+5		][	4+21	] = (	0	,	0	,	0	)
pixelMatrix[	9+5		][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	9+5		][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	9+5		][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	9+5		][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	9+5		][	4+21	] = (	0	,	0	,	0	)
pixelMatrix[	10+5	][	0+21	] = (	255	,	255	,	255	)#E
pixelMatrix[	10+5	][	1+21	] = (	255	,	255	,	255	)
pixelMatrix[	10+5	][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	10+5	][	3+21	] = (	255	,	255	,	255	)
pixelMatrix[	10+5	][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	11+5	][	0+21	] = (	255	,	255	,	255	)
pixelMatrix[	11+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	11+5	][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	11+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	11+5	][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	12+5	][	0+21	] = (	255	,	255	,	255	)
pixelMatrix[	12+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	12+5	][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	12+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	12+5	][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	13+5	][	0+21	] = (	255	,	255	,	255	)
pixelMatrix[	13+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	13+5	][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	13+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	13+5	][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	14+5	][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	14+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	14+5	][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	14+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	14+5	][	4+21	] = (	0	,	0	,	0	)			
pixelMatrix[	15+5	][	0+21	] = (	255	,	255	,	255	)#s
pixelMatrix[	15+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	15+5	][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	15+5	][	3+21	] = (	255	,	255	,	255	)
pixelMatrix[	15+5	][	4+21	] = (	0	,	0	,	0	)
pixelMatrix[	16+5	][	0+21	] = (	255	,	255	,	255	)
pixelMatrix[	16+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	16+5	][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	16+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	16+5	][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	17+5	][	0+21	] = (	255	,	255	,	255	)
pixelMatrix[	17+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	17+5	][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	17+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	17+5	][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	18+5	][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	18+5	][	1+21	] = (	255	,	255	,	255	)
pixelMatrix[	18+5	][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	18+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	18+5	][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	19+5	][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	19+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	19+5	][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	19+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	19+5	][	4+21	] = (	0	,	0	,	0	)
pixelMatrix[	20+5	][	0+21	] = (	255	,	255	,	255	) #s
pixelMatrix[	20+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	20+5	][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	20+5	][	3+21	] = (	255	,	255	,	255	)
pixelMatrix[	20+5	][	4+21	] = (	0	,	0	,	0	)
pixelMatrix[	21+5	][	0+21	] = (	255	,	255	,	255	)
pixelMatrix[	21+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	21+5	][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	21+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	21+5	][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	22+5	][	0+21	] = (	255	,	255	,	255	)
pixelMatrix[	22+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	22+5	][	2+21	] = (	255	,	255	,	255	)
pixelMatrix[	22+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	22+5	][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	23+5	][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	23+5	][	1+21	] = (	255	,	255	,	255	)
pixelMatrix[	23+5	][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	23+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	23+5	][	4+21	] = (	255	,	255	,	255	)
pixelMatrix[	24+5	][	0+21	] = (	0	,	0	,	0	)
pixelMatrix[	24+5	][	1+21	] = (	0	,	0	,	0	)
pixelMatrix[	24+5	][	2+21	] = (	0	,	0	,	0	)
pixelMatrix[	24+5	][	3+21	] = (	0	,	0	,	0	)
pixelMatrix[	24+5	][	4+21	] = (	0	,	0	,	0	)


#######################################################################3

pixelMatrix[	0+5		][	0+13	] = (	255	,	255	,	255	) #S
pixelMatrix[	0+5		][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	0+5		][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	0+5		][	3+13	] = (	255	,	255	,	255	)
pixelMatrix[	0+5		][	4+13	] = (	0	,	0	,	0	)
pixelMatrix[	1+5		][	0+13	] = (	255	,	255	,	255	)
pixelMatrix[	1+5		][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	1+5		][	2+13	] = (	255	,	255	,	255	)
pixelMatrix[	1+5		][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	1+5		][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	2+5		][	0+13	] = (	255	,	255	,	255	)
pixelMatrix[	2+5		][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	2+5		][	2+13	] = (	255	,	255	,	255	)
pixelMatrix[	2+5		][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	2+5		][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	3+5		][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	3+5		][	1+13	] = (	255	,	255	,	255	)
pixelMatrix[	3+5		][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	3+5		][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	3+5		][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	4+5		][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	4+5		][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	4+5		][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	4+5		][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	4+5		][	4+13	] = (	0	,	0	,	0	)
pixelMatrix[	5+5		][	0+13	] = (	0	,	0	,	0	) #T
pixelMatrix[	5+5		][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	5+5		][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	5+5		][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	5+5		][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	6+5		][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	6+5		][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	6+5		][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	6+5		][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	6+5		][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	7+5		][	0+13	] = (	255	,	255	,	255	)
pixelMatrix[	7+5		][	1+13	] = (	255	,	255	,	255	)
pixelMatrix[	7+5		][	2+13	] = (	255	,	255	,	255	)
pixelMatrix[	7+5		][	3+13	] = (	255	,	255	,	255	)
pixelMatrix[	7+5		][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	8+5		][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	8+5		][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	8+5		][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	8+5		][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	8+5		][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	9+5		][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	9+5		][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	9+5		][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	9+5		][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	9+5		][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	10+5	][	0+13	] = (	255	,	255	,	255	) #A
pixelMatrix[	10+5	][	1+13	] = (	255	,	255	,	255	)
pixelMatrix[	10+5	][	2+13	] = (	255	,	255	,	255	)
pixelMatrix[	10+5	][	3+13	] = (	255	,	255	,	255	)
pixelMatrix[	10+5	][	4+13	] = (	0	,	0	,	0	)
pixelMatrix[	11+5	][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	11+5	][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	11+5	][	2+13	] = (	255	,	255	,	255	)
pixelMatrix[	11+5	][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	11+5	][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	12+5	][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	12+5	][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	12+5	][	2+13	] = (	255	,	255	,	255	)
pixelMatrix[	12+5	][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	12+5	][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	13+5	][	0+13	] = (	255	,	255	,	255	) 
pixelMatrix[	13+5	][	1+13	] = (	255	,	255	,	255	)
pixelMatrix[	13+5	][	2+13	] = (	255	,	255	,	255	)
pixelMatrix[	13+5	][	3+13	] = (	255	,	255	,	255	)
pixelMatrix[	13+5	][	4+13	] = (	0	,	0	,	0	)
pixelMatrix[	14+5	][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	14+5	][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	14+5	][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	14+5	][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	14+5	][	4+13	] = (	0	,	0	,	0	)
pixelMatrix[	15+5	][	0+13	] = (	255	,	255	,	255	)#R
pixelMatrix[	15+5	][	1+13	] = (	255	,	255	,	255	)
pixelMatrix[	15+5	][	2+13	] = (	255	,	255	,	255	)
pixelMatrix[	15+5	][	3+13	] = (	255	,	255	,	255	)
pixelMatrix[	15+5	][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	16+5	][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	16+5	][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	16+5	][	2+13	] = (	255	,	255	,	255	)
pixelMatrix[	16+5	][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	16+5	][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	17+5	][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	17+5	][	1+13	] = (	255	,	255	,	255	)
pixelMatrix[	17+5	][	2+13	] = (	255	,	255	,	255	)
pixelMatrix[	17+5	][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	17+5	][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	18+5	][	0+13	] = (	255	,	255	,	255	)
pixelMatrix[	18+5	][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	18+5	][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	18+5	][	3+13	] = (	255	,	255	,	255	)
pixelMatrix[	18+5	][	4+13	] = (	0	,	0	,	0	)
pixelMatrix[	19+5	][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	19+5	][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	19+5	][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	19+5	][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	19+5	][	4+13	] = (	0	,	0	,	0	)
pixelMatrix[	20+5	][	0+13	] = (	0	,	0	,	0	) #T
pixelMatrix[	20+5	][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	20+5	][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	20+5	][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	20+5	][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	21+5	][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	21+5	][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	21+5	][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	21+5	][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	21+5	][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	22+5	][	0+13	] = (	255	,	255	,	255	)
pixelMatrix[	22+5	][	1+13	] = (	255	,	255	,	255	)
pixelMatrix[	22+5	][	2+13	] = (	255	,	255	,	255	)
pixelMatrix[	22+5	][	3+13	] = (	255	,	255	,	255	)
pixelMatrix[	22+5	][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	23+5	][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	23+5	][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	23+5	][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	23+5	][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	23+5	][	4+13	] = (	255	,	255	,	255	)
pixelMatrix[	24+5	][	0+13	] = (	0	,	0	,	0	)
pixelMatrix[	24+5	][	1+13	] = (	0	,	0	,	0	)
pixelMatrix[	24+5	][	2+13	] = (	0	,	0	,	0	)
pixelMatrix[	24+5	][	3+13	] = (	0	,	0	,	0	)
pixelMatrix[	24+5	][	4+13	] = (	255	,	255	,	255	)


matrixToArray(pixelMatrix)
client.put_pixels(pixels)

