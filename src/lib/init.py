# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.


import subprocess
import os 
import pathlib

#data
json_dict = None
table = op('queue')
config = mod('lib_config')
info = op('info')

#parent
parent = parent()

#movies
firstChannel = op('moviefilein1')
secondChannel = op('moviefilein2')
loopInChannel = op('loop_intro')
transit = mod('lib_transition')

#dynamic assets (tagline / img)
tagline = op('tagline')
client = op('client')


def getConfigInfo():
    global json_dict;
    json_dict = config.getInfo()

def setLoopIn(): 
    global loopInChannel,parent
    print(parent)
    print('Initialize: set loop_in')

    resetStats()
    resetSwitches()

    #set loop intro & plays it
    loopInChannel.par.play = False
    transit.setTransition('intro', 0)

    #set loop_intro before Start
    loopInChannel.par.file = json_dict['videos']['loop_in']
    loopInChannel.par.play = True
    loopInChannel.par.reload.pulse()

def muteAudio():
    op('audiodevout1').par.active = not op('audiodevout1').par.active

def setQueue():
    global table, firstChannel, secondChannel
    #put files in movie files in

    #set first moviefile
    firstChannel.par.file = table[0,0]
    firstChannel.preload()
    firstChannel.par.play = False

    #reset second channel
    secondChannel.par.file = ''
    secondChannel.par.play = False
    return

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def setDynamicItems():

    global tagline, json_dict, client
    
    tagline.par.text = json_dict['tagline']['value'].replace('\\\\', '\\')
    tagline.par.fontsizex = json_dict['tagline']['fontsize']

    client.par.file = json_dict['client']['image']
    op('transform_client').par.sx = json_dict['client']['size']

    return

def fetchQueue():

    global json_dict, table
    
    #reset table
    table.setSize(0,1)

    #append values to table
    loop_outro = json_dict['videos']['loop_out']
    queue = json_dict['videos']['queue']
  
    for i in range(len(queue)):
        currentvid = queue[i]
        fullpath = str(pathlib.PureWindowsPath( os.getcwd()+currentvid ))
        table.appendRow(currentvid)

    table.appendRow(loop_outro)

def resetStats():
    #set total video duration on output
    info.par.value0 = 0 #set currentindex to 0
    info.par.value1 = table.numRows

def resetSwitches():
    global switchMain, switchQueue
     #reset switch
    transit.setTransition('queue', 0)
    #stop loop intro
    transit.setTransition('intro', 0)

#___MAINS___

def onStartQueue():
    global transit, firstChannel, secondChannel, loopInChannel

    resetStats()

    firstChannel.par.file = table[0,0]
    if( table[1,0]):
        secondChannel.par.file = table[1,0]
        secondChannel.preload()
    

    #set switch to
    transit.setTransition('queue', 0)
    transit.setTransition('intro', 1)

    loopInChannel.par.play = False;
    loopInChannel.par.reset.pulse()

    firstChannel.par.play = True
    secondChannel.par.play = False

    firstChannel.par.reset.pulse()
    secondChannel.par.reset.pulse()


    return

def syncParentDimension():
    global json_dict
    parent.par.w = json_dict['dimension']['width'];
    parent.par.h = json_dict['dimension']['height'];

def onStart():

    getConfigInfo()

    syncParentDimension()

    setLoopIn()
    setDynamicItems()
    resetSwitches()
    resetStats()
    fetchQueue()
    setQueue()

    return


#______________KEY LISTENER_________________
# me - This DAT
# 
# dat - The DAT that received the key event
# key - The name of the key attached to the event.
#		This tries to be consistent regardless of which language
#		the keyboard is set to. The values will be the english/ASCII
#		values that most closely match the key pressed.
#		This is what should be used for shortcuts instead of 'character'.
# character - The unicode character generated.
# alt - True if the alt modifier is pressed
# ctrl - True if the ctrl modifier is pressed
# shift - True if the shift modifier is pressed
# state - True if the event is a key press event
# time - The time when the event came in milliseconds
# cmd - True if the cmd modifier is pressed

def onKey(dat, key, character, alt, lAlt, rAlt, ctrl, lCtrl, rCtrl, shift, lShift, rShift, state, time, cmd, lCmd, rCmd):
    global sequence

    if(key == 'r'):
        #go back to Loop-in
        onStart()

    if(key == 'enter'):
        onStartQueue()

    if(key == 'm' and state == 1):
        muteAudio()



    return

# shortcutName is the name of the shortcut

def onShortcut(dat, shortcutName, time):
	return;
	