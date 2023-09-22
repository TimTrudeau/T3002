linlimit = 280
rotatlimit = 360
flow = {'linMaxFlow': 5000, 'rotMaxFlow': 5000}
linsteps_per_mm = 800
rotsteps_per_degree = 35

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