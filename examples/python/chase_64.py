#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time

numLEDs = 64
client = opc.Client('localhost:7890')

pixels = [ (0,0,0) ] * numLEDs
pixels[9] = (255 , 255, 255)
pixels[10] = (255 , 255, 255)
pixels[11] = (255 , 255, 255)
client.put_pixels(pixels)
time.sleep(0.02)

# while True:
# 	for i in range(numLEDs):
# 		pixels = [ (0,0,0) ] * numLEDs
# 		pixels[i] = (255, 255, 255)
# 		client.put_pixels(pixels)
# 		time.sleep(0.02)
