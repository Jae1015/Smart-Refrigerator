#!/usr/bin/python
import sys
import smbus
import time 
from time import sleep
from Adafruit_I2C import Adafruit_I2C
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
GPIO.setwarnings(False)
class Luxmeter:
	i2c = None
	gain = 0
	def __init__(self, address=0x39, debug=0, pause=0.8):
		self.i2c = Adafruit_I2C(address)
		self.address = address
		self.pause = pause
		self.debug = debug
		self.gain = 0
		self.i2c.write8(0x80, 0x03)
	def setGain(self,gain=1):
		"""set the gain"""
		if(gain != self.gain):
			if(gain==1):
				self.i2c.write8(0x81,0x02)
				if (self.debug):
					print"Setting low gain"
			else:
				self.i2c.write8(0x81, 0x12)
				if(self.debug):
					print"Setting high gain"
			self.gain=gain;
			time.sleep(self.pause)
	def readWord(self, reg):
		"""Reads a word from I2C device"""
		try:
			wordval = self.i2c.readU16(reg)
			newval = self.i2c.reverseByteOrder(wordval)
			if (self.debug):
				print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X"%(self.address, wordval & 0xFFFF, reg))
			return newval
		except IOError:
			print("Error accessing 0x%02X: Check your I2C address" % self.address)
			return -1
	def readFull(self, reg=0x8C):
		"""Reads visible+IR diode from the I2C device"""
		return self.readWord(reg);
	
	def readIR(self,reg=0x8E):
		"""Reads IR only diode from the I2C device"""
		return self.readWord(reg);
	
	def getLux(self, gain = 0):
		"""Grabs a lux reading either with autoranging (gain=0) or with a specified gain (1, 16)"""
		if (gain == 1 or gain == 16):
			self.setGain(gain)
			ambient = self.readFull()
			IR = self.readIR()
		elif (gain==0):
			self.setGain(16)
			ambient = self.readFull()
		if (ambient < 65535):
		
			IR = self.readIR()
		if (ambient >= 65535 or IR >= 65535):
			self.setGain(1)
			ambient = self.readFull()
			IR = self.readIR()	
	
		if(self.gain==1):
			ambient *= 16
			IR *= 16
			
		if (IR <= 0):
			print"LIGHT ON"
			GPIO.output(25,GPIO.HIGH)
		elif (IR >= 16):
			GPIO.output(25,GPIO.LOW)
	
		ratio = (IR / float(ambient))
			
		if (self.debug):
			print "IR Result", IR
			print "Ambient Result", ambient
		if ((ratio >= 0) & (ratio <= 0.52)):
			lux = (0.0315 * ambient) - (0.0593 * ambient * (ratio**1.4))
		elif (ratio <= 0.65):
			lux = (0.0229 * ambient) - (0.0291 * IR)
		elif (ratio <= 0.80):
			lux = (0.0157 * ambient) - (0.018 * IR)
		elif (ratio <= 1.3):
			lux = (0.00338 * ambient) - (0.0026 * IR)
		elif (ratio > 1.3):
			lux = 0
			
		return lux

#while True:
	#oLuxmeter = Luxmeter()
	#print "Light intensity in term of LUX ",  oLuxmeter.getLux(1)
#	print "====================================================================="
#	time.sleep(.1)
