# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.

queue = op('queue')
transit = mod('lib_transition')
config = mod('lib_config')
numvideo = queue.numRows
currentVideo = ''


def onOffToOn(channel, sampleIndex, val, prev):
	currentindex = int(op('info').par.value0)
	print('SWITCH VIDEO')
	print('Queue length: ' + str(numvideo) )
	print('Current index: ' + str(currentindex) )

	#preload next movie
	if(currentindex+1 < numvideo):

		#update current index
		
		currentindex+=1
		op('info').par.value0 = currentindex

		print('=> Current index: ' + str(currentindex) +' /'+str(numvideo))

		#pause the movie that reached 1
		endedMovie = op('moviefilein1') if currentindex%2 == 1 else op('moviefilein2')
		endedMovie.par.play = False
		#endedMovie.par.reload.pulse()
			
		#feed new file to moviefileop
		nextmovie = queue[currentindex,0]
		print('=> Next movie: ' + str(nextmovie) )

		nextchannel = op('moviefilein2') if currentindex%2 == 1 else op('moviefilein1')
		nextchannel.par.file = nextmovie
		nextchannel.preload()
		nextchannel.par.play = True

		#finally switch index
		transit.setTransition('queue', currentindex%2)

		#if(	queue[currentindex+1,0] ):
		#	endedMovie.par.file = queue[currentindex+1,0]
		#	endedMovie.preload()

		
		return print( '[...] Loading ' + str(nextmovie)  + ' in ' + str(nextchannel) )
	else: 
		#loop final outro
		return print( 'Looping outro' )
		
	return

def whileOn(channel, sampleIndex, val, prev):
	return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
	return
	