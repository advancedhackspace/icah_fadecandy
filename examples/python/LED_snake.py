#!/usr/bin/env python

import opc, time
import random
import curses

import threading, time
import os, struct, array
from fcntl import ioctl

import sys
import LED_snake_joystick as joystick

numLEDs = 1088+55
numLEDsPerStrip = 32
xLEDs = 34
yLEDs = 32
client = opc.Client('localhost:7890')
evbuf = ""

black = [ (0,0,0) ] * (numLEDs)
white = [ (255,255,255) ] * (numLEDs)
red = [ (255,0,0) ] * (numLEDs)

blackMatrix = [[(0,0,0)] * yLEDs for i in range(xLEDs)]
whiteMatrix = [[(255,255,255)] * yLEDs for i in range(xLEDs)]
redMatrix = [[(255,0,0)] * yLEDs for i in range(xLEDs)]

pixels = [ (0,0,0) ] * numLEDs
pixelMatrix = [[(0,0,0)] * yLEDs for i in range(xLEDs)]

start_mode = True
food = None
snake = []

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
	pos = 55+(_x*numLEDsPerStrip) + ((_x%2)*numLEDsPerStrip) + (((_x+1)%2)*_y) + ((_x%2)*-_y) + ((_x%2)*-1)
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

def generateFoodPos():
	f=None
	while f is None:
		newfood = [[
		random.randint(1,xLEDs-2),
		random.randint(1,yLEDs-2),
		(0,255,0)
		]]
		f = newfood if newfood not in snake else None
		return f

def letterToLED(_letter, _x, _y):
	letterMatrix = [[(0,0,0)] * 5 for i in range(5)]
	letterMatrix = alphabet[_letter]

def gameOver():
	for i in range(0, 3):
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

			# alphabet = {
			# 	"A" : [
			# 		[(255,255,255), (255,255,255), (255,255,255), (255,255,255)],
			# 		[(255,255,255), (255,255,255), (255,255,255), (255,255,255)],
			# 		[(255,255,255), (255,255,255), (255,255,255), (255,255,255)],
			# 		[(255,255,255), (255,255,255), (255,255,255), (255,255,255)],
			# 	]
			# }

if __name__ == '__main__':
	# Set mode based on command line args
	# 0 = game mode
	# 1 = dev mode (don't use joysticks, send data to opengl server)
	assert (len(sys.argv) == 2), 'Incorrect number of arguments supplied'

	if (sys.argv[1] == "0"):
		print '0'
	else:
		print '1'

	# Iterate over the joystick devices.
	print('Available devices:')

	for fn in os.listdir('/dev/input'):
		if fn.startswith('js'):
			print('  /dev/input/%s' % (fn))

	# We'll store the states here.
	axis_states = {}
	button_states = {}

	# Import joystick constants
	axis_names = joystick.axis_names
	button_names = joystick.button_names

	axis_map = []
	button_map = []

	# Open the joystick device.
	fn = '/dev/input/js0'
	print('Opening %s...' % fn)
	jsdev = open(fn, 'rb')

	# Get the device name.
	#buf = bytearray(63)
	buf = array.array('c', ['\0'] * 64)
	ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
	js_name = buf.tostring()
	print('Device name: %s' % js_name)

	# Get number of axes and buttons.
	buf = array.array('B', [0])
	ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
	num_axes = buf[0]

	buf = array.array('B', [0])
	ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
	num_buttons = buf[0]

	# Get the axis map.
	buf = array.array('B', [0] * 0x40)
	ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

	for axis in buf[:num_axes]:
		axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
		axis_map.append(axis_name)
		axis_states[axis_name] = 0.0

	# Get the button map.
	buf = array.array('H', [0] * 200)
	ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

	for btn in buf[:num_buttons]:
		btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
		button_map.append(btn_name)
		button_states[btn_name] = 0

	print '%d axes found: %s' % (num_axes, ', '.join(axis_map))
	print '%d buttons found: %s' % (num_buttons, ', '.join(button_map))

	s = curses.initscr()
	curses.curs_set(0)
	sh, sw = s.getmaxyx()
	w = curses.newwin(sh, sw, 0, 0)
	w.keypad(1)
	w.timeout(100)
	startx = xLEDs/4
	starty = yLEDs/2

	# snake = [
	# 	[startx, 	starty, (255,255,255)],
	# 	[startx-1, 	starty, (255,255,255)],
	# 	[startx-2, 	starty, (255,255,255)]
	# ]

	thread = threading.Thread(target = dancematThread)
	thread.daemon = True
	thread.start()
	# time.sleep(5)

	client.put_pixels(pixels)

	try:
		while True:
			brightness = 0
			shift = 1
			while (start_mode):
				# print "in start mode"
				# pixels = black[:]
				# client.put_pixels(pixels)
				brightness = brightness+(5*shift)
				if (brightness  == 255):
					shift = -1
				if (brightness == 100):
					shift = 1
				gameStartPixels(brightness)
				matrixToArray(pixelMatrix)
				client.put_pixels(pixels)
				if evbuf:
					time2, value, type, number = struct.unpack('IhBB', evbuf)
					if type & 0x01:
						button = button_map[number]
						if button:
							button_states[button] = value
							if value:
								# print "%s pressed" % (button)
								if (button == "base4"):
									snake = [
										[startx, 	starty, (255,255,255)],
										[startx-1, 	starty, (255,255,255)],
										[startx-2, 	starty, (255,255,255)]
									]
									start_mode = False
									food = generateFoodPos()
									key = curses.KEY_RIGHT
									prev_key = curses.KEY_RIGHT
									pixels = black[:]
									resetPixelMatrix()
									client.put_pixels(pixels)
									time.sleep(2)

			#next_key = w.getch()
			#key = key if next_key == -1 else next_key
			if evbuf:
				time2, value, type, number = struct.unpack('IhBB', evbuf)
				if type & 0x01:
					button = button_map[number]
					if button:
						button_states[button] = value
						if value:
							# print "%s pressed" % (button)
							if (button == "thumb2"): #UP
								if (prev_key != curses.KEY_DOWN):
									key = curses.KEY_UP
									prev_key = key
							if (button == "thumb"): #DOWN
								if (prev_key != curses.KEY_UP):
									key = curses.KEY_DOWN
									prev_key = key
							if (button == "trigger"): #LEFT
								if (prev_key != curses.KEY_RIGHT):
									key = curses.KEY_LEFT
									prev_key = key
							if (button == "top"): #RIGHT
								if (prev_key != curses.KEY_LEFT):
									key = curses.KEY_RIGHT
									prev_key = key
						# else:
							# print "%s released" % (button)

			if snake[0][0] in [0, xLEDs-1] or snake[0][1] in [0, yLEDs-1] or snake[0] in snake[1:]: #need to add bit to do with colliding with itself
				print snake[0]
				print snake[1:]
				gameOver()
				start_mode = True
				for i, value in enumerate(pixels[1087:1142:1]):
					pixels[i] = (255,255,255)
				pixels = black[:]
				client.put_pixels(pixels)
				# client.put_pixels(pixels)
				continue
				# start_mode = True
				# curses.endwin()
				# quit()

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
				food = generateFoodPos()
			else:
				tail = snake.pop()
				pixelMatrix[tail[0]][tail[1]] = (0,0,0)

			updatePixelMatrixWithList(snake)
			updatePixelMatrixWithList(food)
			matrixToArray(pixelMatrix)
			client.put_pixels(pixels)
			time.sleep(1.0/(len(snake)+1))
	except KeyboardInterrupt:
		curses.endwin()
		quit()
