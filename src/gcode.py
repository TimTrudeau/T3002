linlimit = 350
rotatlimit = 360
flow = {'linMaxFlow': 1300, 'rotMaxFlow': 15000}


HOME     = 'HOME'
ABSOLUTE = 'ABSOLUTE'
RELATIVE = 'RELATIVE'
MOVE     = 'MOVE'
WAIT     = 'WAIT'
STOP     = 'STOP'
SETZERO  = 'SETZERO'
GET_POS  = 'GET_POS'

_gcodes = {
    HOME:     'G28 X,Y',
    ABSOLUTE: 'G90',
    RELATIVE: 'G91',
    MOVE:     'G1 ',
    WAIT:     'G4 ',
    STOP:     'M410',
    SETZERO:  'G92 X0 Y0',
    GET_POS:  'M114',
}