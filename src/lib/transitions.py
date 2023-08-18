
operator = op('transition_trigger')
map = {
'tagline': 'value0',
'client': 'value1',
'queue': 'value2',
'intro':'value3',
'volume':'value4'
}

def setTransition(target, value):
    if( operator.par[ map[target] ] != value ):
        operator.par[ map[target] ] = value
    return

