#! /usr/bin/python

from morse_code import *
from gpiozero import LED
from time import sleep



class LightEncoder(object):

	def __init__(self, gpioPin):
		
		self.__led = LED(gpioPin)

	# End __init__

	
	def dot(self, t):
		self.__led.on()
		sleep(t)

	# End dot


	def dash(self, t):
		self.__led.on()
		sleep(t)
	
	# End dash
	
	
	def space(self, t):
		self.__led.off()
		sleep(t)
	
	# End space

# End LightEncoder


encoder = LightEncoder(15)

text = raw_input("Enter text to encode: ")

sendMessage(text, .5, encoder)
