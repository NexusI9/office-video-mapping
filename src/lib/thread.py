# me - this DAT
# 
# frame - the current frame
# state - True if the timeline is paused
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.



def onOffToOn(channel, sampleIndex, val, prev):
	print('set foreground')
	op('perform').setForeground()
	return

def onValueChange(channel, sampleIndex, val, prev):
	return