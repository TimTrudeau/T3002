

import gcode_maker as gm
import pytest
from gcode import linlimit, rotatlimit
from gcode_maker import GCodeMaker
from robot_serial_port import serial_port_manager,_openSerialPort


def test_GCodeMaker():
    GCM = GCodeMaker(None)
    assert GCM.linear_limit == linlimit
    assert GCM.rotation_limit == rotatlimit

def test_GCodeMaker_exception():
    """Missing com port in call to GCodeMaker"""
    with pytest.raises(TypeError):
        GCM = GCodeMaker()

def test_open_serial_port():
    with _openSerialPort('com4') as port:
        assert port is not None
        assert port.is_open
        assert port.baudrate == 115200

def test_gcode_maker_init():
    GCM = GCodeMaker()
    with serial_port_manager() as manager:
        GCM.serialport = manager
        assert (GCM.serialport.is_open is True)
        GCM.set_absolute()
    pass
    assert (GCM.serialport.is_open is False)



if __name__ == '__main__':
    pytest.main()

