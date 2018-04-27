#!/usr/bin/env python

# Open Pixel Control client: All lights to solid white

import opc, time

numLEDs = (34*32)
client = opc.Client('localhost:7890')

black = [ (0,0,0) ] * numLEDs
white = [ (255,255,255) ] * numLEDs
test = [ (255,255,255)] * numLEDs

# Fade to white
client.put_pixels(black)
client.put_pixels(black)
time.sleep(0.5)
client.put_pixels(white)
test[520] = (0,0,0)
client.put_pixels(test)
