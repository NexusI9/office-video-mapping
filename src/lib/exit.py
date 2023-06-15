# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.

import os

def onOffToOn(channel, sampleIndex, val, prev):

	os.system('taskkill /f /im MadMapper.exe')
	os.system('taskkill /f /im TouchDesigner.exe')
	os.system('taskkill /f /im node.exe')
	os.system('taskkill /f /im CMD.exe')

	return print("exit")

def whileOn(channel, sampleIndex, val, prev):
	return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
	return
	