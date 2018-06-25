#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time
import random
import curses

import threading, time
import os, struct, array
from fcntl import ioctl

numLEDs = 1088
numLEDsPerStrip = 32
xLEDs = 34
yLEDs = 32
client = opc.Client('localhost:7890')
evbuf = ""

black = [ (0,0,0) ] * (numLEDs-55)
white = [ (255,255,255) ] * (numLEDs-55)
red = [ (255,0,0) ] * (numLEDs-55)

blackMatrix = [[(0,0,0)] * yLEDs for i in range(xLEDs)]
whiteMatrix = [[(255,255,255)] * yLEDs for i in range(xLEDs)]
redMatrix = [[(255,0,0)] * yLEDs for i in range(xLEDs)]

pixels = [ (0,0,0) ] * numLEDs
pixelMatrix = [[(0,0,0)] * yLEDs for i in range(xLEDs)]

start_mode = True
ball = None
paddle1 = [
	[0,	(yLEDs/2)+2,	(255,255,255)], 
	[0,	(yLEDs/2)+1,	(255,255,255)], 
	[0,	(yLEDs/2),		(255,255,255)], 
	[0,	(yLEDs/2)-1,	(255,255,255)], 
	[0,	(yLEDs/2)-2,	(255,255,255)]
	]



paddle2 = [
	[xLEDs-1,	(yLEDs/2)+2	, (255,255,255)], 
	[xLEDs-1,	(yLEDs/2)+1	, (255,255,255)], 
	[xLEDs-1,	(yLEDs/2)	, (255,255,255)], 
	[xLEDs-1,	(yLEDs/2)-1 , (255,255,255)], 
	[xLEDs-1,	(yLEDs/2)-2 , (255,255,255)]
	]

def gameStartPixels(b):
	pixelMatrix[	0+5		][	0+21	] = (	b	,	b	,	b	)#P
	pixelMatrix[	0+5		][	1+21	] = (	b	,	b	,	b	)
	pixelMatrix[	0+5		][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	0+5		][	3+21	] = (	b	,	b	,	b	)
	pixelMatrix[	0+5		][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	1+5		][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	1+5		][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	1+5		][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	1+5		][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	1+5		][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	2+5		][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	2+5		][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	2+5		][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	2+5		][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	2+5		][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	3+5		][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	3+5		][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	3+5		][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	3+5		][	3+21	] = (	b	,	b	,	b	)
	pixelMatrix[	3+5		][	4+21	] = (	0	,	0	,	0	)
	pixelMatrix[	4+5		][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	4+5		][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	4+5		][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	4+5		][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	4+5		][	4+21	] = (	0	,	0	,	0	)
	pixelMatrix[	5+5		][	0+21	] = (	b	,	b	,	b	)#R
	pixelMatrix[	5+5		][	1+21	] = (	b	,	b	,	b	)
	pixelMatrix[	5+5		][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	5+5		][	3+21	] = (	b	,	b	,	b	)
	pixelMatrix[	5+5		][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	6+5		][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	6+5		][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	6+5		][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	6+5		][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	6+5		][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	7+5		][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	7+5		][	1+21	] = (	b	,	b	,	b	)
	pixelMatrix[	7+5		][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	7+5		][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	7+5		][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	8+5		][	0+21	] = (	b	,	b	,	b	)
	pixelMatrix[	8+5		][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	8+5		][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	8+5		][	3+21	] = (	b	,	b	,	b	)
	pixelMatrix[	8+5		][	4+21	] = (	0	,	0	,	0	)
	pixelMatrix[	9+5		][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	9+5		][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	9+5		][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	9+5		][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	9+5		][	4+21	] = (	0	,	0	,	0	)
	pixelMatrix[	10+5	][	0+21	] = (	b	,	b	,	b	)#E
	pixelMatrix[	10+5	][	1+21	] = (	b	,	b	,	b	)
	pixelMatrix[	10+5	][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	10+5	][	3+21	] = (	b	,	b	,	b	)
	pixelMatrix[	10+5	][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	11+5	][	0+21	] = (	b	,	b	,	b	)
	pixelMatrix[	11+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	11+5	][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	11+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	11+5	][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	12+5	][	0+21	] = (	b	,	b	,	b	)
	pixelMatrix[	12+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	12+5	][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	12+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	12+5	][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	13+5	][	0+21	] = (	b	,	b	,	b	)
	pixelMatrix[	13+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	13+5	][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	13+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	13+5	][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	14+5	][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	14+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	14+5	][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	14+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	14+5	][	4+21	] = (	0	,	0	,	0	)			
	pixelMatrix[	15+5	][	0+21	] = (	b	,	b	,	b	)#s
	pixelMatrix[	15+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	15+5	][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	15+5	][	3+21	] = (	b	,	b	,	b	)
	pixelMatrix[	15+5	][	4+21	] = (	0	,	0	,	0	)
	pixelMatrix[	16+5	][	0+21	] = (	b	,	b	,	b	)
	pixelMatrix[	16+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	16+5	][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	16+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	16+5	][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	17+5	][	0+21	] = (	b	,	b	,	b	)
	pixelMatrix[	17+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	17+5	][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	17+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	17+5	][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	18+5	][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	18+5	][	1+21	] = (	b	,	b	,	b	)
	pixelMatrix[	18+5	][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	18+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	18+5	][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	19+5	][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	19+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	19+5	][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	19+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	19+5	][	4+21	] = (	0	,	0	,	0	)
	pixelMatrix[	20+5	][	0+21	] = (	b	,	b	,	b	) #s
	pixelMatrix[	20+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	20+5	][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	20+5	][	3+21	] = (	b	,	b	,	b	)
	pixelMatrix[	20+5	][	4+21	] = (	0	,	0	,	0	)
	pixelMatrix[	21+5	][	0+21	] = (	b	,	b	,	b	)
	pixelMatrix[	21+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	21+5	][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	21+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	21+5	][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	22+5	][	0+21	] = (	b	,	b	,	b	)
	pixelMatrix[	22+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	22+5	][	2+21	] = (	b	,	b	,	b	)
	pixelMatrix[	22+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	22+5	][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	23+5	][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	23+5	][	1+21	] = (	b	,	b	,	b	)
	pixelMatrix[	23+5	][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	23+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	23+5	][	4+21	] = (	b	,	b	,	b	)
	pixelMatrix[	24+5	][	0+21	] = (	0	,	0	,	0	)
	pixelMatrix[	24+5	][	1+21	] = (	0	,	0	,	0	)
	pixelMatrix[	24+5	][	2+21	] = (	0	,	0	,	0	)
	pixelMatrix[	24+5	][	3+21	] = (	0	,	0	,	0	)
	pixelMatrix[	24+5	][	4+21	] = (	0	,	0	,	0	)


	#######################################################################3

	pixelMatrix[	0+5		][	0+13	] = (	b	,	b	,	b	) #S
	pixelMatrix[	0+5		][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	0+5		][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	0+5		][	3+13	] = (	b	,	b	,	b	)
	pixelMatrix[	0+5		][	4+13	] = (	0	,	0	,	0	)
	pixelMatrix[	1+5		][	0+13	] = (	b	,	b	,	b	)
	pixelMatrix[	1+5		][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	1+5		][	2+13	] = (	b	,	b	,	b	)
	pixelMatrix[	1+5		][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	1+5		][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	2+5		][	0+13	] = (	b	,	b	,	b	)
	pixelMatrix[	2+5		][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	2+5		][	2+13	] = (	b	,	b	,	b	)
	pixelMatrix[	2+5		][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	2+5		][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	3+5		][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	3+5		][	1+13	] = (	b	,	b	,	b	)
	pixelMatrix[	3+5		][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	3+5		][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	3+5		][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	4+5		][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	4+5		][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	4+5		][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	4+5		][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	4+5		][	4+13	] = (	0	,	0	,	0	)
	pixelMatrix[	5+5		][	0+13	] = (	0	,	0	,	0	) #T
	pixelMatrix[	5+5		][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	5+5		][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	5+5		][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	5+5		][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	6+5		][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	6+5		][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	6+5		][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	6+5		][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	6+5		][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	7+5		][	0+13	] = (	b	,	b	,	b	)
	pixelMatrix[	7+5		][	1+13	] = (	b	,	b	,	b	)
	pixelMatrix[	7+5		][	2+13	] = (	b	,	b	,	b	)
	pixelMatrix[	7+5		][	3+13	] = (	b	,	b	,	b	)
	pixelMatrix[	7+5		][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	8+5		][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	8+5		][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	8+5		][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	8+5		][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	8+5		][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	9+5		][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	9+5		][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	9+5		][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	9+5		][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	9+5		][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	10+5	][	0+13	] = (	b	,	b	,	b	) #A
	pixelMatrix[	10+5	][	1+13	] = (	b	,	b	,	b	)
	pixelMatrix[	10+5	][	2+13	] = (	b	,	b	,	b	)
	pixelMatrix[	10+5	][	3+13	] = (	b	,	b	,	b	)
	pixelMatrix[	10+5	][	4+13	] = (	0	,	0	,	0	)
	pixelMatrix[	11+5	][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	11+5	][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	11+5	][	2+13	] = (	b	,	b	,	b	)
	pixelMatrix[	11+5	][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	11+5	][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	12+5	][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	12+5	][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	12+5	][	2+13	] = (	b	,	b	,	b	)
	pixelMatrix[	12+5	][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	12+5	][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	13+5	][	0+13	] = (	b	,	b	,	b	) 
	pixelMatrix[	13+5	][	1+13	] = (	b	,	b	,	b	)
	pixelMatrix[	13+5	][	2+13	] = (	b	,	b	,	b	)
	pixelMatrix[	13+5	][	3+13	] = (	b	,	b	,	b	)
	pixelMatrix[	13+5	][	4+13	] = (	0	,	0	,	0	)
	pixelMatrix[	14+5	][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	14+5	][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	14+5	][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	14+5	][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	14+5	][	4+13	] = (	0	,	0	,	0	)
	pixelMatrix[	15+5	][	0+13	] = (	b	,	b	,	b	)#R
	pixelMatrix[	15+5	][	1+13	] = (	b	,	b	,	b	)
	pixelMatrix[	15+5	][	2+13	] = (	b	,	b	,	b	)
	pixelMatrix[	15+5	][	3+13	] = (	b	,	b	,	b	)
	pixelMatrix[	15+5	][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	16+5	][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	16+5	][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	16+5	][	2+13	] = (	b	,	b	,	b	)
	pixelMatrix[	16+5	][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	16+5	][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	17+5	][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	17+5	][	1+13	] = (	b	,	b	,	b	)
	pixelMatrix[	17+5	][	2+13	] = (	b	,	b	,	b	)
	pixelMatrix[	17+5	][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	17+5	][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	18+5	][	0+13	] = (	b	,	b	,	b	)
	pixelMatrix[	18+5	][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	18+5	][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	18+5	][	3+13	] = (	b	,	b	,	b	)
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
	pixelMatrix[	20+5	][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	21+5	][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	21+5	][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	21+5	][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	21+5	][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	21+5	][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	22+5	][	0+13	] = (	b	,	b	,	b	)
	pixelMatrix[	22+5	][	1+13	] = (	b	,	b	,	b	)
	pixelMatrix[	22+5	][	2+13	] = (	b	,	b	,	b	)
	pixelMatrix[	22+5	][	3+13	] = (	b	,	b	,	b	)
	pixelMatrix[	22+5	][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	23+5	][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	23+5	][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	23+5	][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	23+5	][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	23+5	][	4+13	] = (	b	,	b	,	b	)
	pixelMatrix[	24+5	][	0+13	] = (	0	,	0	,	0	)
	pixelMatrix[	24+5	][	1+13	] = (	0	,	0	,	0	)
	pixelMatrix[	24+5	][	2+13	] = (	0	,	0	,	0	)
	pixelMatrix[	24+5	][	3+13	] = (	0	,	0	,	0	)
	pixelMatrix[	24+5	][	4+13	] = (	b	,	b	,	b	)

def calcPixelArrayPos( _x, _y):
	pos = (_x*numLEDsPerStrip) + ((_x%2)*numLEDsPerStrip) + (((_x+1)%2)*_y) + ((_x%2)*-_y) + ((_x%2)*-1)
	return pos

def matrixToArray(coords):
	for x in range(34):
		for y in range(32):
			pixels[calcPixelArrayPos(x,y)] = coords[x][y]

def updatePixelMatrixWithList(s):
	for i in range(len(s)):
		pixelMatrix[s[i][0]][s[i][1]] = s[i][2]

def resetPixelMatrix():
	for x in range(34):
		for y in range(32):
			pixelMatrix[x][y] = (0,0,0)

def letterToLED(_letter, _x, _y):
	letterMatrix = [[(0,0,0)] * 5 for i in range(5)]
	letterMatrix = alphabet[_letter]

def gameOver():
	pixelMatrix = redMatrix
	matrixToArray(pixelMatrix)
	pixels = [(255,0,0)] * numLEDs
	client.put_pixels(pixels)
	time.sleep(0.1) 
	pixelMatrix = blackMatrix
	matrixToArray(pixelMatrix)
	pixels = [(0,0,0)] * numLEDs
	client.put_pixels(pixels)
	time.sleep(0.1)
	pixelMatrix = redMatrix
	matrixToArray(pixelMatrix)
	pixels = [(255,0,0)] * numLEDs
	client.put_pixels(pixels)
	time.sleep(0.1) 
	pixelMatrix = blackMatrix
	matrixToArray(pixelMatrix)
	pixels = [(0,0,0)] * numLEDs
	client.put_pixels(pixels)
	time.sleep(0.1)
	pixelMatrix = redMatrix
	matrixToArray(pixelMatrix)
	pixels = [(255,0,0)] * numLEDs
	client.put_pixels(pixels)
	time.sleep(0.1) 
	pixelMatrix = blackMatrix
	matrixToArray(pixelMatrix)
	pixels = [(0,0,0)] * numLEDs
	client.put_pixels(pixels)
	time.sleep(0.1)

def dancematThread():
	global evbuf
	lock = threading.Lock()
	while True:
		with lock:
			evbuf = jsdev.read(8)

if __name__ == '__main__':
	# s = curses.initscr()
	# curses.curs_set(0)
	# sh, sw = s.getmaxyx()
	# w = curses.newwin(sh, sw, 0, 0)
	# w.keypad(1)
	# w.timeout(100)

	resetPixelMatrix()
	client.put_pixels(pixels)
	# pixelMatrix[0][(yLEDs/2)+2] 	= (255,255,255)
	# pixelMatrix[0][(yLEDs/2)+1]		= (255,255,255)
	# pixelMatrix[0][(yLEDs/2)]		= (255,255,255)
	# pixelMatrix[0][(yLEDs/2)-1]		= (255,255,255)
	# pixelMatrix[0][(yLEDs/2)-2]		= (255,255,255)
	updatePixelMatrixWithList(paddle1)
	updatePixelMatrixWithList(paddle2)
	matrixToArray(pixelMatrix)
	client.put_pixels(pixels)