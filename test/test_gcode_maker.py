

import gcode_maker as gm
import pytest
from gcode import linlimit, rotatlimit
from gcode_maker import GCodeMaker


def test_GCodeMaker():
    GCM = GCodeMaker(None)
    assert GCM.linear_limit == linlimit
    assert GCM.rotation_limit == rotatlimit

def test_GCodeMaker_exception():
    """Missing com port in call to GCodeMaker"""
    with pytest.raises(TypeError):
        GCM = GCodeMaker()

def test_open_serial_port():
    with gm.open_serial_port('com3') as port:
        assert port is not None
        assert port.is_open
        assert port.baudrate == '115200'




if __name__ == '__main__':
    pytest.main()

