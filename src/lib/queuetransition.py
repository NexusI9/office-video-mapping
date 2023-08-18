# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.
config = mod('lib_config').getInfo()
transit = mod('lib_transition')

client = {
	"start": config['client']['start'],
	"end": config['client']['end'],
	"video": config['client']['video'],
	"transition": "client"
}

tagline = {
	"start": config['tagline']['start'],
	"end": config['tagline']['end'],
	"video": config['tagline']['video'],
	"transition": "tagline"
}


soundtrack = {
	"video":config['soundtrack']['video'],
	"transition":"volume"
}

table = op('queue')
info = op('info')

def checkInterval(object, time):


	#appear
	if( time >=  int(object['start']) and time <= int(object['end']) ):
	
		transit.setTransition(object['transition'],1)

	#disapear
	elif( time >= int(object['end'])  ):
		transit.setTransition(object['transition'], 0)
	
	else:
		transit.setTransition(object['transition'],0)


def onOffToOn(channel, sampleIndex, val, prev):
	print('update config')
	global config;
	config = mod('lib_config').getInfo()
	
	return

def whileOn(channel, sampleIndex, val, prev):

	currentVideo = str(table[ info.par.value0, 0 ])

	#setup tagline transition
	if( tagline['video'] in currentVideo ):
		checkInterval(tagline, val)
	else:
		transit.setTransition('tagline',0)

	#setup client logo transition	
	if( client['video'] in currentVideo):
		checkInterval(client, val)
	elif( info.par.value0 == table.numRows-1 ):
		transit.setTransition('client',1)
	else:
		transit.setTransition('client',0)

	print(soundtrack['video'])
	print(currentVideo)
	#setup soundtrack transition
	if( soundtrack['video'] in currentVideo):
		transit.setTransition('volume', config['soundtrack']['volume'])

	#switch off soundtrack on loop_out
	if(config['videos']['loop_out'] == currentVideo):
		transit.setTransition('volume', 0)

	return

def onOnToOff(channel, sampleIndex, val, prev):
	print('update config')
	global config;
	config = mod('lib_config').getInfo()
	
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
	return
	