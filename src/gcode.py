linlimit = 280
rotatlimit = 720
flow = {'linMaxFlow': 4000, 'rotMaxFlow': 20000}
linsteps_per_mm = 800*2
rotsteps_per_degree = int(36/4)

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
