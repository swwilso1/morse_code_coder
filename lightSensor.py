#! /usr/bin/python -i

from gpiozero import LightSensor, LED
from time import sleep

ldr = LightSensor(4)
led = LED(15)

on = True
sleeptime = .5
onticks = 0
offticks = 0

while True:
	print(ldr.value)
	sleep(sleeptime)
	if on:
		led.on()
		onticks += 1
		if onticks > 4:
			on = False
			onticks = 0
	else:
		led.off()
		offticks += 1
		if offticks > 2:
			on = True
			offticks = 0



