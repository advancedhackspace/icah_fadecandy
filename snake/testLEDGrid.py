import opc
from time import sleep

NUM_LEDS = 1088 + 55

client = opc.Client('localhost:7890')
pixels = [(0,0,0)] * NUM_LEDS

#for i in range(55, NUM_LEDS):
#    pixels[i] = (255,255,255)
#    sleep(0.01)
client.put_pixels(pixels)
