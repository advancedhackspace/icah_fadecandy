#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time
import random
import curses

import threading, time
import os, struct, array
from fcntl import ioctl

numLEDs = 1152
numLEDsPerStrip = 32
xLEDs = 34
yLEDs = 32
client = opc.Client('localhost:7890')
evbuf = ""

black = [ (0,0,0) ] * numLEDs
white = [ (255,255,255) ] * numLEDs
red = [ (255,0,0) ] * numLEDs

blackMatrix = [[(0,0,0)] * yLEDs for i in range(xLEDs)]
whiteMatrix = [[(255,255,255)] * yLEDs for i in range(xLEDs)]
redMatrix = [[(255,0,0)] * yLEDs for i in range(xLEDs)]

pixels = [ (0,0,0) ] * numLEDs
pixelMatrix = [[(0,0,0)] * yLEDs for i in range(xLEDs)]

start_mode = True
food = None
snake = []


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
	pixelMatrix = redMatrix
	matrixToArray(pixelMatrix)
	client.put_pixels(pixels)
	time.sleep(0.1) 
	pixelMatrix = blackMatrix
	matrixToArray(pixelMatrix)
	client.put_pixels(pixels)
	time.sleep(0.1)
	pixelMatrix = redMatrix
	matrixToArray(pixelMatrix)
	client.put_pixels(pixels)
	time.sleep(0.1) 
	pixelMatrix = blackMatrix
	matrixToArray(pixelMatrix)
	client.put_pixels(pixels)
	time.sleep(0.1)
	pixelMatrix = redMatrix
	matrixToArray(pixelMatrix)
	client.put_pixels(pixels)
	time.sleep(0.1) 
	pixelMatrix = blackMatrix
	matrixToArray(pixelMatrix)
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


	# Iterate over the joystick devices.
	print('Available devices:')

	for fn in os.listdir('/dev/input'):
	    if fn.startswith('js'):
	        print('  /dev/input/%s' % (fn))

	# We'll store the states here.
	axis_states = {}
	button_states = {}

	# These constants were borrowed from linux/input.h
	axis_names = {
	    0x00 : 'x',
	    0x01 : 'y',
	    0x02 : 'z',
	    0x03 : 'rx',
	    0x04 : 'ry',
	    0x05 : 'rz',
	    0x06 : 'trottle',
	    0x07 : 'rudder',
	    0x08 : 'wheel',
	    0x09 : 'gas',
	    0x0a : 'brake',
	    0x10 : 'hat0x',
	    0x11 : 'hat0y',
	    0x12 : 'hat1x',
	    0x13 : 'hat1y',
	    0x14 : 'hat2x',
	    0x15 : 'hat2y',
	    0x16 : 'hat3x',
	    0x17 : 'hat3y',
	    0x18 : 'pressure',
	    0x19 : 'distance',
	    0x1a : 'tilt_x',
	    0x1b : 'tilt_y',
	    0x1c : 'tool_width',
	    0x20 : 'volume',
	    0x28 : 'misc',
	}

	button_names = {
	    0x120 : 'trigger',
	    0x121 : 'thumb',
	    0x122 : 'thumb2',
	    0x123 : 'top',
	    0x124 : 'top2',
	    0x125 : 'pinkie',
	    0x126 : 'base',
	    0x127 : 'base2',
	    0x128 : 'base3',
	    0x129 : 'base4',
	    0x12a : 'base5',
	    0x12b : 'base6',
	    0x12f : 'dead',
	    0x130 : 'a',
	    0x131 : 'b',
	    0x132 : 'c',
	    0x133 : 'x',
	    0x134 : 'y',
	    0x135 : 'z',
	    0x136 : 'tl',
	    0x137 : 'tr',
	    0x138 : 'tl2',
	    0x139 : 'tr2',
	    0x13a : 'select',
	    0x13b : 'start',
	    0x13c : 'mode',
	    0x13d : 'thumbl',
	    0x13e : 'thumbr',

	    0x220 : 'dpad_up',
	    0x221 : 'dpad_down',
	    0x222 : 'dpad_left',
	    0x223 : 'dpad_right',

	    # XBox 360 controller uses these codes.
	    0x2c0 : 'dpad_left',
	    0x2c1 : 'dpad_right',
	    0x2c2 : 'dpad_up',
	    0x2c3 : 'dpad_down',
	}

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
			
			while (start_mode):
				# print "in start mode"
				pixels = black[:]
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
							if (button == "thumb2"):
								key = curses.KEY_UP
							if (button == "thumb"):
								key = curses.KEY_DOWN
							if (button == "trigger"):
								key = curses.KEY_LEFT
							if (button == "top"):
								key = curses.KEY_RIGHT
						# else:
							# print "%s released" % (button)

			

			if snake[0][0] in [0, xLEDs-1] or snake[0][1] in [0, yLEDs-1] or snake[0] in snake[1:]: #need to add bit to do with colliding with itself
				print snake[0]
				print snake[1:]
				gameOver()
				start_mode = True
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
