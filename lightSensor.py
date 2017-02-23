#! /usr/bin/python

from gpiozero import LightSensor, LED
from time import sleep

ldr = LightSensor(4)
led = LED(24)

on = True
sleeptime = .5
onticks = 0
offticks = 0

while True:
	print(ldr.value)
	sleep(sleeptime)
	if on:
		led.on()
#		print "LED IS ON", ldr.value
		onticks += 1
		if onticks > 5:
			on = False
			onticks = 0
	else:
		led.off()
#		print "LED IS OFF", ldr.value
		offticks += 1
		if offticks > 5:
			on = True
			offticks = 0



