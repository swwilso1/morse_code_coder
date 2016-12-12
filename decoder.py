#! /usr/bin/python

from morse_code import *
from gpiozero import LightSensor
from time import sleep, time

class Decoder(object):
	
	def __init__(self, sensorNumber):

		self.__sensor = LightSensor(sensorNumber)
			
		self.__sensitivityThreshold = 0.5

		self.__delta = 1

	# End __init__
	
	
	def readLightValue(self):
		
		lightBegin = time()
		
		self.__sensor.wait_for_dark()
		
		lightEnd = time()
		
		diff = lightEnd - lightBegin
	
		if abs(diff - (DOT_LENGTH * self.__delta)) \
			< self.__sensitivityThreshold:
				
			print "DOT"
			
			return DOT
		
		elif abs(diff - (DASH_LENGTH * self.__delta)) \
			< self.__sensitivityThreshold:
				
			print "DASH"
			
			return DASH

#		print "Light-None"

		return None
		
	# End readLightValue
	
	
	def readDarkValue(self):
				
		darkBegin = time()
		
		self.__sensor.wait_for_light(self.__delta *
			(LENGTH_BETWEEN_WORDS + 1))
		
		darkEnd = time()
		
		diff = darkEnd - darkBegin
		
		if abs(diff - (LENGTH_BETWEEN_LETTER_UNITS * self.__delta)) \
			< self.__sensitivityThreshold:
			
#			print "Dark-None"
			return None
		
		elif abs(diff - (LENGTH_BETWEEN_LETTERS * self.__delta)) \
			< self.__sensitivityThreshold:
				
			print "LETTER"
			return LETTER
		
		elif abs(diff - (LENGTH_BETWEEN_WORDS * self.__delta)) \
			< self.__sensitivityThreshold:
			
			print "WORD"
			return WORD
		
		print "END"
		return END

	# End readDarkValue
	

	def read(self, delta):

		self.__delta = delta

		while True:
			
#			print "** waiting for light"
			self.__sensor.wait_for_light()
			
			value = self.readLightValue()
			
			if value == None:
				
				continue
			
			yield value

#			print "** waiting for dark"
			value = self.readDarkValue()
			
			if value == None:
				
				continue
						
			if value == END:
				
				yield LETTER
				yield WORD
			
			elif value == WORD:
				
				yield LETTER
				
			yield value
			
			if value == END:
				
				break
		
	# End read
	
# End Decoder

decoder = Decoder(4)

print "Waiting for Morse code"

res = readMessage(.5, decoder)

print "Received the following via Morse code"
print res

